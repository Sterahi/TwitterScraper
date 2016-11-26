import scrapy

class TwitterSpider(scrapy.Spider):
    name = 'twitter_spider'
    start_urls = ['file://127.0.0.0.1/home/liz/Downloads/kirsy.html']
    def parse(self, response):
        SET_SELECTOR = '.js-stream-item'
        t_check = "False"
        for twitter in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.stream-item-header a strong ::text'
            USER_SELECTOR = '.stream-item-header a .username ::text'
            CONTENT_SELECTOR = '.content .TweetTextSize  ::text'
            QUOTE_SELECTOR = '.content .QuoteTweet-text ::text'
            TIME_SELECTOR = '.content small .tweet-timestamp ::text'

            with open('Themes/09_Food Supply', 'r') as theme:
                for line in theme:
                    output = theme.readline().lower().rstrip('\n')
                    tweet = map(lambda x:x.lower(),twitter.css(CONTENT_SELECTOR).extract())
                    tweet = str(' '.join(tweet))
                    if output.lower() in tweet:
                        t_check = 'Food Supply'
                # Loop test ends.
            yield {
                'name': twitter.css(NAME_SELECTOR).extract_first(),
                'user': twitter.css(USER_SELECTOR).extract(),
                'tweet': twitter.css(CONTENT_SELECTOR).extract(),
                'date': twitter.css(TIME_SELECTOR).extract_first(),
                'quote': twitter.css(QUOTE_SELECTOR).extract_first(),
                'theme': t_check
            }
            t_check = "False"
            # Yield Ends
        NEXT_PAGE_SELECTOR ='.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
