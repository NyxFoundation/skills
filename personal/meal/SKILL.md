---
name: meal
description: |
  食事の写真やざっくりしたメニューを受け取り、カロリーと PFC（たんぱく質・脂質・炭水化物）を
  推定して食事記録ブック（meal_log.xlsx）に追記し、Google Drive と life リポジトリへ反映する。
  トリガー: 食事の画像が添付される、「meal」「食べた」「今日の食事」「これ記録して」など
  食事内容の報告、または栄養記録ブックの更新・確認の依頼。
version: 1.0.0
author: gohan
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [nutrition, xlsx, drive, git, slack, workflow]
---

# 食事・栄養記録フロー（meal）

Slack から hermes に食事の写真かメニューを投げると、この順で1本の処理が走る。

```
画像 / メニュー文
  → ① 品目に分解して分量を見積もる
  → ② kcal と P/F/C(g) を推定
  → ③ meal_log.xlsx に追記（集計シートとグラフは自動で伸びる）
  → ④ Google Drive に上書きアップロード
  → ⑤ life リポジトリに commit & push
  → ⑥ その日の合計を Slack に返す
```

## 前提

作業ディレクトリは **private リポジトリ `grandchildrice/life` の `meal/`**。

| ファイル | 役割 |
|---|---|
| `meal_log.xlsx` | 記録ブック本体。シートは 使い方・設定 / 記録 / 日次 / 週次 / 月次 |
| `meal_lib.py` | シートの体裁・数式・グラフ・再計算の共通部品 |
| `append_meal.py` | JSON を受け取って「記録」シートに追記する。**通常はこれだけを使う** |
| `build_meal_log.py` | ブックをゼロから作り直す。**運用中は絶対に実行しない**（記録が消える） |
| `sync_meal.sh` | Drive アップロード + git commit/push |
| `config.json` | Drive のフォルダIDと rclone remote 名。private リポにのみ存在する |

Python は uv 経由でのみ動く（NixOS のため `pip install` は使えない）。
スクリプトは PEP 723 のインラインメタデータを持つので `uv run <script>` でそのまま動く。

## 実行手順

### Step 1: 食事の内容を品目に分解する

画像がある場合は vision で読み取る。皿の上のものを**一品ずつ**挙げ、
それぞれの分量をグラム or 個数で見積もる。ここが推定精度のほぼすべてを決める。

見積もりの手がかり:

- 茶碗1杯の白米 ≒ 150g、丼・ファミレスのライス普通盛 ≒ 200g
- 鶏むね・もも1枚 ≒ 250〜300g、切り身の魚 ≒ 80〜100g
- 卵1個（可食部）≒ 50g、食パン6枚切1枚 ≒ 60g
- 小鉢の副菜 ≒ 50〜80g、味噌汁・スープ1杯 ≒ 150〜200ml
- 「半分こ」「シェア」と言われたら迷わず半量にする

### Step 2: kcal と P/F/C を推定する

**日本食品標準成分表の値を基準にする。** 主要な食品は暗記に頼らず、
不確かなら `WebSearch` で「<食品名> 栄養成分 100g」を確認する。

外食チェーンは公表栄養値があればそれを最優先で使う。
`WebSearch` で「<店名> <メニュー名> カロリー 栄養成分」を引き、
見つからなければ同等メニューからの推定とし、必ず `memo` に「概算」と書く。

推定したら **P×4 + F×9 + C×4 が kcal とおおむね合うか**を必ず検算する。
30%以上ずれていたらどこかを間違えている。`append_meal.py` も同じ検算をして警告を出す。

調味料（油・ドレッシング・マヨネーズ・砂糖）は忘れやすいわりに脂質・糖質へ効くので、
使っていそうなら必ず一品として立てる。

### Step 3: JSON を組み立てて追記する

1品1オブジェクトの JSON 配列にする。同じ食事の品は `time` をそろえる。

```bash
cd ~/workspace/life/meal
cat > /tmp/meal_input.json <<'JSON'
[
  {"date": "2026-09-08", "time": "12:30", "type": "昼食",
   "menu": "鶏むね肉（皮なし）", "amount": "200g",
   "kcal": 215, "p": 44.6, "f": 3.0, "c": 0.0, "memo": "写真から推定"},
  {"date": "2026-09-08", "time": "12:30", "type": "昼食",
   "menu": "白米", "amount": "150g",
   "kcal": 234, "p": 3.8, "f": 0.5, "c": 55.7}
]
JSON

# まず必ず --dry-run で検証する
uv run append_meal.py /tmp/meal_input.json --dry-run

# 問題なければ本適用
uv run append_meal.py /tmp/meal_input.json
```

フィールド:

| キー | 必須 | 内容 |
|---|---|---|
| `date` | ✅ | `YYYY-MM-DD` |
| `menu` | ✅ | 品名 |
| `time` | | `HH:MM`。不明なら朝 08:00 / 昼 12:30 / 夜 19:00 を仮置きし memo に断る |
| `type` | | 朝食 / 昼食 / 夕食 / 間食 / 飲み物 のいずれか |
| `amount` | | 「200g」「1杯」など |
| `kcal` `p` `f` `c` | | 数値。省略すると 0 |
| `memo` | | 推定の根拠、概算である旨、シェアした旨など |

`append_meal.py` がやること:

- 同じ日・同じ時刻・同じメニューの二重登録を検出して中断する（意図的なら `--allow-duplicates`）
- 「記録」シートの空き行に追記し、足りなければ行を増やす
- 新しい日付が範囲外なら日次・週次・月次シートを自動で伸ばす
- グラフの参照範囲を張り直す
- LibreOffice で全数式を再計算し、エラーが残っていれば非ゼロ終了する
- 追記した日の合計を JSON で標準出力に出す

### Step 4: Drive と GitHub に反映する

```bash
cd ~/workspace/life/meal
./sync_meal.sh "meal: 2026-09-08 の食事を記録"
```

Drive のフォルダIDは `config.json` から読む。**スキル側にIDを書かない**
（このスキルは public リポジトリ NyxFoundation/skills にある）。

部分実行:

```bash
./sync_meal.sh --drive-only    # Drive だけ
./sync_meal.sh --git-only      # git だけ
./sync_meal.sh --no-push       # commit まで
```

### Step 5: Slack に返す

`append_meal.py` の出力からその日の合計を読み取り、次の形で短く返す。

```
2026-09-08（火）を記録しました
  昼食  鶏むね肉200g / 白米150g
  合計  449 kcal ・ P 48.4g ・ F 3.5g ・ C 55.7g
  目標比 kcal -1,551 / P -71.6g
推定の根拠: 分量は写真からの目測。外食は公表値がないため概算。
Drive と life リポジトリに反映済み。
```

推定の不確かさは必ず明示する。数字を断定しない。

## 絶対に避けること

- ❌ `build_meal_log.py` を運用中に実行しない — 「記録」シートが初期データで上書きされ、記録が消える
- ❌ `config.json` の中身（Drive フォルダID）を skills リポジトリに書かない — public repo
- ❌ `pip install` を使わない — NixOS。Python は `uv run` 経由のみ
- ❌ 推定値を「正確な値」として提示しない — 目測の分量に基づく概算である旨を必ず添える
- ❌ 「記録」シートの数式列（J列 PFC換算kcal）や集計シートを手で書き換えない
- ❌ 数式エラーが出た状態で Drive / git へ反映しない — `append_meal.py` が非ゼロ終了したら止まる

## トラブルシューティング

**`soffice が見つからない` と出る**
再計算だけスキップされる。数式自体は Excel / Google スプレッドシートで開けば計算されるので
致命的ではない。恒久対応は NixOS の設定に `libreoffice-fresh` を追加すること。
暫定なら `nix build --out-link ~/.local/state/nix/gcroots/libreoffice nixpkgs#libreoffice-fresh`。

**`rclone remote 'gdrive:' が未設定`**
`rclone listremotes` で確認する。再設定は `rclone config`。

**追記したのに日次シートに出ない**
日付が日次シートの範囲外だった場合は自動で伸びるはずなので、まず
`append_meal.py` の出力の `extended_rows` を見る。0 のままなら日付の年がずれている。

**git push が拒否される**
`grandchildrice/life` は private。`gh auth status` で認証を確認する。

## 完了確認

- [ ] `append_meal.py` が `formula_errors: {}` で終了した
- [ ] その日の合計が想定の範囲に収まっている（極端な値は分量の見積もりミス）
- [ ] Drive 上の `meal_log.xlsx` の更新時刻が新しい
- [ ] life リポジトリに commit が積まれ push されている
- [ ] Slack に合計と推定の前提を返した
