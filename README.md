# Chat Spam｜GitHub自動更新・ニュース速報弾幕

ライブ配信の下の隙間に配置する、横 **1980 × 縦 50 ピクセル** のニュース速報ティッカーです。ニュースの取得はGitHub Actions側で行い、生成された `news.json` をGitHub Pagesから配信します。弾幕にはニュースの掲載時刻と見出しだけを表示し、Yahoo!ニュースなどの出典元・配信元の名前は表示しません。OBSのブラウザーはニュースAPIへ直接接続しないため、ブラウザー側のCORS制限の影響を受けにくい構成です。

## 仕組み

1. GitHub Actionsが **5分ごと** に起動し、ニュース取得スクリプトを実行します。
2. **GDELT DOC API** と複数の **Google News RSS** を並行して確認します。
3. 取得できた記事を重複除去し、新しい順に並べて `news.json` を生成します。
4. GitHub PagesへHTMLとJSONを公開します。
5. 配信画面は公開済みの `news.json` を60秒ごとに確認します。

GitHub Actionsのスケジュールは5分間隔を指定していますが、GitHub側の負荷によって起動や公開が遅れる場合があります。毎分・秒単位の厳密なリアルタイム配信を保証するものではありません。

## 取得できない場合

- 複数のニュース取得元に並行してアクセスします。
- 全ての取得元が失敗した場合、直前に公開したニュースデータを読み込み、前回の見出しを維持します。
- 前回データもない初回はエラー状態のJSONを生成しますが、次のスケジュールで再度取得を試します。
- 取得失敗時は弾幕に「ニュース更新に失敗・前回データを表示中」と表示します。
- 外部ニュースサービスの障害やGitHub Actionsの遅延時には更新が遅れることがあります。

## ニュース取得元

- [GDELT DOC API](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- [Google News 日本版 RSS](https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja)

## GitHub Pages

公開URL：<https://harunobushishido-boop.github.io/chat-spam/>

- [ニュース速報弾幕のHTML](https://github.com/harunobushishido-boop/chat-spam/blob/main/index.html)
- [サーバー側ニュース取得スクリプト](https://github.com/harunobushishido-boop/chat-spam/blob/main/scripts/fetch_news.py)
- [5分ごとの取得と公開ワークフロー](https://github.com/harunobushishido-boop/chat-spam/blob/main/.github/workflows/pages.yml)
- [GitHub Actionsの実行履歴](https://github.com/harunobushishido-boop/chat-spam/actions)

## OBSなどの配信ソフトで使う

1. OBSで「ブラウザソース」を追加します。
2. URLに <https://harunobushishido-boop.github.io/chat-spam/> を設定します。
3. 幅を `1980`、高さを `50` にします。
4. 配信画面の下の隙間に配置します。

## リポジトリの説明文案

GitHub Actionsで日本語ニュースを5分ごとに自動取得し、GitHub Pagesで配信するOBS向け1980×50pxニュース速報弾幕。
