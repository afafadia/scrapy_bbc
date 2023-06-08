from urllib.parse import urlparse

import scrapy


def map_urls(image_src, image_data_src):
    image_data_src = image_data_src.replace("{width}", "144") if "{width}" in image_data_src else image_data_src
    return f"{image_data_src}" if "data" in image_src else f"{image_src}"


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
        images_src = response.css(".media-list__item .responsive-image img ::attr(src)").getall()
        images_data_src = response.css(".media-list__item .responsive-image ::attr(data-src)").getall()
        valid_images = map(map_urls, images_src, images_data_src)
        home_page_titles = [title.strip() if title else "" for title in response.css("a.media__link::text").getall()]

        for i, (article, home_page_title, image, tag) in enumerate(
            zip(articles, home_page_titles, valid_images, tags)
        ):
            yield response.follow(
                article,
                callback=self.parse_article,
                meta={
                    "i": i,
                    "home_page_title": home_page_title,
                    "tag": tag,
                    "image": image,
                },
                dont_filter=True,
            )

    def parse_article(self, response):
        page_title = response.css("h1::text").get()

        if not page_title:
            page_title = response.css("#main-heading > span::text").get()

        home_page_title = response.meta["home_page_title"]

        data = {}
        data["i"] = response.meta["i"]

        if page_title != home_page_title:
            data["home_page_title"] = home_page_title

        data_dict = {
            "page_title": page_title.strip() if page_title else "",
            "image": response.meta["image"],
            "url": response.url,
            "tag": response.meta["tag"],
        }

        data.update(data_dict)
        yield data
