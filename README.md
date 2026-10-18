# Chat Spam｜ライブ配信向け天気予報弾幕

横 **1980 × 縦 50 ピクセル** の、ライブ配信画面の下の隙間に配置する天気予報ティッカーです。ブラウザーで最新データを取得し、現在の天気・気温・体感温度・湿度・降水量・風速と、今日から3日間の予報を右から左へ流して表示します。

## GitHub Pages

公開予定URL：<https://harunobushishido-boop.github.io/chat-spam/>

初回だけ、GitHubでリポジトリの **Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定してください。その後は `.github/workflows/pages.yml` が `main` への更新ごとに公開します。初回デプロイが完了するまでは公開URLでページが表示されない場合があります。

## 配信ソフトでの使い方

OBSなどでは「ブラウザソース」を追加し、次のように設定します。

- URL：<https://harunobushishido-boop.github.io/chat-spam/>
- 幅：`1980`
- 高さ：`50`

配信画面の下の隙間に配置してください。HTMLの高さは常に50pxです。背景は濃紺の半透明バーで、ページ全体の余白はありません。弾幕にマウスカーソルを重ねるとスクロールが一時停止します。

## 表示する地域を変更

URLに緯度・経度・地域名を付けると、表示地点を変更できます。

例：東京
```
https://harunobushishido-boop.github.io/chat-spam/?city=東京&lat=35.6812&lon=139.7671
```

デフォルトは仙台市です。地域名はURLエンコードが必要な場合があります。緯度・経度は10進数で指定してください。

## 天気データ・更新

- 天気データ：<https://open-meteo.com/>
- APIキーは不要です。
- ページ表示後、10分ごとに自動更新します。
- 取得できない場合はエラー表示に切り替え、次回の自動更新で再取得を試みます。
- ブラウザーがインターネットに接続されている必要があります。

天気データはOpen-Meteoからブラウザーで取得します。配信地域が仙台以外の場合は、上記URLの `city`、`lat`、`lon` を変更してください。

## ファイル

- `index.html`：50px固定高の天気弾幕ページ
- `.github/workflows/pages.yml`：GitHub Pagesへの自動デプロイ

## リポジトリの説明文案

横1980×縦50pxのライブ配信向け天気予報弾幕。Open-Meteoから現在の天気と3日間予報を取得し、GitHub Pagesで公開します。
