# jizen

学生向けHTML資料を Cloudflare Pages で公開するリポジトリです。

## 仕組み

1. `public/` 以下に HTML を置く（例: `public/materials/2026-10-07_lecture.html`）
2. `main` ブランチに push する
3. GitHub Actions が `scripts/build_site.py` で一覧ページ（`index.html`）を自動生成し、Cloudflare Pages にデプロイ
4. 学生には `https://<プロジェクト名>.pages.dev/` を共有（個別資料のURLを直接渡してもOK）

一覧ページのカードには各HTMLの `<title>` が使われます。`Day3 本題 - 副題` の形にすると、「Day3」がバッジ、「副題」が小さなラベルになります。一覧はファイル名の順（例: `jizen_day2.html` → `jizen_day3.html`）に並びます。

## 初回セットアップ（1回だけ）

### 1. Cloudflare Pages プロジェクトを作成
Cloudflare ダッシュボード → **Workers & Pages** → **Create** → **Pages** → **Upload assets（Direct Upload）** を選び、
プロジェクト名を `jizen` にして作成（中身は空のままでOK）。
※ 別名にした場合は、GitHub の Settings → Secrets and variables → Actions → **Variables** に `CF_PAGES_PROJECT` を追加。

### 2. API トークンを作成
Cloudflare → 右上のアイコン → **My Profile** → **API Tokens** → **Create Token** →
**Custom token** で権限 `Account` / `Cloudflare Pages` / `Edit` を付与して作成。

### 3. GitHub に Secrets を登録
リポジトリの **Settings → Secrets and variables → Actions → New repository secret**:

| 名前 | 値 |
|---|---|
| `CLOUDFLARE_API_TOKEN` | 手順2のトークン |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare ダッシュボード右側（またはURL）に表示される Account ID |

### 4. デプロイ
`main` に push するか、Actions タブの「Deploy to Cloudflare Pages」から **Run workflow**。

## 閲覧を学生に限定したい場合（任意）

Cloudflare **Zero Trust → Access → Applications** で `jizen.pages.dev` を保護対象に追加し、
ポリシーを「Emails ending in `@i-u.ac.jp`」にすると、大学メールでワンタイムコード認証した人だけが閲覧できます（50ユーザーまで無料）。
全ページに `noindex` を入れておくと検索エンジンにも載りにくくなります。

## ローカル確認

```sh
python3 scripts/build_site.py
python3 -m http.server -d dist 8000
```
