# Chat Spam｜リアルタイムニュース速報弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** のニュース速報ティッカーです。日本語のニュース見出し、掲載時刻、配信元ドメインを右から左へ流します。

## 表示する内容

- 日本語ニュースの新しい見出しと記事リンク
- 掲載時刻と配信元
- 5分ごとの自動更新
- 取得失敗時の別クエリによる再試行
- 初回取得に失敗した場合は20秒後に再試行
- 取得失敗中は前回のニュースを維持
- マウスを弾幕に重ねるとスクロールを一時停止

## ニュースAPI

GDELT DOC APIを使い、APIキーなしでニュース記事の一覧を取得します。

- 公式ドキュメント：<https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/>
- API URL：`https://api.gdeltproject.org/api/v2/doc/doc`
- ブラウザーのクロスオリジン制限を避けるため、APIが対応するJSONP方式で取得します。
- 最初の検索で記事が返らない場合は、短い時間範囲で日本語配信元のニュースを再検索します。
- 5分ごとの確認はAPIへの問い合わせ間隔です。報道機関による掲載直後に必ず反映されることまでは保証されません。
- 速報の信頼性が重要な場合は、ニュース配信元・公的機関の元記事も確認してください。

## GitHub Pagesで公開

公開予定URL（GitHub Pagesの初回設定後）：<https://harunobushishido-boop.github.io/chat-spam/>

初回公開時は、リポジトリの [Settings → Pages](https://github.com/harunobushishido-boop/chat-spam/settings/pages) を開き、**Build and deployment → Source → GitHub Actions** を選択してください。その後、[Actions](https://github.com/harunobushishido-boop/chat-spam/actions) で公開ワークフローが成功していることを確認します。Pagesの初期設定がまだの場合、公開URLは動きません。

## OBSなどの配信ソフトで使う

1. 「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を入力します。
3. 幅を `1980`、高さを `50` に設定します。
4. 配信画面の下の隙間へ配置します。

HTML自体の高さは常に50pxです。ブラウザソースにインターネット接続が必要です。

## リポジトリの説明文案

日本語の最新ニュースを5分ごとに自動取得して流す、OBS向け1980×50pxニュース速報弾幕。記事時刻・配信元リンクを表示し、GitHub Pagesで公開。
