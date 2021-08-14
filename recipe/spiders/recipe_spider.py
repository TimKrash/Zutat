from scrapy import Spider
import scrapy
from recipe.items import RecipeItem
# name, time, servings, ingredients

class RecipeSpider(Spider):
    name = "recipe"
    allowed_domains = ["bigoven.com"]
    start_urls = ["http://bigoven.com/recipes/course"]

    BASE_URL = 'http://bigoven.com'

    def parse(self, response):
        root = response.xpath('//div[@class="col-xs-12 collection-tile-full"]')
        root_links = root.xpath('//a[contains(@href, "/recipes")]/@href').getall()
        for idx, link in enumerate(root_links):
            self.abs_url = self.BASE_URL + link
            yield scrapy.Request(self.abs_url, callback=self.parse_root)

    def parse_root(self, response):
        subroot = response.xpath('//div[@id="recipesContainer"]')
        subroot_links = subroot.xpath('//a[contains(@href, "/recipes")]/@href').getall()
        for link in subroot_links:
            rel_url = self.BASE_URL + link
            yield scrapy.Request(rel_url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        recipe_root = response.xpath('//div[@id="resultContainer"]')
        recipe_links = recipe_root.xpath('//a[contains(@href, "/recipe/")]/@href').getall()
        for link in recipe_links:
            yield scrapy.Request(link, callback=self.parse_all)

    def parse_all(self, response):
        ingredients = response.xpath('//span[@class="name"]/text()').getall()
        ingredients.extend(response.xpath('//span[@class="name"]/a/text()').getall())
        name = response.xpath('//div[@class="recipe-container modern"]/h1/text()').getall()
        servings = response.xpath('//div[@class="yield"]/text()').getall()[1]
        time = response.xpath('//div[@class="ready-in rc-opt"]/text()').getall()[1]
        
        item = RecipeItem()
        item['name'] = name
        item['time'] = time
        item['servings'] = servings
        item['ingredients'] = ingredients

        yield item



