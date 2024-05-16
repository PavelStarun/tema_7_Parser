import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lights = response.css("div._Ud0k")

        for light in lights:
            yield {
                "name": light.css("div.lsooF span::text").get(),
                "price": light.css("div.pY3d2 span::text").get(),
                "url": light.css("a").attrib["href"],
            }

