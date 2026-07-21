---
name: meishi
description: |
  名刺画像を受け取った際の自動登録フロー。Notion Business Card DB にテキスト情報と画像を登録する。
  トリガー: ユーザー入力に「meishi」が含まれる、または名刺画像が添付される。
version: 1.1.0
author: gohan
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [notion, business-card, ocr, workflow]
---

# 名刺登録フロー（meishi）

## トリガー条件
- ユーザーのメッセージに「meishi」が含まれる
- または名刺/ビジネスカード画像が添付される

## 対象データベース

**Business Card DB** に登録する。Database ID はハードコードせず
[`docs/nyx-directory.md`](../../docs/nyx-directory.md) の "Business Card DB" を参照する（以下では
`<business-card-db-id>` と表記）。Notion API key は各環境のセットアップで登録済み
（`~/.config/notion/api_key`）で、このリポには含めない。

## DBスキーマ

| プロパティ | 型 | 必須 |
|-----------|-----|------|
| Name | title | ✅ |
| Company | rich_text | 任意 |
| Company_EN | rich_text | 任意 |
| Department | rich_text | 任意 |
| Job | rich_text | 任意 |
| 担当メンバー | rich_text | 任意（交換した弊社担当者を記載） |
| Name_EN | rich_text | 任意 |
| Phone | phone_number | 任意 |
| Email | email | 任意 |
| URL | url | 任意 |
| When | date | 任意 |
| Status | status | 任意（デフォルト: 未連絡） |
| Memo | rich_text | 任意 |

## 実行手順

### Step 1: OCRで名刺テキストを抽出
```bash
# vision_analyze で名刺画像を読み取る
# プロンプト: "Extract all text from this business card accurately.
#  Return: name, organization, department, title, address, phone, fax, email."
```

### Step 2: Notion Business Card DBにページ作成
`<business-card-db-id>` は `docs/nyx-directory.md` の Business Card DB の値に置き換える:

```bash
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "<business-card-db-id>"},
    "properties": {
      "Name": {"title": [{"text": {"content": "[氏名]"}}]},
      "Company": {"rich_text": [{"text": {"content": "[会社名]"}}]},
      "Department": {"rich_text": [{"text": {"content": "[部署]"}}]},
      "Job": {"rich_text": [{"text": {"content": "[役職]"}}]},
      "担当メンバー": {"rich_text": [{"text": {"content": "[弊社担当者名]"}}]},
      "Phone": {"phone_number": "[電話番号]"},
      "Email": {"email": "[メールアドレス]"},
      "When": {"date": {"start": "YYYY-MM-DD"}},
      "Status": {"status": {"name": "未連絡"}},
      "Memo": {"rich_text": [{"text": {"content": "[住所/FAXなど]"}}]}
    }
  }'
```

### Step 3: 名刺画像を `ntn` CLI でアップロード
`{page_id}` は Step 2 で作成したページ。詳細は `notion-databases` スキル参照:

```bash
# 前提: npm install -g ntn / workspace_id は notion-databases スキル参照
UPLOAD_ID=$(NOTION_API_TOKEN=$(cat ~/.config/notion/api_key) \
  NOTION_WORKSPACE_ID=<workspace_id> \
  ~/.local/bin/ntn files create --plain < ./meishi.jpeg | cut -f1)

curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{"children":[{"object":"block","type":"image","image":{"type":"file_upload","file_upload":{"id":"'"$UPLOAD_ID"'"}}}]}'
```

## 絶対に避けること
- ❌ Scrapbox DB には名刺を登録しない — Business Card DB のみ使用（IDは `docs/nyx-directory.md` 参照）
- ❌ `POST /v1/file_uploads`→生PUT は失敗する — 画像アップロードは `ntn` CLI を使用
- ❌ Notion APIの `created_by` は変更不可 — Nyxのままで問題なし

## 完了確認
- [ ] Business Card DBにページが作成されている
- [ ] 画像がimage blockとしてページに添付されている
- [ ] ローカルにも画像バックアップを保存（`~/.hermes/workspace/`）
