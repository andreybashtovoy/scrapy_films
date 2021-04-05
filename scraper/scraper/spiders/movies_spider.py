import scrapy
from html_text import extract_text
from ..items import MovieItem


class MoviesSpider(scrapy.Spider):
    name = "movies"
    pages_count = 2

    def start_requests(self):
        base_url = "https://rezka.ag/films/page/%s/"

        for page in range(1, self.pages_count + 1):
            yield scrapy.Request(url=base_url % page, callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        for item in response.css(".b-content__inline_item"):
            movie_url = item.css(".b-content__inline_item-cover a").attrib["href"]

            yield scrapy.Request(url=movie_url, callback=self.parse_movie)

    def parse_movie(self, response: scrapy.http.Response):
        obj = dict()

        for i in range(1, 15):
            if response.css(".b-post__info tr:nth-child(%s)" % i).get() is None:
                break

            key = extract_text(response.css(".b-post__info tr:nth-child(%s) td:first-child" % i).get())[:-3]
            value = extract_text(response.css(".b-post__info tr:nth-child(%s) td:last-child" % i).get())

            obj[key] = value

        movie_item = MovieItem()

        movie_item['name'] = response.css('.b-post__title h1::text').get()
        movie_item['ratings'] = obj['Рейтинги'] if 'Рейтинги' in obj else None
        movie_item['country'] = obj['Страна'] if 'Страна' in obj else None
        movie_item['genres'] = obj['Жанр'] if 'Жанр' in obj else None
        movie_item['time'] = obj['Время'] if 'Время' in obj else None

        yield movie_item
