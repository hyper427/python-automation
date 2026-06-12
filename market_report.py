"""Yahoo Finance (yfinance) から各銘柄を取得し、日次マーケットレポートをMarkdownとHTMLで出力する。"""

import html
import logging
import time
from datetime import date

import yfinance as yf

REQUEST_INTERVAL = 0.3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

JP_STOCK_CODES = [
    "7011", "7744", "7777", "6721", "1407", "3823", "3777", "2134", "3070", "8894",
    "5016", "7012", "5451", "5803", "285A", "8267", "4661", "8729", "8107", "7148",
    "2914", "5401", "3350", "5838", "4755", "4063", "4452", "4502", "4503", "4568",
    "6098", "6501", "6758", "6861", "6954", "6981", "7203", "7267", "7751", "7974",
    "8031", "8058", "8306", "8316", "8411", "8766", "8802", "9432", "9984",
]

US_STOCK_CODES = [
    "TSLA", "COIN", "TLT", "HOOD", "QS", "RIOT", "MARA", "MO", "CRWV", "MSTR",
    "NBIS", "ONDS", "INOD", "BMNR", "NVDA", "AMSC", "INDI", "MU", "OKLO", "POET",
    "SNDK", "ZS", "APH", "AAOI", "VRT", "ALAB", "COHR", "HYPD",
]

SECTIONS = [
    ("📊 指数サマリー", ["^N225", "^TOPX", "^IXIC", "^DJI", "^GSPC", "^SOX"]),
    ("🇯🇵 日本株", [f"{code}.T" for code in JP_STOCK_CODES]),
    ("🇺🇸 米国株", US_STOCK_CODES),
    ("💰 仮想通貨", ["BTC-USD", "HYPE32196-USD"]),
    ("💴 為替・コモディティ・金利", ["USDJPY=X", "GC=F", "^TNX"]),
]

# 日本語名が判明している銘柄のみマッピング(不明な銘柄はyfinanceの英語名を使用)
NAME_OVERRIDES = {
    "^N225": "日経平均株価",
    "^IXIC": "NASDAQ総合指数",
    "^DJI": "NYダウ",
    "^GSPC": "S&P500",
    "^SOX": "SOX指数(フィラデルフィア半導体)",
    "7011.T": "三菱重工業",
    "7744.T": "ノーリツ鋼機",
    "7777.T": "スリー・ディー・マトリックス",
    "6721.T": "ウインテスト",
    "1407.T": "ウエストホールディングス",
    "3823.T": "WHY HOW DO",
    "3777.T": "環境フレンドリー",
    "2134.T": "キタハマキャピタル",
    "3070.T": "ジェリービーンズ",
    "8894.T": "REVOLUTION",
    "5016.T": "JX金属",
    "7012.T": "川崎重工業",
    "5451.T": "淀川製鋼所",
    "5803.T": "フジクラ",
    "285A.T": "キオクシアHD",
    "8267.T": "イオン",
    "4661.T": "OLC",
    "8729.T": "ソニーFG",
    "8107.T": "キムラタン",
    "7148.T": "FPG",
    "2914.T": "日本たばこ産業",
    "5401.T": "日本製鉄",
    "3350.T": "メタプラネット",
    "5838.T": "楽天銀行",
    "4755.T": "楽天グループ",
    "4063.T": "信越化学工業",
    "4452.T": "花王",
    "4502.T": "武田薬品工業",
    "4503.T": "アステラス製薬",
    "4568.T": "第一三共",
    "6098.T": "リクルートホールディングス",
    "6501.T": "日立製作所",
    "6758.T": "ソニーグループ",
    "6861.T": "キーエンス",
    "6954.T": "ファナック",
    "6981.T": "村田製作所",
    "7203.T": "トヨタ自動車",
    "7267.T": "本田技研工業",
    "7751.T": "キヤノン",
    "7974.T": "任天堂",
    "8031.T": "三井物産",
    "8058.T": "三菱商事",
    "8306.T": "三菱UFJフィナンシャル・グループ",
    "8316.T": "三井住友フィナンシャルグループ",
    "8411.T": "みずほフィナンシャルグループ",
    "8766.T": "東京海上ホールディングス",
    "8802.T": "三菱地所",
    "9432.T": "日本電信電話",
    "9984.T": "ソフトバンクグループ",
    "TSLA": "テスラ",
    "COIN": "コインベース",
    "TLT": "iシェアーズ米国国債20年",
    "HOOD": "ロビンフッド",
    "QS": "クアンタムスケープ",
    "RIOT": "ライオットプラットフォームズ",
    "MARA": "マラホールディングス",
    "MO": "アルトリア",
    "CRWV": "コアウィーブ",
    "MSTR": "ストラテジー",
    "NBIS": "ネビウスグループ",
    "ONDS": "オンダスインク",
    "INOD": "イノデータ",
    "BMNR": "ビットマインイマージョン",
    "NVDA": "エヌビディア",
    "AMSC": "アメリカンスーパーコンダクター",
    "INDI": "インディセミコンダクタ",
    "MU": "マイクロン",
    "OKLO": "オクロ",
    "POET": "ポエットテクノロジーズ",
    "SNDK": "サンディスク",
    "ZS": "Zスケーラー",
    "APH": "アンフェノール",
    "AAOI": "アプライドオプトエレクトロニクス",
    "VRT": "バーティブホールディングス",
    "ALAB": "アステラボ",
    "COHR": "コヒレント",
    "HYPD": "ハイペリオンDeFi",
}


def fetch_quote(symbol):
    info = yf.Ticker(symbol).info

    name = NAME_OVERRIDES.get(symbol) or info.get("shortName") or info.get("longName") or symbol
    current = info.get("regularMarketPrice")
    previous_close = info.get("regularMarketPreviousClose")
    change = info.get("regularMarketChange")
    change_percent = info.get("regularMarketChangePercent")

    if current is None or previous_close is None:
        raise ValueError("価格データを取得できませんでした")

    if change is None:
        change = current - previous_close
    if change_percent is None:
        change_percent = (change / previous_close) * 100 if previous_close else 0.0

    return {
        "name": name,
        "current": current,
        "change": change,
        "change_percent": change_percent,
    }


def collect_section_quotes(symbols):
    quotes = []
    for symbol in symbols:
        try:
            quote = fetch_quote(symbol)
        except Exception as exc:
            logger.error("取得失敗のためスキップします: %s (%s)", symbol, exc)
            continue
        quotes.append(quote)
        time.sleep(REQUEST_INTERVAL)
    return quotes


def arrow_for(change):
    if change > 0:
        return "▲"
    if change < 0:
        return "▼"
    return "→"


def build_markdown_section(title, quotes):
    lines = [f"## {title}", "", "| 銘柄名 | 現在値 | 前日比(%) | 前日比(金額) |", "| --- | --- | --- | --- |"]

    for quote in quotes:
        arrow = arrow_for(quote["change"])
        sign = "+" if quote["change"] >= 0 else ""
        current_str = f"{quote['current']:,.2f}"
        pct_str = f"{arrow} {sign}{quote['change_percent']:.2f}%"
        change_str = f"{arrow} {sign}{quote['change']:,.2f}"
        lines.append(f"| {quote['name']} | {current_str} | {pct_str} | {change_str} |")

    lines.append("")
    return lines


def build_html_section(title, quotes, is_index=False):
    section_class = "section index" if is_index else "section"
    items = []
    for quote in quotes:
        change = quote["change"]
        if change > 0:
            change_class = "up"
        elif change < 0:
            change_class = "down"
        else:
            change_class = "flat"

        arrow = arrow_for(change)
        sign = "+" if change >= 0 else ""
        items.append(f"""      <div class="ticker">
        <span class="name">{html.escape(quote['name'])}</span>
        <span class="price">{quote['current']:,.2f}</span>
        <span class="change {change_class}">{arrow} {sign}{quote['change_percent']:.2f}%</span>
        <span class="change {change_class}">{arrow} {sign}{quote['change']:,.2f}</span>
      </div>""")

    items_html = "\n".join(items)
    return f"""  <section class="{section_class}">
    <h2>{html.escape(title)}</h2>
    <div class="grid">
{items_html}
    </div>
  </section>"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>市場レポート ({date})</title>
<style>
  :root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --text: #c9d1d9;
    --muted: #8b949e;
    --green: #3fb950;
    --red: #f85149;
    --border: #30363d;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 16px;
  }}
  h1 {{
    text-align: center;
    font-size: 1.4rem;
    margin-bottom: 24px;
  }}
  .section {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin: 0 auto 20px;
    max-width: 960px;
  }}
  .section h2 {{
    margin-top: 0;
    font-size: 1.1rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}
  .grid {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .ticker {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
  }}
  .ticker .name {{
    flex: 2 1 auto;
    min-width: 0;
    font-weight: 600;
    color: var(--text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .ticker .price {{
    flex: 1 0 auto;
    width: 100px;
    text-align: right;
    font-weight: 700;
  }}
  .ticker .change {{
    flex: 1 0 auto;
    width: 90px;
    text-align: right;
    font-size: 0.9rem;
  }}
  .change.up {{ color: var(--green); }}
  .change.down {{ color: var(--red); }}
  .change.flat {{ color: var(--muted); }}

  .section.index .ticker {{
    padding: 10px 14px;
  }}
  .section.index .ticker .price {{
    font-size: 1.6rem;
    width: 140px;
  }}
  .section.index .ticker .name {{
    font-size: 1.1rem;
  }}

  @media (max-width: 480px) {{
    body {{ padding: 8px; }}
    .ticker {{ gap: 4px; padding: 6px 8px; font-size: 0.85rem; }}
    .ticker .price {{ width: 80px; }}
    .ticker .change {{ width: 72px; font-size: 0.8rem; }}
    .section.index .ticker .price {{ font-size: 1.2rem; width: 100px; }}
  }}
</style>
</head>
<body>
  <h1>市場レポート ({date})</h1>
{sections}
</body>
</html>
"""


def build_html(today, section_results):
    sections_html = []
    for index, (title, quotes) in enumerate(section_results):
        sections_html.append(build_html_section(title, quotes, is_index=(index == 0)))

    return HTML_TEMPLATE.format(date=today.isoformat(), sections="\n".join(sections_html))


def main():
    today = date.today()
    markdown_lines = [f"# 市場レポート ({today.isoformat()})", ""]
    section_results = []

    for title, symbols in SECTIONS:
        logger.info("取得中: %s", title)
        quotes = collect_section_quotes(symbols)
        section_results.append((title, quotes))
        markdown_lines.extend(build_markdown_section(title, quotes))

    md_path = f"market_report_{today.strftime('%Y%m%d')}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))

    html_path = f"market_report_{today.strftime('%Y%m%d')}.html"
    html_content = build_html(today, section_results)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    logger.info("完了しました: %s, %s, index.html", md_path, html_path)


if __name__ == "__main__":
    main()
