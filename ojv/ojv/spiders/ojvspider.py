import scrapy
from scrapy.crawler import CrawlerProcess


class OjvspiderSpider(scrapy.Spider):
    name = "ojvspider"
    allowed_domains = ["www.topcv.vn"]
    start_urls = ["https://www.topcv.vn/tim-viec-lam-moi-nhat"]

    def parse(self, response):
        list_job = response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/div/div/div[3]/div[1]/div/div[1]/div')
        print(response.text)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    })

    process.crawl(OjvspiderSpider)
    process.start()