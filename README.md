# Chat Spam｜リアルタイムニュース速報弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** のニュース速報ティッカーです。天気予報ではなく、日本語のニュース見出し・記事の掲載時刻・配信元を右から左へ流します。

## ニュースの取得方法

1. **GDELT DOC API** を最初に利用し、日本語のニュースをJSONPで取得します。
2. GDELTから記事を取得できない場合は、**Google News RSS**を別経路（RSSプロキシ）で取得します。
3. どちらも失敗した場合は取得エラーを表示し、20秒後に再試行します。前回のニュースがある場合は、更新に失敗しても表示を維持します。

- 5分ごとにニュースの更新を確認します。
- 弾幕には記事の掲載時刻（日本時間）、見出し、配信元、元記事リンクを表示します。
- 更新間隔は確認間隔であり、報道機関の掲載直後に反映されることを保証するものではありません。
- 外部APIやRSSプロキシの障害・利用制限・通信環境によって取得できない場合があります。

## GitHub Pages

公開URL：<https://harunobushishido-boop.github.io/chat-spam/>

公開処理は `main` ブランチの更新時に GitHub Actions が実行します。[Actionsの実行状況](https://github.com/harunobushishido-boop/chat-spam/actions)

## OBSなどの配信ソフトで使う

1. OBSで「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を入力します。
3. 幅を `1980`、高さを `50` に設定します。
4. 配信画面の下の隙間に配置します。

弾幕の高さは常に50pxです。配信ソフトが前の内容をキャッシュしている場合は、ブラウザソースを再読み込みしてください。

## ニュースの情報源

- [GDELT DOC API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- [Google News 日本版 RSS](https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja)

## リポジトリの説明文案

日本語の最新ニュースを5分ごとに自動取得して流す、OBS向け1980×50pxニュース速報弾幕。GDELTとGoogle News RSSに対応。
