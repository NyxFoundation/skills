# リポジトリの制作・改訂手順

## 入口と正本

リポジトリは `https://github.com/NyxFoundation/demo-creator`。
既存のローカル配置を使い、Makefileと実際のスクリプトを確かめる。以下はリポジトリのルートで実行する。

| 場所 | 役割 |
|---|---|
| `out/NAME/NAME.yaml` | 作業用の台本。文言・場面・保持時間 |
| `out/NAME/notes.md` | 出典・保証範囲・設計判断 |
| `out/NAME/layers/SHOT.yaml` | 3D化する場面と透過PNGの選択。sceneは0始まり |
| `out/NAME/shots/SHOT.py` | Blenderのシーン・カメラ・モーション |
| `out/NAME/build/` | HTML、録画、部品画像、3D、MLT、MP4。Git管理外 |
| `examples/NAME/` | 再利用用に保存したソース一式 |
| `engine/scenes/` | 場面の型と動き。共通エンジンを変えると再録画範囲が広がる |

ユーザーが `examples/` を添削していたら、その差分を作業用台本へ先に反映する。
`make example` は作業用から例へ同期し、削除も反映する。最新の添削が例に残っていないか確認してから実行する。
修正箇所を機械的に上書きしない。

## 新規制作

```sh
make new N=demo
# 既存例の構造を使う場合のみ:
# make new N=demo FROM=nyxis
make edit N=demo
```

台本の型はリポジトリの `docs/scenes.md` を参照する。
`card` は大きな文字と数字、`incident` は原因と結果の比較、`policy` はビルドのパスとフェイル、
`kernel` は3D映像と生成前の概形表示。既存例の実装はNyxis向けなので、別の製品の主張に合わせて内容を直す。

Makefileの `N` は主に編集・作成・例の保存に使う。`make html` / `make screens` / `make` は
複数の `out/` があると全デモを対象にする。1本だけ処理する場合は明示的なターゲットを使う。

```sh
make out/demo/build/page.html
make out/demo/build/screens/index.json
make out/demo/build/demo.mp4
```

Nix環境ではMakefileが必要に応じてdev shellを使う。Pythonは `uv run` を使う。
`make clean` は全デモのbuildを消すので、通常の改訂の出発点にしない。

## 文言とテンポの改訂

1. 台本と関係する型を読む。YAML以外に直書きの字幕がある場合もある。
2. 文言を短く整え、HTMLをビルドする。
3. `tools/snap.py` で静止画を出すか、ブラウザで狙った場面を止めて確認する。
4. レイアウトと動きを確認し、MP4を書き出す。

```sh
uv run --with playwright python3 tools/snap.py out/demo/build/page.html --out out/demo/build/snaps
```

ブラウザの `?rec=1&autoplay=0` はコントロールと自動再生を止めた確認用。
コンソールの `D.playScene(i)` は1場面、`D.replay()` は全編を再生する。
Playwrightで開始する場合は `(i) => { void D.playScene(i); }` のように起動し、
Promiseをawaitせずポーリングしながら `body.dataset.done` を待つ。

| 調整するもの | 設定 |
|---|---|
| 文字カードの表示時間 | `hold`（秒）。未指定ならreadingから計算 |
| 数字が着地する時間 | `count_ms`（ミリ秒） |
| 比較画面の待ち | incidentの `timing.settle / request / reveal` |
| 入力と判定 | policyの `timing.line / prepare / build / pass / fail` |
| 場面間の溶かし | トップレベルの `transition.duration`（秒） |
| 3Dの実際の再生時間 | `duration / speed`。speedの既定は1 |

各型で有効な設定は実装を優先する。readingを変えても、明示したholdや型固有のtimingは変わらない。
再ビルドや修正の往復を紹介する必要がなければ、パスとフェイルだけで終える。

## 3Dを作る・直す

```sh
make out/demo/build/parts/kernel/layers.json
make out/demo/build/3d/kernel.blend
make out/demo/build/3d/kernel.mp4
make out/demo/build/demo.mp4
```

通常の `make` は3Dを再描画しない。部品・形状・字幕を変えたときは3D側の更新も必要。
別のショット名を使う場合は、ターゲットとHTML側の動画パスを揃える。

- レイヤーPNGの座標と寸法は `layers.json` にある。DPRを上げたPNGの実ピクセル数とCSS寸法を混同しない。
- 要素のスクリーンショットには重なる別要素も写る。不要な図やノードを隠してから文字レイヤーを撮る。
- 字幕数を変えたら、layersの列挙、表示時刻、HTMLの概形表示も揃える。
- 形とカメラを変える場合は、代表フレームで全体像・注目箇所・終盤を確認してから全フレームを描画する。
- ラベルや字幕は、グロー・被写界深度の後に合成すると読みやすい。
- 画像は `.blend` にパックし、保存し直したファイルからも確認する。

### 文言だけの差し替え

重い3Dを再描画する前に、見出しや字幕が独立レイヤーか調べる。
既存フレームへ新しい画像を重ねる場合、古い文字を確実に消せる背景領域があり、
図形・光・動きにかぶらないことを確認する。透過文字を重ねるだけでは旧文言が残る。
背景を復元できない部分は元のシーンから再描画する。

対応できる場合は、旧フレームを退避し、メタデータの寸法に縮尺を合わせてFFmpegで合成する。
Nyxisのheaderは背景を含むレイヤー。合成の形は次の通りで、座標と寸法は実際のlayers.jsonから読む。

```text
[1:v]scale=WIDTH:HEIGHT,format=rgba[title];
[0:v][title]overlay=x=X:y=Y:format=rgb[v]
```

合成後のPNGからMP4をエンコードし、HTML、編集用Blender、保存用ソースにも同じ文言を反映する。
短い版へ変更するときは、旧連番を退避して空の出力先に描画するか、エンコーダに最終フレーム数を指定する。
前の長い版の末尾フレームを拾わないようにする。
部分再描画では `scene.frame_start` を変更せず、`frame_set` で必要なフレームを指定する。

## 接合部の技術的な不変条件

- ブラウザは前画面を保持してから次を準備する。動画のフレーム保持が取れているかを見る。
- MLTではproducerのinとplaylist entryのinに同じトリムを二重適用しない。
- `edit/dissolve.py` の短いブリッジクリップがMLTとKdenliveに共通の接合部になる。
- ChromiumとBlenderでは画素のレンジが異なる。色域・レンジ指定を変えたら境目の明るさを実映像で比較する。
- 異なる見た目のカットだけでなく、関連する内容の切替も同じ状態の数・字幕・順番になっているか確認する。

## 完了の確認

```sh
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate,nb_frames,duration -of json out/demo/build/demo.mp4
ffmpeg -v error -i out/demo/build/demo.mp4 -f null -
```

ブラウザのJSエラー、最後までの再生、意図したパス／フェイルの回数、字幕、接合部、最終フレームを確認する。
3Dの概形表示を、Blender版の出力確認の代わりにしない。
変更に応じた確認が通ったら、同じ検査を理由なく繰り返さず受け渡す。
保存用の例を更新する場合のみ、ユーザーの添削との差分を確認して次を実行する。

```sh
make example N=demo
```

pushや公開は依頼された対象だけに行う。`out/`、動画、PNG連番、認証情報をGitへ加えない。
