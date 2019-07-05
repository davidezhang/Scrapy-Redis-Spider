import scrapy
 
from Tmall.items import TmallItem

from scrapy_redis.spiders import RedisSpider
 
class TmallSpider(RedisSpider):
    name = "quotes"

    redis_key = 'quotes:start_urls'

    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(TmallSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = TmallItem()
        for quote in response.css("div.quote"):
            item['text'] = quote.css("span.text::text").extract_first(),
            item['author'] = quote.css("small.author::text").extract_first(),
            item['tags'] = quote.css("div.tags > a.tag::text").extract()
            yield item

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
