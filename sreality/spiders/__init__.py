
import json
import scrapy

class SrealitySpider(scrapy.Spider):
    
    name = 'srealityspider'
    allowed_domains = ['sreality.cz']
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500']
    
    def parse(self, response):
        
        data = json.loads(response.body.decode("utf-8", "ignore"))
        
        for e in data["_embedded"]["estates"]:
            yield {
                "title": e["name"],
                "links": [d["href"] for d in e["_links"]["images"]]
            }
