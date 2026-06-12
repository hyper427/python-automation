"""books.toscrape.com から書籍タイトル・価格・在庫状況を収集し、Markdownに保存する。"""

import logging
import random
import sys
import time
from datetime import date
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
ROBOTS_URL = urljoin(BASE_URL, "robots.txt")
USER_AGENT = "books-scraper-bot/1.0"
SLEEP_RANGE = (1, 3)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def load_robot_parser():
    rp = RobotFileParser()
    rp.set_url(ROBOTS_URL)
    try:
        rp.read()
    except Exception as exc:
        logger.error("robots.txtの取得に失敗しました: %s", exc)
        sys.exit(1)
    return rp


def can_fetch(rp, url):
    if not rp.can_fetch(USER_AGENT, url):
        logger.error("robots.txtによりアクセスが禁止されています: %s", url)
        return False
    return True


def fetch_html(rp, session, url):
    if not can_fetch(rp, url):
        return None
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("接続エラーが発生しました (%s): %s", url, exc)
        sys.exit(1)
    response.encoding = response.apparent_encoding
    return response.text


def parse_book_list(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one("p.price_color").get_text(strip=True)
        availability = article.select_one("p.instock.availability").get_text(strip=True)
        books.append({"title": title, "price": price, "availability": availability})

    next_link = soup.select_one("li.next a")
    next_url = urljoin(base_url, next_link["href"]) if next_link else None
    return books, next_url


def scrape_all_books(rp, session):
    books = []
    url = urljoin(BASE_URL, "catalogue/page-1.html")

    while url:
        logger.info("取得中: %s", url)
        html = fetch_html(rp, session, url)
        if html is None:
            break

        page_books, next_url = parse_book_list(html, url)
        books.extend(page_books)

        url = next_url
        if url:
            time.sleep(random.uniform(*SLEEP_RANGE))

    return books


def save_to_markdown(books, output_path):
    lines = [
        "# books.toscrape.com 書籍一覧",
        "",
        f"取得日: {date.today().isoformat()}",
        f"件数: {len(books)}",
        "",
        "| タイトル | 価格 | 在庫状況 |",
        "| --- | --- | --- |",
    ]
    for book in books:
        title = book["title"].replace("|", "\\|")
        lines.append(f"| {title} | {book['price']} | {book['availability']} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    rp = load_robot_parser()

    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})
        books = scrape_all_books(rp, session)

    output_path = f"books_{date.today().strftime('%Y%m%d')}.md"
    save_to_markdown(books, output_path)
    logger.info("完了しました: %s (%d件)", output_path, len(books))


if __name__ == "__main__":
    main()
