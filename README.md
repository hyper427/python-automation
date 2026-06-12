# python-automation

## 概要

日経平均・米国株・仮想通貨・為替などの主要銘柄をYahoo Financeから取得し、日次の市場レポートをMarkdownとHTMLダッシュボードで自動生成するツールです。あわせて、Webスクレイピングの練習用スクリプト(書籍サイト・名言サイト)も含まれています。

## 必要な環境

- Windows
- Python 3.14 (3.10以降推奨)
- 必要なライブラリ
  - `requests`
  - `beautifulsoup4`
  - `playwright`(+ Chromiumブラウザ)
  - `yfinance`

## セットアップ手順

```powershell
cd C:\Users\user\Desktop\python-automation

# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
.venv\Scripts\activate

# 必要ライブラリのインストール
pip install requests beautifulsoup4 playwright yfinance

# Playwright用ブラウザ(Chromium)のインストール
python -m playwright install chromium
```

## 実行方法

仮想環境を有効化した状態で、各スクリプトを実行します。

```powershell
.venv\Scripts\activate

# 書籍スクレイピング(books.toscrape.com) -> books_〔日付〕.md
python scrape_books.py

# 名言スクレイピング(quotes.toscrape.com/js, Playwright) -> quotes_〔日付〕.md / .png
python scrape_quotes.py

# 市場レポート生成 -> market_report_〔日付〕.md / .html / index.html
python market_report.py
```

## 自動実行の設定方法(タスクスケジューラ)

[run_market_report.bat](run_market_report.bat) が `.venv` の有効化 → `market_report.py` 実行 → `git add` / `commit` / `push` → ログ追記までを自動実行します。

1. `Win + R` → `taskschd.msc` でタスクスケジューラを開く
2. 「操作」→「タスクの作成」
3. **「全般」タブ**
   - 名前: `MarketReport`
   - 「ユーザーがログオンしているかどうかにかかわらず実行する」を選択
   - 「最上位の特権で実行する」にチェック
4. **「トリガー」タブ**(2つ作成)
   - 新規 → 「毎日」→ 開始時刻 `6:00:00`
   - 新規 → 「毎日」→ 開始時刻 `16:00:00`
5. **「操作」タブ**
   - 「新規」→「プログラムの開始」
   - プログラム/スクリプト: `C:\Users\user\Desktop\python-automation\run_market_report.bat`
   - 開始(オプション): `C:\Users\user\Desktop\python-automation`
6. 保存してパスワードを入力

> **事前準備**: `git push` を非対話で実行するため、Git Credential ManagerまたはSSH鍵で認証情報をキャッシュ/設定しておく必要があります。

## 取得できる銘柄一覧

### 📊 指数サマリー
| ティッカー | 名称 |
| --- | --- |
| ^N225 | 日経平均株価 |
| ^TOPX | TOPIX ※現在Yahoo Finance側でデータ未提供のため常にスキップ |
| ^IXIC | NASDAQ総合指数 |
| ^DJI | NYダウ |
| ^GSPC | S&P500 |
| ^SOX | SOX指数(フィラデルフィア半導体) |

### 🇯🇵 日本株(49銘柄)
| コード | 名称 | コード | 名称 |
| --- | --- | --- | --- |
| 7011 | 三菱重工業 | 6098 | リクルートホールディングス |
| 7744 | ノーリツ鋼機 | 6501 | 日立製作所 |
| 7777 | スリー・ディー・マトリックス | 6758 | ソニーグループ |
| 6721 | ウインテスト | 6861 | キーエンス |
| 1407 | ウエストホールディングス | 6954 | ファナック |
| 3823 | WHY HOW DO | 6981 | 村田製作所 |
| 3777 | 環境フレンドリー | 7203 | トヨタ自動車 |
| 2134 | キタハマキャピタル | 7267 | 本田技研工業 |
| 3070 | ジェリービーンズ | 7751 | キヤノン |
| 8894 | REVOLUTION | 7974 | 任天堂 |
| 5016 | JX金属 | 8031 | 三井物産 |
| 7012 | 川崎重工業 | 8058 | 三菱商事 |
| 5451 | 淀川製鋼所 | 8306 | 三菱UFJフィナンシャル・グループ |
| 5803 | フジクラ | 8316 | 三井住友フィナンシャルグループ |
| 285A | キオクシアHD | 8411 | みずほフィナンシャルグループ |
| 8267 | イオン | 8766 | 東京海上ホールディングス |
| 4661 | OLC | 8802 | 三菱地所 |
| 8729 | ソニーFG | 9432 | 日本電信電話 |
| 8107 | キムラタン | 9984 | ソフトバンクグループ |
| 7148 | FPG | | |
| 2914 | 日本たばこ産業 | | |
| 5401 | 日本製鉄 | | |
| 3350 | メタプラネット | | |
| 5838 | 楽天銀行 | | |
| 4755 | 楽天グループ | | |
| 4063 | 信越化学工業 | | |
| 4452 | 花王 | | |
| 4502 | 武田薬品工業 | | |
| 4503 | アステラス製薬 | | |
| 4568 | 第一三共 | | |

### 🇺🇸 米国株(28銘柄)
| ティッカー | 名称 | ティッカー | 名称 |
| --- | --- | --- | --- |
| TSLA | テスラ | INDI | インディセミコンダクタ |
| COIN | コインベース | MU | マイクロン |
| TLT | iシェアーズ米国国債20年 | OKLO | オクロ |
| HOOD | ロビンフッド | POET | ポエットテクノロジーズ |
| QS | クアンタムスケープ | SNDK | サンディスク |
| RIOT | ライオットプラットフォームズ | ZS | Zスケーラー |
| MARA | マラホールディングス | APH | アンフェノール |
| MO | アルトリア | AAOI | アプライドオプトエレクトロニクス |
| CRWV | コアウィーブ | VRT | バーティブホールディングス |
| MSTR | ストラテジー | ALAB | アステラボ |
| NBIS | ネビウスグループ | COHR | コヒレント |
| ONDS | オンダスインク | HYPD | ハイペリオンDeFi |
| INOD | イノデータ | | |
| BMNR | ビットマインイマージョン | | |
| NVDA | エヌビディア | | |
| AMSC | アメリカンスーパーコンダクター | | |

### 💰 仮想通貨
| ティッカー | 名称 |
| --- | --- |
| BTC-USD | Bitcoin USD |
| HYPE32196-USD | Hyperliquid USD |

### 💴 為替・コモディティ・金利
| ティッカー | 名称 |
| --- | --- |
| USDJPY=X | ドル円 |
| GC=F | ゴールド先物 |
| ^TNX | 米国10年債利回り |

## よくあるエラーと対処法

| エラー / 症状 | 原因 | 対処法 |
| --- | --- | --- |
| `^TOPX` が毎回「取得失敗のためスキップ」になる | Yahoo Finance側でTOPIXのデータ提供が停止している | 仕様通りの動作。対応不要(他社データソースへの切替が必要な場合は別途検討) |
| 多数の銘柄で取得失敗が発生する | yfinanceがYahoo Financeのレート制限/一時的なブロックを受けている | 時間を置いて再実行する、または `market_report.py` の `REQUEST_INTERVAL` を増やす |
| `playwright._impl._errors.Error: Executable doesn't exist` | Playwright用ブラウザ未インストール | `python -m playwright install chromium` を実行 |
| コンソールのログが文字化けする(`�`等) | Windowsコンソールの既定コードページがUTF-8でない | `log_market_report.txt` 等のファイル自体はUTF-8で正しく保存されている。表示のみの問題でエディタで開けば正常に見える |
| `git push` でタスクが止まる/失敗する | 認証情報が未設定で資格情報入力待ちになっている | Git Credential Managerで認証情報をキャッシュするか、SSH鍵を設定する |
| `git commit` が "nothing to commit" でエラー表示される | 前回実行時とレポート内容に差分がない | バッチは継続するため対応不要。ログに記録されるのみ |
| `ModuleNotFoundError: No module named 'yfinance'` 等 | 仮想環境が有効化されていない、またはライブラリ未インストール | `.venv\Scripts\activate` を実行してから `pip install` し直す |
| HYPEの価格が異常に小さい(0.000005程度) | `HYPE-USD` は無関係な別トークンを指している | `market_report.py` では `HYPE32196-USD` を使用済み(修正不要) |
