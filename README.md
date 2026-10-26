# シレン6 値段識別

風来のシレン6で、店で見た売値・買値から未識別アイテム（巻物・草と種・腕輪・杖・壺）の候補を絞り込むWebアプリです。判断が済んだアイテムを「判断完了」にすると、以後の候補から外れます。判断済みの状態はブラウザの localStorage に保存されます。

## 構成

| パス | 内容 |
| --- | --- |
| `public/index.html` | 公開する単一HTML。データとフォント（サブセット）を内蔵 |
| `wrangler.jsonc` | Cloudflare Workers（静的アセット配信）の設定 |
| `tools/` | データ取得・HTML生成用のスクリプト |
| `licenses/` | 同梱フォントのライセンス |

## Cloudflare Workersへのデプロイ

### GitHub連携（自動デプロイ）

1. Cloudflareダッシュボードで Workers & Pages → Create → Import a repository を選びます。
2. このリポジトリを選び、ビルドコマンドは空、デプロイコマンドは `npx wrangler deploy` のままにします。
3. `main` へのpushごとに自動で公開されます。

### カスタムドメイン

ドメインのDNSがCloudflareで管理されている場合、ダッシュボードの Workers & Pages → 対象のWorker → Settings → Domains & Routes → Add → Custom domain で追加できます。設定ファイルで管理する場合は `wrangler.jsonc` に次を追加します。

```jsonc
"routes": [{ "pattern": "shiren.example.com", "custom_domain": true }]
```

### 手元から直接デプロイ

```sh
npx wrangler deploy
```

## データの更新手順

価格は [風来のシレン6 とぐろ島探検録 Wiki「値段一覧表」](https://shiren6.game-info.wiki/d/%c3%cd%c3%ca%b0%ec%cd%f7%c9%bd)（取得時点の最終更新 2025年12月25日）から取得しています。

```sh
pip install fonttools brotli
cd tools
./fetch.sh                        # price.utf8.html を取得
python3 build_data.py             # items.json を生成
LINESEED_DIR=/path/to/fonts/ python3 assemble.py   # ../public/index.html を生成
```

`LINESEED_DIR` には `LINESeedJP-Regular.woff2` と `LINESeedJP-Bold.woff2` を置いたディレクトリを指定します。

## ライセンス

フォントの LINE Seed JP は SIL Open Font License 1.1 です。ライセンス全文は `licenses/LINESeedJP-OFL.txt` にあります。
