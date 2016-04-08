import scrapy


from uvinum.items import UvinumItem
from uvinum import uvinumCSVItemExporter
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.log import configure_logging

class uvinumSpider(scrapy.Spider):
    name = "uvinum"
    allowed_domains = ["uvinum.es"]
    start_urls = [
        "http://www.uvinum.es/denominaciones"
    ]
    
    wine_types = [
        "t:tinto",
        "t:blanco",
        "t:espumoso",
        "t:rosado",
        "t:generoso",
        "t:dulce",
        "t:sin-alcohol"
    ]
    
    wine_year = [
        "y:1997",
        "y:1998",
        "y:1999",
        "y:2000",
        "y:2001",
        "y:2002",
        "y:2003",
        "y:2004",
        "y:2005",
        "y:2006",
        "y:2007",
        "y:2008",
        "y:2009",
        "y:2010",
        "y:2011",
        "y:2012",
        "y:2013",
        "y:2014",
        "y:2015",
        "y:2016"
    ]
    #configure_logging({'LOG_LEVEL': '%(levelname)s: %(message)s'})

    
    def parse(self, response):
        
        self.logger.info('** Init parse **')
        #urls = response.xpath('//div[@class="region"]/ul/li/a/@href').extract()
        
        
        
        
        #urls = ['vino-rioja','vino-navarra']
        
        #for url in urls:
        #
        #    _url = url.split('/')
        #    do_name = _url[len(_url)-1]
        #    self.logger.debug('** DO %s **',do_name)
        #            
        #    do_to_scrap = "http://www.uvinum.es/vinos:k:"+do_name+":v:todos"
        #            
        #    for types in self.wine_types:
        #        for years in self.wine_year:
        #            url_to_scrap = do_to_scrap + ":" + years + ":" + types
        #            yield scrapy.Request(url_to_scrap, callback=self.parseDO,meta = {
        #          'dont_redirect': True,
        #          'handle_httpstatus_list': [301]
        #      })
        
        #url_to_scrap = "http://www.uvinum.es/vinos:k:vino-navarra:v:todos:y:1998:t:tinto"
        #yield scrapy.Request(url_to_scrap, callback=self.parseDO,meta = {
        #          'dont_redirect': True,
        #          'handle_httpstatus_list': [301]
        #      })
        
        url_to_scrap = "http://www.uvinum.es/vino-navarra/dignus-1998"
        yield scrapy.Request(url_to_scrap, callback=self.parseURL2,meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [301]
              }, dont_filter=True) 
                
      
    def parseDO(self, response):
        
        self.logger.debug('** DO url %s **',response.url)
        
        arrows = response.xpath('//a[@class="arrows"]/@href').extract();
        
        if len(arrows) > 0:
            lastPage = arrows[len(arrows)-1]
            self.logger.debug('** last page for DO %s **',lastPage)
            
            exitCondition = True
            index = 1;
            while exitCondition:
                
                url = response.url+":"+ str(index)
                self.logger.debug('** scrap URL %s',url)
                yield scrapy.Request(url, callback=self.parseURL,meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [301]
              }) 
                
                index = index + 1
                if index > 60:
                    self.logger.warning('** More than 60 pages for DO %s',response.url)
                if url == lastPage:
                    exitCondition = False
                else:
                    exitCondition = True
                
        else:
            self.logger.debug('** No pagination for DO %s ',response.url)
            
            yield scrapy.Request(response.url, callback=self.parseURL,meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [301]
              }, dont_filter=True) 
        
        
#nada
    
    def parseURL(self, response):
        

            
        self.logger.info('** Init parseURL1 %s **',response.url)    
            
        hxs = Selector(response)
        products = hxs.xpath('//li[@class="data-product result result-with-button"]')
        #products = hxs.xpath('///html/body/div[2]/div[3]/div[3]/div[3]/div[2]/ul/li[2]')
        products = products + hxs.xpath('//li[@class="data-product result"]')
        
        items = []
        for product in products:
            item = UvinumItem()
            item['cellar'] = product.xpath('@data-cellar').extract()
            item['store'] = product.xpath('@data-store').extract()
            item['category'] = product.xpath('@data-category').extract()
            item['name'] = product.xpath('@data-name').extract()
            item['source'] = product.xpath('@data-store').extract()
            item['precio'] = product.xpath('normalize-space(.//*[@class="precio"]/text())').extract()
            item['puntuacion'] = product.xpath('normalize-space(.//*[@class="nota"]/strong)').extract()
            
            #item['cellar'] = item['cellar'].encode('utf-8')
            items.append(item)
        return items
    
    def parseURL2(self, response):
        
        self.logger.info('** Init parseURL2 %s **',response.url)    
            
        item = UvinumItem()
        item['name'] = response.xpath('normalize-space(.//*[@class="url"]/strong/text())').extract()
        item['anada'] = response.xpath('normalize-space(.//*[@class="anadas"]/strong)').extract()
        item['cellar'] = response.xpath('normalize-space(.//*[@itemprop="name"]/text())').extract()
        item['do'] = response.xpath('normalize-space(.//*[@class="attribute"]/a/text())').extract()
        item['tipo'] = response.xpath('normalize-space(.//*[@class="wine-type"]/dd/text())').extract()
        item['volumen'] = response.xpath('normalize-space(.//*[@class="tamanos"]/strong/text())').extract()
        item['tipouvas'] = response.xpath('normalize-space(.//*[@itemprop="description"]/br/text())').extract()
        item['alergenos'] = response.xpath('normalize-space(.//*[@class="attributes-box-right"]/dd/text())').extract()
        item['precio'] = response.xpath('normalize-space(.//*[@class="price"]/text())').extract()
        item['store'] = response.xpath('normalize-space(.//*[@class="shipping_info"]/span/a/strong/text())').extract()
        item['puntuacion'] = response.xpath('normalize-space(.//*[@class="nota"]/strong)').extract()
            
        return item
            