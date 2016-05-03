 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import scrapy
import math
import os
import random

from uvinum.items import UvinumItem
from uvinum import uvinumCSVItemExporter, settings
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
#from scrapy.utils.log import configure_logging

class uvinumSpider(scrapy.Spider):
    name = "uvinum"
    allowed_domains = ["uvinum.es"]  
    
    
    
    proxy_pool = [
        "http://50.16.130.96:80",
        "http://107.163.117.234:808",
        "http://107.151.152.210:80",
        "http://107.163.117.116:808",
        "http://107.163.117.82:808",
        "http://134.249.168.16:80",
        "http://107.151.142.124:80",
        "http://81.21.77.150:8083",
        "http://23.96.16.185:80",
        "http://46.129.14.37:80",
        "http://117.135.250.134:8081",
        "http://117.135.251.135:84",
        "http://117.135.251.132:84",
        "http://117.135.251.134:81",
        "http://117.135.251.136:83",
        "http://117.135.251.133:84",
        "http://117.135.251.136:81",
        "http://117.135.251.134:80",
        "http://117.135.251.136:80",
        "http://117.135.250.133:8082",
        "http://117.135.251.133:80",
        "http://117.135.250.134:80",
        "http://117.135.251.135:82",
        "http://117.135.251.131:83",
        "http://117.135.251.133:83",
        "http://117.135.251.131:82",
        "http://117.135.251.134:84",
        "http://117.135.251.131:81",
        "http://117.135.250.134:8082",
        "http://120.198.233.211:80",
        "http://101.81.22.21:8118",
        "http://117.135.250.133:8081",
        "http://117.135.250.133:8083"
    ]
    
    os.environ['http_proxy']=proxy_pool[random.randint(0,len(proxy_pool)-1)]
    #url donde empieza a buscar
    start_urls = [
        "http://www.uvinum.es/denominaciones"
    ]

#     wine_types = [
#         "t:tinto",
#         "t:blanco",
#         "t:espumoso",
#         "t:rosado",
#         "t:generoso",
#         "t:dulce",
#         "t:sin-alcohol"
#     ]
    
#     wine_year = [
#         "y:1997",
#         "y:1998",
#         "y:1999",
#         "y:2000",
#         "y:2001",
#         "y:2002",
#         "y:2003",
#         "y:2004",
#         "y:2005",
#         "y:2006",
#         "y:2007",
#         "y:2008",
#         "y:2009",
#         "y:2010",
#         "y:2011",
#         "y:2012",
#         "y:2013",
#         "y:2014",
#         "y:2015",
#         "y:2016"
#     ]


    #configure_logging({'LOG_LEVEL': '%(levelname)s: %(message)s'})
    
    def parse(self, response):
        """Este metodo obtiene una lista de url con filtros de region que se scrapean con los otros metodos parse.
        """
        self.logger.info('** Init parse **')
        #obtener la lista de regiones como urls
        region_urls = response.xpath('//div[@class="region"]/ul/li/a/@href').extract()
        #urls = ['vino-rioja','vino-navarra']
        
        #hacer requests para las url de la lista de vinos con los filtros para cada region
        for url in region_urls[120:121]:#iterando sobre las regiones
            os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]   
            region = str(url)[21:]#cortar de cada url el nombre de la region
            #self.logger.debug('** Region %s **',region)
                
            #construir la url de la lista de vinos con el filtro de la region        
            region_filter_url = "http://www.uvinum.es/vinos:k:"+region+":v:todos"
            print "I will go to", region_filter_url
            #añadir a la url do_to_scrap filtros de anada y tipos de vino (no se puede hacer aqui porque no los sabemos)
            #usar filter_vintage y filter_wine_type        
#             for types in self.wine_types:
#                 for years in self.wine_year:
#                     total_filter_url = region_filter + ":" + years + ":" + types
#                     yield scrapy.Request(total_filter_url, callback=self.parseDO,meta = {
#                   'dont_redirect': True,
#                   'handle_httpstatus_list': [301]
#               })
        
            #requests para cada region
            yield scrapy.Request(region_filter_url, callback=self.parseRegion,meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301]
                })
        
        
        #crear requests a las url con una callback que es otro metodo parse
        #la callback se ejecuta una vez ejecutada la request
#         yield scrapy.Request(url_to_scrap, callback=self.parseURL,meta = {
#                   'dont_redirect': True,
#                   'handle_httpstatus_list': [301]
#               }, dont_filter=True) 
                
    def parseRegion(self, response):
        """Este parse se ejecuta para cada region. Obtiene las anadas y tipos de vino que haya y manda las requests para
        las urls con filtros de region, anada y tipos."""
        region_name = response.xpath("//title/text()").extract_first()
        print region_name
        #self.logger.debug('** Region filter %s **', region_name)
        #print region_name
        #obtner las urls de las paginas con filtro de region y año
        year_urls = response.xpath('//div[@id="filter_vintage"]/ul/li/a/@href').extract()
        
        for year_url in year_urls:
            os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]
            if year_url!="#":# a veces en las url que coge hay un #, con este if evitamos que salte el error
                yield scrapy.Request(year_url, callback=self.parseYear)
        
#         #crear lista con los años que hay y añadir el filtro de año a la url con filtro de tipo y region
#         for year_url in year_urls:
#             year = year_url[-7:]#coger la seccion ":y:AAAA" de la url
#             for type_url in type_urls:
#                 #añadir esta seccion a la url que ya lleva el filtro de tipo y region
#                 total_url = type_url + year
                
        
    
    def parseYear(self, response):
        "Se ejecuta para cada region y año. Envia requests para cada tipo, region y año."
        
        #obtener las urls de las paginas con filtro de tipo que hay en esta pagina
        type_urls = response.xpath('//div[@id="filter_wine_type"]/ul/li/a/@href').extract()
        
        print "i am in", response.url
        
        for type_url in type_urls:
            os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]
            if type_url!="#":
                yield scrapy.Request(type_url, callback=self.parseType, meta = {
                        'dont_redirect': True,
                        'handle_httpstatus_list': [301]
                    })
        
        
    def parseType(self, response):
        """Se ejecuta para cada region, año y tipo.
        Obtener las url de los vinos de una pagina con filtros, y enviar requests si hay mas paginas con esos filtros."""
        #self.logger.debug('** I am in %s **', response.url)
        first_page = response.url
        print "I am in", first_page
        
        #cuantos vinos hay con estos filtros.
        N_wines = int((response.xpath('//div[@class="sales-filters"]/em/text()').extract()[-1])[1:-1])
        #y cuantas paginas, para poder buscar en ellas si hay mas de 1
        N_pages = int(math.ceil(N_wines/20.))
        #if N_wines > 1200:#quiza hay que handlear algun caso, poniendo otro filtro
        
        wine_urls = response.xpath('//a[@class="name"]/@href').extract()#obtner las urls de cada vino
        
        #request individual para cada vino
        for wine_url in wine_urls:
            #os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]
            #wine_url = "http://webcache.googleusercontent.com/search?q=cache:" + wine_url
            
            if wine_url!="#":
                yield scrapy.Request(wine_url, callback=self.parseDATA, meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301]
                })
            
        #comprovar si hay mas paginas       
        if (N_pages > 1):
            for x in xrange(N_pages-1):#para cada una de las siguientes paginas
                #añadir el numero de pagina a la url
                page_url = first_page + str(x+2)
                #hacer la request para la url de esa pagina
                os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]
                if page_url!="#":
                    yield scrapy.Request(page_url, callback=self.parseType_extraPage, meta = {
                        'dont_redirect': True,
                        'handle_httpstatus_list': [301]
                        })
                
    def parseType_extraPage(self, response):    
        """parse para las siguientes paginas con filtro de año, region y tipo; en caso de haber mas de una."""  
        print "I am in", response.url
        
        wine_urls = response.xpath('//a[@class="name"]/@href').extract()#obtner las urls de cada vino
        
        #request individual para cada vino
        for wine_url in wine_urls:
            #os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]
            #wine_url = "http://webcache.googleusercontent.com/search?q=cache:" + wine_url
            if wine_url!="#":
                yield scrapy.Request(wine_url, callback=self.parseDATA, meta = {
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301]
                })
            
    def parseDATA(self, response):
        """Obtener los datos de cada campo de interes para un vino."""
        ### EN PROCESO ###
        print "I am in", response.url
        wine = UvinumItem()
        wine['name'] = response.xpath('//div[@class="product-title"]/h1/@title').extract()
        product = response.xpath('//div[@class="attributes-container"]')
        wine['cellar'] = product.xpath('.//a[@class="bodegas"]/@title').extract()
        wine['tipo'] = product.xpath('.//dl[@class="wine-type"]/dd/strong/text()').extract()
        wine['anada'] = product.xpath('.//dd[@class="anadas"]/strong/text()').extract()
        wine['DO'] = product.xpath('.//dl[@class="appellation"]/dd/a/text()').extract_first()
        wine['volumen'] = product.xpath('.//dd[@class="tamanos"]/strong/text()').extract()
        #wine['alergenos'] = #no se puede buscar por nombre porque la etiqueta es Alérgenos, y no se aceptan acentos en xpath
        wine['precio'] = response.xpath('//span[@itemprop="price"]/text()').extract_first()
        wine['tipouvas'] = product.xpath('//p[@itemprop="description"]').extract()
#         if wine['tipouvas']!=[]:
#             if "UVAS" in wine['tipouvas'][0]:
#                 wine['tipouvas'] = wine['tipouvas'][0].split('UVAS')[1].split('BODEGA')[0]
#             else: #si no lo podemos sacar de la descripcion
#                 wine['tipouvas'] = product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract()
#         else: wine['tipouvas'] = product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract()
        wine['tipouvas'] = product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract()
        wine['alcohol'] = product.xpath('.//dt[@title="Vol. de alcohol"]/../dd/text()').extract()
        wine['puntuacionrp'] = product.xpath('//dd[@class="guides"]/span[@class="guia_pk guide"]/text()').extract()
        wine['puntuacionws'] = product.xpath('//dd[@class="guides"]/span[@class="guia_ws guide"]/text()').extract()
        wine['puntuacionrvf'] = product.xpath('//dd[@class="guides"]/span[@class="guia_larvf guide"]/text()').extract()
        wine['puntuaciongp'] = product.xpath('//dd[@class="guides"]/span[@class="guia_p guide"]/text()').extract()
        wine['notausuarios'] = response.xpath('//div[@class="nota"]/p/strong[@itemprop="ratingValue"]/text()').extract()
        wine['notadecata'] = product.xpath('//p[@itemprop="description"]').extract()[0]
        #para recortar la nota de cata:
        if "BODEGA" in wine['notadecata']:
            wine['notadecata'] = wine['notadecata'].split("BODEGA")[0]
        if "UVAS" in wine['notadecata']:
            wine['notadecata'] = wine['notadecata'].split("UVAS")[0]
        
        #...Añadir
        return wine
    
    
# #    def parseDO(self, response):
#         
#         self.logger.debug('** DO url %s **',response.url)
#         
#         arrows = response.xpath('//a[@class="arrows"]/@href').extract();
#         
#         if len(arrows) > 0:
#             lastPage = arrows[len(arrows)-1]
#             self.logger.debug('** last page for DO %s **',lastPage)
#             
#             exitCondition = True
#             index = 1;
#             while exitCondition:
#                 
#                 url = response.url+":"+ str(index)
#                 self.logger.debug('** scrap URL %s',url)
#                 yield scrapy.Request(url, callback=self.parseURL,meta = {
#                   'dont_redirect': True,
#                   'handle_httpstatus_list': [301]
#               }) 
#                 
#                 index = index + 1
#                 if index > 60:
#                     self.logger.warning('** More than 60 pages for DO %s',response.url)
#                 if url == lastPage:
#                     exitCondition = False
#                 else:
#                     exitCondition = True
#                 
#         else:
#             self.logger.debug('** No pagination for DO %s ',response.url)
#             
#             yield scrapy.Request(response.url, callback=self.parseURL,meta = {
#                   'dont_redirect': True,
#                   'handle_httpstatus_list': [301]
#               }, dont_filter=True) 
#         
#         
# #nada
#     
# #    def parseURL(self, response):
#         
# 
#             
#         self.logger.info('** Init parseURL1 %s **',response.url)    
#             
#         #hxs = Selector(response)
#         products = response.xpath('//li[@class="data-product result result-with-button"]')
#         #products = hxs.xpath('///html/body/div[2]/div[3]/div[3]/div[3]/div[2]/ul/li[2]')
#         products = products + response.xpath('//li[@class="data-product result"]')
#         
#         items = []
#         for product in products:
#             item = UvinumItem()
#             item['cellar'] = product.xpath('@data-cellar').extract()
#             item['store'] = product.xpath('@data-store').extract()
#             item['category'] = product.xpath('@data-category').extract()
#             item['name'] = product.xpath('@data-name').extract()
#             item['source'] = product.xpath('@data-store').extract()
#             item['precio'] = product.xpath('normalize-space(.//*[@class="precio"]/text())').extract()
#             item['puntuacion'] = product.xpath('normalize-space(.//*[@class="nota"]/strong)').extract()
#             
#             #item['cellar'] = item['cellar'].encode('utf-8')
#             items.append(item)
#         return items #yield?
#     
# #    def parseURL2(self, response):
#         
#         self.logger.info('** Init parseURL2 %s **',response.url)    
#             
#         item = UvinumItem()
#         #xpath() devuelve selectores (nodos) seleccionados segun su argumento
#         #sobre los selectores se puede llamar xpath() otra vez
#         #extract() devuelve los datos de los selectores
#         item['name'] = response.xpath('normalize-space(.//*[@class="url"]/strong/text())').extract()
#         item['anada'] = response.xpath('normalize-space(.//*[@class="anadas"]/strong)').extract()
#         item['cellar'] = response.xpath('normalize-space(.//*[@class="maker"]/text())').extract()
#         item['DO'] = response.xpath('normalize-space(.//*[@class="appellation"]/dd/a/text())').extract()
#         item['tipo'] = response.xpath('normalize-space(.//*[@class="wine-type"]/dd/strong/text())').extract()
#         item['volumen'] = response.xpath('normalize-space(.//*[@class="tamanos"]/strong/text())').extract()
#         item['textogeneral'] = response.xpath('.//*[@class="maker-description"]').xpath('normalize-space(.//*[@itemprop])').extract()
#         #item['tipouvas'] = 
#         #item['alcohol'] = 
#         #item['notadecata'] =
#         item['notausuarios'] = response.xpath('normalize-space(.//*[@class="nota"]/strong)').extract()
#         item['alcohol'] = response.xpath('.//*[@class="attribute" and @title="Vol. de alcohol"]/following-sibling::dd[1]/text()').extract()
#         item['alergenos'] = response.xpath('.//*[@class="attribute" and @title="Alérgenos"]/following-sibling::dd[1]/text()').extract()
#         item['precio'] = response.xpath('normalize-space(.//*[@class="price"]/text())').extract()
#         item['store'] = response.xpath('normalize-space(.//*[@class="shipping_info"]/span/a/strong/text())').extract()
#         item['puntuacionrp'] = response.xpath('normalize-space(.//*[@class="guia_pk guide"]/text())').extract()
#         item['puntuaciongp'] = response.xpath('normalize-space(.//*[@class="guia_p guide"]/text())').extract()
#         #item['']
#         
#         #primero = response.xpath('.//*[@class="maker-description"]').xpath('normalize-space(.//*[@itemprop])').extract()[0].split(':')
#         #tercero = response.xpath('.//*[@class="maker-description"]').xpath('normalize-space(.//*[@itemprop])').extract()[0].split('-')
#         #item['tipouvas'] = primero[6].split('.')[0].split(' ')[1]
#         #item['alcohol'] = primero[7].split(' ')[1]
#         #item['notadecata'] =tercero[1]+tercero[2]+tercero[3].split('.')[0]
#             
#         return item
#             