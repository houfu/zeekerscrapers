import datetime
import re

import requests
import scrapy
import bs4

from about_singapore_law.items import ZeekerArticle


class SlwSpider(scrapy.Spider):
    name = "about_singapore_law"
    allowed_domains = ["singaporelawwatch.sg"]
    start_urls = [
        "https://www.singaporelawwatch.sg/About-Singapore-Law/Overview",
        "https://www.singaporelawwatch.sg/About-Singapore-Law/Commercial-Law",
        "https://www.singaporelawwatch.sg/About-Singapore-Law/Singapore-Legal-System",
    ]

    def start_requests(self):
        for url in self.start_urls:
            r = requests.get(url)
            soup = bs4.BeautifulSoup(r.text, 'html5lib')
            article_list = soup.find(class_="edn__articleListWrapper")
            articles = [article for article in article_list if type(article) == bs4.element.Tag]
            for article in articles:
                yield scrapy.Request(article.a["href"])

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, "html5lib")
        article = soup.find(class_='edn_article')
        text_list = []
        published = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        for child in article.children:
            if type(child) == bs4.element.Tag:
                if "edn_fixedPrevNextArticleNavigation" in child.attrs.get('class', []):
                    break
                if match := re.match(r"Updated as at (\d{2} [a-zA-Z]+ \d{4})", child.text):
                    raw_date = match.group(1)
                    dt = datetime.datetime.strptime(raw_date, "%d %B %Y")
                    published = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    continue
            text_list.append(child.text)

        text = ''.join(text_list)

        yield ZeekerArticle(
            title=article.h1.text,
            date_scraped=datetime.datetime.now().isoformat(),
            url=response.url,
            text=text,
            date_published=published
        )
