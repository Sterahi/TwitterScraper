import scrapy


class TwitterSpider(scrapy.Spider):
    name = 'twitter_spider'
    start_urls = ['file://127.0.0.0.1/home/liz/Downloads/kirsy.html']
    # start_urls = ['https://twitter.com/search?f=tweets&q=%23urwhatutweat&src=typd']

    def parse(self, response):
        SET_SELECTOR = '.js-stream-item'
        for twitter in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.stream-item-header a strong ::text'
            USER_SELECTOR = '.stream-item-header a .username ::text'
            CONTENT_SELECTOR = '.content .TweetTextSize  ::text'
            QUOTE_SELECTOR = '.content .QuoteTweet-text ::text'
            TIME_SELECTOR = '.content small .tweet-timestamp ::text'
            # IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': twitter.css(NAME_SELECTOR).extract_first(),
                'user': twitter.css(USER_SELECTOR).extract(),
                'tweet': twitter.css(CONTENT_SELECTOR).extract(),
                'date': twitter.css(TIME_SELECTOR).extract_first(),
                'quote': twitter.css(QUOTE_SELECTOR).extract_first(),
                # 'image': twitter.css(IMAGE_SELECTOR).extract_first(),
                # {"name": "Danielle Vucenovic", "quote": null, "time": "Nov 8", "tweet": "Obviously not going to stop ", "user": "@"},

            }
        NEXT_PAGE_SELECTOR ='.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
