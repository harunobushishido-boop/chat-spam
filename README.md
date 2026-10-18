# Chat Spam｜リアルタイムニュース速報弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** のニュース速報ティッカーです。天気予報ではなく、日本語のニュース見出しを取得して右から左へ流します。

## 表示する内容

- 日本語ニュースの最新見出し
- 各記事の時刻・配信元ドメイン・元記事リンク
- 新着記事を取得して、5分ごとに自動更新
- ニュースが取得できない場合は前回の見出しを維持し、再取得を試行
- マウスを弾幕に重ねるとスクロールを一時停止

情報源はGDELT DOC APIです。日本語として分類されたニュース記事を過去6時間から検索し、公開時刻の新しい順に並べます。ニュースの速報性や更新タイミングは元の報道機関とGDELT側の収集状況に依存するため、5分ごとの更新は「ページがAPIを確認する間隔」であり、すべてのニュースが必ず5分以内に掲載されることを保証するものではありません。重大な緊急速報・避難情報は、自治体や公的機関の公式発表も確認してください。

## GitHub Pages で公開

公開予定URL（GitHub Pagesの初回設定後）：<https://harunobushishido-boop.github.io/chat-spam/>

初回公開時は、リポジトリの [Settings → Pages](https://github.com/harunobushishido-boop/chat-spam/settings/pages) を開き、**Build and deployment → Source → GitHub Actions** を選択してください。その後、[Actions](https://github.com/harunobushishido-boop/chat-spam/actions) で公開ワークフローが成功していることを確認します。Pagesの初期設定がまだの場合、公開URLは動きません。

## OBSなどの配信ソフトで使う

1. 「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を入力します。
3. 幅を `1980`、高さを `50` に設定します。
4. 配信画面の下の隙間へ配置します。

ページの余白はなく、高さは常に50pxです。OBSのブラウザソースから閲覧するため、ブラウザーがインターネットに接続されている必要があります。

## ニュースAPI

- **GDELT DOC API：** <https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/>
- **APIエンドポイント：** `https://api.gdeltproject.org/api/v2/doc/doc`
- この構成ではAPIキーを設定せず、ブラウザーから直接取得します。
- GDELT DOC APIの出力はブラウザーから利用できるようCORSが設定されています。
- 取得条件：日本語（`sourcelang:japanese`）、直近6時間、公開日時の新しい順、最大50件を取得し、画面には重複を除いて最大30件を表示します。
- 更新間隔：5分

## ファイル

- `index.html`：1980×50pxのニュース速報弾幕
- `.github/workflows/pages.yml`：GitHub Pages自動デプロイ

## リポジトリの説明文案

日本語の最新ニュースを5分ごとに自動取得して流す、OBS向け1980×50pxニュース速報弾幕。記事時刻・配信元リンクを表示し、GitHub Pagesで公開。
