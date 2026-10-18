# Chat Spam｜リアルタイムニュース速報弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** のニュース速報ティッカーです。日本語のニュース見出し、掲載時刻、配信元を右から左へ流します。

## ニュース取得と予備ルート

ニュースデータが1つのサービスで取得できない場合に備え、取得経路を複数用意しています。

1. **GDELT DOC API**：JSONPでニュース記事を取得
2. **Google News RSS**：GDELTが失敗した場合にRSSを取得
3. **予備のRSSプロキシ**：Google News RSSの1つ目の取得経路も失敗したときに再試行

- 5分ごとにニュースAPIを確認します。
- 最初の取得が失敗した場合は20秒後に自動再試行します。
- 取得に失敗しても前回のニュースを消さず、再取得を試みます。
- プロキシを含む外部サービスは、障害や利用制限によって一時的に取得できない場合があります。
- 「5分ごとに更新」は確認間隔であり、ニュース掲載直後の反映を保証するものではありません。

## GitHub Pagesで公開

公開予定URL（GitHub Pagesの初回設定後）：<https://harunobushishido-boop.github.io/chat-spam/>

初回公開時は、リポジトリの [Settings → Pages](https://github.com/harunobushishido-boop/chat-spam/settings/pages) を開き、**Build and deployment → Source → GitHub Actions** を選択してください。その後、[Actions](https://github.com/harunobushishido-boop/chat-spam/actions) で公開ワークフローが成功していることを確認します。Pagesの初期設定がまだの場合、公開URLは動きません。

## OBSなどの配信ソフトで使う

1. 「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を入力します。
3. 幅を `1980`、高さを `50` に設定します。
4. 配信画面の下の隙間へ配置します。

HTML自体の高さは常に50pxです。ブラウザソースにはインターネット接続が必要です。

## API・情報源の公式ページ

- GDELT DOC API：<https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/>
- Google News RSS：<https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja>

## リポジトリの説明文案

日本語の最新ニュースを複数の取得経路で配信する、OBS向け1980×50pxニュース速報弾幕。GDELTとGoogle News RSSを利用し、5分ごとに自動更新。
