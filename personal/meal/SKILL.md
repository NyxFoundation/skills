---
name: meal
description: |
  食事の写真やざっくりしたメニューを受け取り、カロリーと PFC（たんぱく質・脂質・炭水化物）を
  推定して食事記録（records/*.json が正本、meal_log.xlsx は成果物）に追記し、
  Google Drive と life リポジトリへ反映する。
  トリガー: 食事の画像が添付される、「meal」「食べた」「今日の食事」「これ記録して」など
  食事内容の報告、または栄養記録ブックの更新・確認の依頼。
version: 2.0.0
author: gohan
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [nutrition, records, xlsx, drive, git, slack, workflow]
---

# 食事・栄養記録フロー（meal）

## 絶対に守る3つのこと

このスキルで一番大事なのはここ。手順より優先する。

### 1. 正本は records/。xlsx は成果物。xlsx を手で直さない

記録の正本は **`records/`（1食事1ファイルの JSON）**。
`meal_log.xlsx` は `build_meal_log.py` がいつでも全再生成できる成果物。

- xlsx のセルを手で直しても、次の build で上書きされて**消える**
- 値の修正 → 対応する `records/*.json` を編集 → `uv run build_meal_log.py`
- 品目の削除 → `records/*.json` から消す → `uv run build_meal_log.py`
- 目標値の変更 → `config.json` の `target` → `uv run build_meal_log.py`
- xlsx が壊れた・衝突した・消えた → **慌てず `uv run build_meal_log.py`。
  旧構成のような「復旧オペレーション」は不要。正本が無事なら全部戻る**

### 2. Drive は既存の URL をそのまま更新する

Drive 上の `meal_log.xlsx` は**同じファイルを上書きし続ける**。新しいファイルを作らない。
共有相手のブックマークもリンクも、ファイルIDが変わった瞬間に切れる。

`config.json` の `drive_file_id` が Drive 上の実体ID。`sync_meal.sh` が
アップロードの前後でこのIDの一致を検証し、食い違ったら中止する。
**手で `rclone` を叩いて上げ直さない。必ず `sync_meal.sh` を通す。**

### 3. 食事がなにかわからないときは、適当に入れない

**推測で埋めるくらいなら、記録せずに本人に聞く。** 間違った値が入った記録は、
記録が無いより悪い。日次・週次・月次の平均をすべて汚染する。

聞き返すべき場面:

- 写真が暗い・見切れている・盛りが読めなくて品目や分量が判断できない
- 「昼になんか食べた」のように内容が特定できない
- 外食で店名やメニュー名がわからず、栄養値の当たりがつけられない
- 複数の解釈があり、どちらかで数値が大きく変わる（例: 皮つきか皮なしか）

`append_meal.py` は次のいずれかに当たると追記せず中断する:

| 弾かれる条件 | 意味 |
|---|---|
| メニュー名が「不明」「なにか」「たぶん」等 | 内容が特定できていない |
| kcal・P・F・C がすべて 0 | 値を出せていない（水・お茶などは例外） |
| `confidence` が `low` / `unknown` | 推定に自信が無い |
| P×4+F×9+C×4 が kcal と50%以上ずれる | 見積もりのどこかが間違っている |
| 日付が過去180日〜未来2日の窓の外 | **年号ミス**（2025年の事故の再発防止） |
| 同じ日・時刻・メニューが既にある | 二重登録（修正なら `--edit`） |

中断したら**推測で値を作って再実行しない**。本人に確認して、確定してから入れる。
確認が取れた場合にかぎり `--allow-uncertain` `--allow-zero` を使う。

## 流れ

Slack から hermes に食事の写真かメニューを投げると、この順で1本の処理が走る。

```
画像 / メニュー文
  → ① 品目に分解して分量を見積もる
        └ 特定できない品があれば ここで止めて本人に聞く
  → ② kcal と P/F/C(g) を推定
        └ 値の当たりがつかなければ ここで止めて本人に聞く
  → ③ records/YYYYMMDD_HHMM_<type>.json に書き出し（1食事1ファイル）
  → ④ meal_log.xlsx を records/ から全再生成（再計算・検査つき）
  → ⑤ sync_meal.sh: rebase → ドリフト検査(自動ヒール) → Drive上書き(ID検証) → commit/push
  → ⑥ その日の合計と、推定の前提を Slack に返す
```

## 前提

作業ディレクトリは **private リポジトリ `grandchildrice/life` の `meal/`**。

| ファイル | 役割 |
|---|---|
| `records/` | **正本**。1食事1ファイル。`YYYYMMDD_HHMM_<type>.json` に品目の配列 |
| `meal_log.xlsx` | 成果物。build がいつでも作り直す。git には入るが「原本」ではない |
| `meal_lib.py` | 共通部品。体裁・数式・グラフ・正本の読み書き・検証・全再生成 |
| `append_meal.py` | JSON を受け取って records/ に追記してブックを再生成。**通常はこれだけを使う** |
| `build_meal_log.py` | records/ からブックを全再生成。**いつでも実行してよい** |
| `check_meal.py` | 正本とブックの健全性。Drive / git に出す前の関門 |
| `sync_meal.sh` | Drive + git。rebase・xlsx衝突の自動解決・ドリフトのヒールまで |
| `config.json` | Drive IDs・目標値・日付ウィンドウ。private リポにのみ存在 |
| `.backups/` | 旧構成の名残の退避先。新構成では正本が git 管理なので実質不要 |

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

**ここで一品でも「何かわからない」ものが残ったら、先に進まずに本人に聞く。**

### Step 2: kcal と P/F/C を推定する

**日本食品標準成分表の値を基準にする。** 主要な食品は暗記に頼らず、
不確かなら `WebSearch` で「<食品名> 栄養成分 100g」を確認する。

外食チェーンは公表栄養値があればそれを最優先で使う。
`WebSearch` で「<店名> <メニュー名> カロリー 栄養成分」を引き、
見つからなければ同等メニューからの推定とし、必ず `memo` に「概算」と書く。

推定したら **P×4 + F×9 + C×4 が kcal とおおむね合うか**必ず検算する。
30%以上ずれていたらどこかを間違えている。`append_meal.py` も同じ検算をする。

調味料（油・ドレッシング・マヨネーズ・砂糖）は忘れやすいわりに脂質・糖質へ効くので、
使っていそうなら必ず一品として立てる。

推定できたら、品ごとに `confidence` を正直に付ける:

| 値 | いつ付けるか |
|---|---|
| `high` | 品名も分量もはっきりしていて、成分表か公表値で裏が取れる |
| `medium` | 品名は確かで、分量が目測。日常の記録はたいていこれ |
| `low` | 品名か分量に自信が無い。**追記は中断される。本人に確認すること** |

### Step 3: 追記前に `date` で今日を確認する

**JSON を組む前に必ず `date +%Y-%m-%d` を実行して西暦を確認する。**
過去に「ユーザーの言う 9/12」を内部時計の 2025 年で書き込み、日次集計に出ない事故が
起きている。日付ウィンドウ（過去180日/未来2日）が機械的に弾くようになったが、
スキル側でも最初に確認する。

### Step 4: JSON を組み立てて追記する

1品1オブジェクトの JSON 配列にする。同じ食事の品は `date` と `time` をそろえる
（同じ `date+time+type` が1つの records ファイルになる）。

```bash
cd ~/workspace/life/meal
date +%F   # ← 今日の日付を必ず確認
cat > /tmp/meal_input.json <<'JSON'
[
  {"date": "2026-09-14", "time": "12:30", "type": "昼食",
   "menu": "鶏むね肉（皮なし）", "amount": "200g",
   "kcal": 215, "p": 44.6, "f": 3.0, "c": 0.0, "memo": "写真から推定"},
  {"date": "2026-09-14", "time": "12:30", "type": "昼食",
   "menu": "白米", "amount": "150g",
   "kcal": 234, "p": 3.8, "f": 0.5, "c": 55.7}
]
JSON

# まず必ず --dry-run で検証する
uv run append_meal.py /tmp/meal_input.json --dry-run

# 問題なければ本適用（records/ への書き出し + xlsx 全再生成 + 再計算 + 検査）
uv run append_meal.py /tmp/meal_input.json
```

フィールド:

| キー | 必須 | 内容 |
|---|---|---|
| `date` | ✅ | `YYYY-MM-DD`。**組む前に `date` コマンドで今年を確認** |
| `menu` | ✅ | 品名 |
| `time` | | `HH:MM`。不明なら朝 08:00 / 昼 12:30 / 夜 19:00 を仮置きし memo に断る |
| `type` | | 朝食 / 昼食 / 夕食 / 間食 / 飲み物 のいずれか |
| `amount` | | 「200g」「1杯」など |
| `kcal` `p` `f` `c` | | 数値。省略すると 0。全部 0 だと弾かれる |
| `confidence` | | `high` / `medium` / `low`。省略すると `medium` |
| `memo` | | 推定の根拠、概算である旨、シェアした旨など |

`append_meal.py` がやること:

- 内容が特定できていない記録を弾く（曖昧なメニュー名 / 全ゼロ / `low` / PFC矛盾 / 年号）
- 既存 records との重複（同日・同時刻・同メニュー）を検出して中断
- 1食事を `records/YYYYMMDD_HHMM_<type>.json` に書き出す（既にあれば `--edit` でマージ。**1品だけ直しても他の品目は消えない**）
- records/ 全体を再検証し、落ちたら書いたファイルを巻き戻す
- meal_log.xlsx を records/ から全再生成し、LibreOffice で再計算し、全体を検査する
- 追記した日の合計を JSON で標準出力に出す

中断したときは records/ も meal_log.xlsx も変わっていない。安心して原因を直してよい。

### Step 5: Drive と GitHub に反映する

```bash
cd ~/workspace/life/meal
./sync_meal.sh "meal: 2026-09-14 の食事を記録"
```

`sync_meal.sh` がこの順で守る。

1. `check_meal.py` を通す（正本の健全性 + ブックとの一致）。落ちたら Drive も git も触らない
2. `git pull --rebase` する。records/ の JSON は行マージされ、
   `meal_log.xlsx` が衝突したら **records/ を正として rebuild して自動解決**
3. rebase 後、xlsx が正本とズレていたら（黙ズレ）**自動で rebuild してヒール**
4. アップロード前に、Drive のフォルダ内の `meal_log.xlsx` が1個だけで、
   実体IDが `config.json` の `drive_file_id` と一致することを確かめる
5. `rclone copy` で同じファイルを上書きする
6. アップロード後にもう一度IDを確かめる。**変わっていたら失敗させる**（URL が変わったということ）
7. commit & push（pushは再び拒否されない限り成功する）

**`rclone` を手で叩かない。** 部分実行:

```bash
./sync_meal.sh --drive-only    # Drive だけ
./sync_meal.sh --git-only      # git だけ
./sync_meal.sh --no-push       # commit まで
```

### Step 6: Slack に返す

`append_meal.py` の出力からその日の合計を読み取り、次の形で短く返す。

```
2026-09-14（月）を記録しました
  昼食  鶏むね肉200g / 白米150g
  合計  449 kcal ・ P 48.4g ・ F 3.5g ・ C 55.7g
  目標比 kcal -1,551 / P -71.6g
分量は写真からの目測なので、数値は概算です。
Drive（同じURL）と life リポジトリに反映しました。
```

推定の不確かさは必ず明示する。数字を断定しない。
中断したときも、何が足りなくて止まったかをそのまま伝えて聞き返す。

## 修正・削除・事故のとき

**一番多い「前の食事が消えた」の正体は xlsx の手編集か push 衝突。新構成では両方とも
機械が守る。それでも何かおかしいと思ったら:**

```bash
# ① 正本とブックの整合を見る（ズレはここで見つかる）
uv run check_meal.py

# ② 何かおかしければ、全部 records/ から作り直す（安全。いつでも実行してよい）
uv run build_meal_log.py

# ③ それでもダメなら、正本（records/）を git で確認。diff は読める形式になっている
git -C ~/workspace/life log --oneline -5 -- meal/records/
git -C ~/workspace/life diff HEAD -- meal/records/
```

- **品目の修正**: `records/*.json` を直接編集 → `uv run build_meal_log.py`
- **品目の削除**: `records/*.json` からその品目を消す → `uv run build_meal_log.py`
- **食事ごと削除**: `records/20260912_1900_dinner.json` を消す → `uv run build_meal_log.py`
- **--edit で1品だけ直す**: `uv run append_meal.py fix.json --edit`
  （マージ動作。入力に無い品目は必ず残る。**消すときは JSON を直接編集**）

## 絶対に避けること

- ❌ **meal_log.xlsx のセルを手で直さない** — 次の build で上書きされて消える。直すのは records/
- ❌ **Drive で新しいファイルを作らない** — 消して作り直す、別名で上げる、`rclone` を手で叩く。どれもURLが変わる
- ❌ **わからない食事を推測で埋めない** — 中断されたら値をでっち上げて再実行せず、本人に聞く
- ❌ `--allow-uncertain` `--allow-zero` `--allow-duplicates` を「通すため」に使わない — 本人に確認が取れたときだけ
- ❌ `config.json` の中身（Drive IDs）を skills リポジトリに書かない — public repo
- ❌ `pip install` を使わない — NixOS。Python は `uv run` 経由のみ
- ❌ 推定値を「正確な値」として提示しない — 目測の分量に基づく概算である旨を必ず添える
- ❌ 日付を組む前に `date` を確認しない — 年号ミスは窓ガードで弾かれるが、スキル側でも最初に確認する
- ❌ 記録が消えたと思って git の歴史を書き換える — 正本（records/）は git にある。`git log` / `git diff` で追えば必ず残っている

## トラブルシューティング

**追記が「年号の可能性」で弾かれた**
それが正しい挙動。`date +%F` で今日を確認し、正しい年で組み直す。
どうしても過去180日より前を記録したい（遡って入れる）ときは、
`config.json` の `date_window.past_days` を一時的に広げて、終わったら戻す。

**`soffice が見つからない` と出る**
再計算だけスキップされる。数式自体は Excel / Google スプレッドシートで開けば計算されるので
致命的ではない。恒久対応は NixOS の設定に `libreoffice-fresh` を追加すること。
暫定なら `nix build --out-link ~/.local/state/nix/gcroots/libreoffice nixpkgs#libreoffice-fresh`。

**`rclone remote 'gdrive:' が未設定`**
`rclone listremotes` で確認する。再設定は `rclone config`。

**git push が拒否される**
`sync_meal.sh` が rebase と衝突解決をやるはずなので、まず普通に再実行する。
records/*.json がコンフリクトしている場合はメッセージに従って手でマージする
（JSON なので行単位で解決できる）。`gh auth status` で認証確認。

**xlsx が開けない・壊れた**
`uv run build_meal_log.py`。正本（records/）が無事なら全部戻る。

**追記したのに日次シートに出ない**
`uv run check_meal.py` でドリフトを確認する。ズレていれば build で直る。
記録の年がずれていた場合は日付ウィンドウがそもそも弾くはず（弾かずに入った旧データが
疑われるときは、`records/` のファイル名と中身の `date` を見比べる）。

**グラフにデータが表示されない / バーが左端に潰れて見えない**
build はグラフ範囲を「実際にデータがある最終日付まで」に絞る
（`rebuild_all_charts(wb, max_date=...)`）。壊れた古いブックを見ているなら
`uv run build_meal_log.py` で作り直せば直る。

## 完了確認

- [ ] 特定できない品を推測で埋めていない（残っていたなら聞き返して保留にした）
- [ ] JSON を組む前に `date` で今日の年を確認した
- [ ] `append_meal.py` が正常終了し、records/ に食事ファイルが増えている
- [ ] `check_meal.py` が「完全一致」で通っている
- [ ] `sync_meal.sh` が「同じ URL のまま（ID ...）」と出した
- [ ] その日の合計が想定の範囲に収まっている（極端な値は分量の見積もりミス）
- [ ] life リポジトリに commit が積まれ push されている
- [ ] Slack に合計と、概算である旨を返した