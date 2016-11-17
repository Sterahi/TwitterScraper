import scrapy


class BrickSetSpider(scrapy.Spider):
    name = 'brickset_spider'
    start_urls = ['file://127.0.0.0.1/home/liz/Downloads/urwhatutweat.html']
    # start_urls = ['https://twitter.com/search?f=tweets&q=%23urwhatutweat&src=typd']

    def parse(self, response):
        SET_SELECTOR = '.js-stream-item'  # Getting class to pull base info from
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.stream-item-header a strong ::text'  # CSS identifier for the set name
            USER_SELECTOR = '.stream-item-header a .username ::text'
            CONTENT_SELECTOR = '.content p ::text'
            # IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'user': brickset.css(USER_SELECTOR).extract_first(),
                'minifigs': brickset.css(CONTENT_SELECTOR).extract_first(),
                # 'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
        NEXT_PAGE_SELECTOR ='.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
