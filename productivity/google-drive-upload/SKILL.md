---
name: google-drive-upload
description: >
  API 権限が取れない Google Drive へ、ログイン済みの Chrome を CDP で操作してファイルを
  アップロードする回避策。OAuth スコープが下りない・サービスアカウントを共有フォルダに
  招待できない・rclone の設定が通らない場面で使う。「Drive にアップして」と言われて
  API 経路が塞がっているときの最後の手段。
tags: [google-drive, cdp, chrome-devtools, upload, workaround]
---

# SKILL: google-drive-upload (CDP 経由)

## いつ使うか

**先に API 経路を試すこと。** `rclone`（`~/.config/rclone/rclone.conf` に設定済み）や Drive API が
使えるならそちらが速くて壊れにくい。このスキルは、

- OAuth のスコープが組織ポリシーで下りない
- サービスアカウントを対象フォルダに招待できない
- 個人アカウントのブラウザセッションでしか到達できない共有ドライブ

といった、**ブラウザのログイン状態そのものが唯一の認証手段**になっている場合の回避策。

## 前提

リモートデバッグを有効にした Chrome が起動していて、Drive の対象フォルダを開いたタブがあること。

```bash
# Chrome をデバッグポート付きで起動
google-chrome --remote-debugging-port=9222 &

# タブ一覧から対象タブの id を取る
curl -s http://127.0.0.1:9222/json | grep -B3 'drive.google.com'
```

## 実行

```bash
node scripts/upload_drive_cdp.mjs <TAB_ID> <FILE>...
```

`scripts/cdp.mjs` が WebSocket で DevTools Protocol を喋る最小クライアント。
`upload_drive_cdp.mjs` は `Page.setInterceptFileChooserDialog` でファイル選択ダイアログを
横取りし、`DOM.setFileInputFiles` でパスを直接流し込む。ダイアログが GUI に出ないので
ヘッドレス相当で動く。

## 落とし穴

- **タブ id は再起動で変わる。** 毎回 `curl http://127.0.0.1:9222/json` で取り直す。
- アップロード完了の判定は DOM の状態を見ているだけなので、**大きいファイルでは
  `sleep` の待ちを伸ばす**必要がある。
- Drive の UI が変わると壊れる。壊れたら DOM セレクタを直すより、まず API 経路が
  開いていないか再確認するほうが早い。
- 認証済みブラウザを自動操作するため、**対象フォルダを間違えると他人の共有先に置く**。
  実行前にタブが開いているフォルダを必ず目視する。
