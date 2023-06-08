from urllib.parse import urlparse

import scrapy


class BBCSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com"]

    def remove_domain(self, urls):
        cleaned_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            cleaned_urls.append(parsed_url.path)
        return cleaned_urls

    def parse(self, response):
        articles = self.remove_domain(response.css("a.media__link ::attr(href)").getall())
        tags = response.css("a.media__tag ::text").getall()

        home_page_titles = [title.strip() if title else "" for title in response.css("a.media__link::text").getall()]

        for article, home_page_title, tag in zip(articles, home_page_titles, tags):
            yield response.follow(
                article,
                callback=self.parse_article,
                meta={
                    "home_page_title": home_page_title,
                    "tag": tag,
                },
                dont_filter=True,
            )

    def parse_article(self, response):
        """
        Parse Articles Detail Page
        """

        page_title = response.css("h1::text").get()
        article_detail_page_image = response.css("meta[property='og:image']::attr(content)").get()

        if not page_title:
            page_title = response.css("#main-heading > span::text").get()

        home_page_title = response.meta["home_page_title"]

        data = {}

        # If title on home page is different than the title on articles detail page, show both titles
        if page_title != home_page_title:
            data["home_page_title"] = home_page_title

        data_dict = {
            "page_title": page_title.strip() if page_title else "",
            "image": article_detail_page_image if "live" not in response.url else "LIVE PAGE",
            "url": response.url,
            "tag": response.meta["tag"],
        }

        data.update(data_dict)
        yield data
