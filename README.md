# Chat Spam｜全国の天気ニュース弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** の天気ニュース・ティッカーです。仙台市だけでなく、北海道から沖縄まで全国12都市の現在の天気と予報をまとめ、ニュース見出し風に右から左へ流します。

## 表示する内容

- 全国12都市の現在の天気・気温
- 各都市の今日の予想最高気温・最低気温・降水確率
- 全国の雨・雪の地点数、降水確率40%以上の都市数
- 予想最高気温・最低気温の都市
- 10分ごとの自動更新と最終データ時刻
- 天気の状況に応じた強調表示

対象都市：札幌、青森、仙台、新潟、東京、名古屋、大阪、広島、高知、福岡、鹿児島、那覇。日本全国すべての地点ではなく、各地域の代表都市を使った全国概況です。

## GitHub Pages で公開

公開予定URL（GitHub Pagesの初回設定後）：<https://harunobushishido-boop.github.io/chat-spam/>

初回公開時は、リポジトリの [Settings → Pages](https://github.com/harunobushishido-boop/chat-spam/settings/pages) を開き、**Build and deployment → Source → GitHub Actions** を選択してください。その後、[Actions](https://github.com/harunobushishido-boop/chat-spam/actions) で公開ワークフローが成功していることを確認します。Pagesの初期設定がまだの場合、公開URLは動きません。

## OBSなどの配信ソフトで使う

1. 「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を入力します。
3. 幅を `1980`、高さを `50` に設定します。
4. 配信画面の下の隙間へ配置します。

ページ自体に余白はなく、高さは常に50pxです。弾幕の上にマウスを置くとスクロールが一時停止します。

## 天気データ・自動更新

- API：<https://open-meteo.com/>
- APIキー不要
- 10分間隔で最新データを取得
- ネットワークエラー時は前回の表示を維持し、次回に再取得
- 日本時間（Asia/Tokyo）を使用

天気データはOpen-Meteoからブラウザーで取得します。全国概況は代表都市の予報に基づくもので、すべての市区町村の実況を示すものではありません。

## ファイル

- `index.html`：1980×50pxの全国天気ニュース弾幕
- `.github/workflows/pages.yml`：GitHub Pages自動デプロイ

## リポジトリの説明文案

全国12都市の最新天気をニュース形式で配信する、OBS向け1980×50px天気弾幕。気温・降水確率・地域別予報を10分ごとに自動更新。
