# CLAUDE.md

## 概要

このリポジトリは、Pythonによる業務自動化スクリプト集です。Webスクレイピングの練習用スクリプトと、日次の市場レポート(株価・指数・仮想通貨等)を自動生成するスクリプトを管理しています。

## 使用技術

- **Python 3.14** (`.venv` による仮想環境)
- **requests / BeautifulSoup4**: 静的HTMLのスクレイピング ([scrape_books.py](scrape_books.py))
- **Playwright (Chromium)**: JavaScriptで描画されるページのスクレイピング ([scrape_quotes.py](scrape_quotes.py))
- **yfinance**: Yahoo Financeから株価・指数・仮想通貨・為替データを取得 ([market_report.py](market_report.py))
- **バッチファイル + Windowsタスクスケジューラ**: 定期実行 ([run_market_report.bat](run_market_report.bat))
- **Git/GitHub**: 生成レポートの自動コミット・プッシュ (`origin` = `hyper427/python-automation`)

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| [scrape_books.py](scrape_books.py) | books.toscrape.com から書籍タイトル・価格・在庫状況を取得し `books_〔日付〕.md` を生成 |
| [scrape_quotes.py](scrape_quotes.py) | quotes.toscrape.com/js から名言・著者を取得し `quotes_〔日付〕.md` とスクリーンショット `quotes_〔日付〕.png` を生成 |
| [market_report.py](market_report.py) | 指数・日本株・米国株・仮想通貨・為替等を取得し `market_report_〔日付〕.md` / `.html` / `index.html` を生成 |
| [run_market_report.bat](run_market_report.bat) | `.venv` を有効化して `market_report.py` を実行し、結果を `git add`→`commit`→`push`。ログを `log_market_report.txt` に追記 |
| `log_market_report.txt` | `run_market_report.bat` の実行ログ(追記式) |
| `index.html` | 最新の市場レポートHTML(`market_report_〔日付〕.html` と同内容、GitHub Pages等での公開を想定) |
| `.venv/` | Python仮想環境(Git管理外) |

## 注意事項

- **`.venv` はコミットしない**(`.venv/.gitignore` に `*` が自動生成されているため、ルートの `.gitignore` 追加は不要)
- **`^TOPX`(TOPIX)は常に取得失敗してスキップされる**: Yahoo Finance側でデータが提供されていないため(仕様通りの動作)
- **HYPEは `HYPE32196-USD` を使用**: `HYPE-USD` は無関係な別トークンを指すため
- **銘柄の日本語表示名は `market_report.py` の `NAME_OVERRIDES` で管理**: 新しい銘柄を追加する場合はここに追記する
- **yfinanceの `Ticker.info` は銘柄ごとにAPIリクエストが発生**: 全銘柄取得で約1〜2分かかる。レート制限を受けた場合は `REQUEST_INTERVAL` を増やす
- **`run_market_report.bat` は `git push` を含む**: タスクスケジューラから非対話実行するため、事前にGit Credential ManagerまたはSSH鍵で認証を済ませておく必要がある
- **Windowsのコンソールは既定でUTF-8ではない**ため、ログ出力(`log_market_report.txt`)内の日本語が文字化けして見える場合がある。ファイル自体はUTF-8で保存されているため、エディタ等で開けば正しく表示される
