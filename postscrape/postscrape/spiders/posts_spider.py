import scrapy

# Use 'scrapy crawl posts' from terminal to run this code which will
# generate the output html files.
# For interactive experimentation instead, use:
#   scrapy shell <url>
# which will open the scrapy shell, crawl that url, and create a 'response'
# variable containing the scraped response, then call various methods on response,
# WATCH THE VIDEO: https://www.youtube.com/watch?v=ALizgnSFTwQ&t=1535s 

class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        'https://blog.scrapinghub.com/page/1',
        'https://blog.scrapinghub.com/page/2'
    ]

    def parse(self, response):
        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

