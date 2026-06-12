"""quotes.toscrape.com/js から名言・著者名を収集し、Markdownとスクリーンショットに保存する。"""

import logging
import random
import sys
import time
from datetime import date
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

BASE_URL = "https://quotes.toscrape.com/"
START_PATH = "/js"
ROBOTS_URL = urljoin(BASE_URL, "robots.txt")
USER_AGENT = "quotes-scraper-bot/1.0"
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


def parse_quotes(page):
    quotes = []
    for block in page.query_selector_all(".quote"):
        text = block.query_selector(".text").inner_text().strip()
        author = block.query_selector(".author").inner_text().strip()
        quotes.append({"text": text, "author": author})
    return quotes


def get_next_url(page, current_url):
    next_link = page.query_selector("li.next a")
    if not next_link:
        return None
    return urljoin(current_url, next_link.get_attribute("href"))


def scrape_all_quotes(rp, page):
    quotes = []
    url = urljoin(BASE_URL, START_PATH)
    first_page = True
    screenshot_path = None

    while url:
        if not can_fetch(rp, url):
            break

        logger.info("取得中: %s", url)
        try:
            page.goto(url, wait_until="networkidle")
        except PlaywrightError as exc:
            logger.error("接続エラーが発生しました (%s): %s", url, exc)
            sys.exit(1)

        if first_page:
            screenshot_path = f"quotes_{date.today().strftime('%Y%m%d')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            first_page = False

        quotes.extend(parse_quotes(page))

        next_url = get_next_url(page, url)
        url = next_url
        if url:
            time.sleep(random.uniform(*SLEEP_RANGE))

    return quotes, screenshot_path


def save_to_markdown(quotes, output_path):
    lines = [
        "# quotes.toscrape.com 名言一覧",
        "",
        f"取得日: {date.today().isoformat()}",
        f"件数: {len(quotes)}",
        "",
        "| 名言 | 著者 |",
        "| --- | --- |",
    ]
    for quote in quotes:
        text = quote["text"].replace("|", "\\|")
        author = quote["author"].replace("|", "\\|")
        lines.append(f"| {text} | {author} |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    rp = load_robot_parser()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        try:
            page = browser.new_page(user_agent=USER_AGENT)
            quotes, screenshot_path = scrape_all_quotes(rp, page)
        finally:
            browser.close()

    output_path = f"quotes_{date.today().strftime('%Y%m%d')}.md"
    save_to_markdown(quotes, output_path)
    logger.info("完了しました: %s (%d件), スクリーンショット: %s", output_path, len(quotes), screenshot_path)


if __name__ == "__main__":
    main()
