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
        for url in region_urls:#iterando sobre las regiones
            os.environ['http_proxy']=self.proxy_pool[random.randint(0,len(self.proxy_pool)-1)]   
            region = str(url)[21:]#cortar de cada url el nombre de la region
            #self.logger.debug('** Region %s **',region)
                
            #construir la url de la lista de vinos con el filtro de la region        
            region_filter_url = "http://www.uvinum.es/vinos:k:"+region+":v:todos"
            print "I will go to", region_filter_url
        
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
        wine['nombre_del_vino'] = ''.join(response.xpath('//div[@class="product-title"]/h1/@title').extract())
        product = response.xpath('//div[@class="attributes-container"]')
        wine['bodega'] = ''.join(product.xpath('.//a[@class="bodegas"]/@title').extract())
        wine['tipo'] = ''.join(product.xpath('.//dl[@class="wine-type"]/dd/strong/text()').extract())
        wine['anada'] = ''.join(product.xpath('.//dd[@class="anadas"]/strong/text()').extract())
        wine['DO'] = ''.join(product.xpath('.//dl[@class="appellation"]/dd/a/text()').extract_first())
        wine['volumen'] = ''.join(product.xpath('.//dd[@class="tamanos"]/strong/text()').extract())
        #para evitar el problema del acento en alérgenos usamos una lista de nodos con condición de que lo que se
        #extraiga del nodo contenga "genos" y por lo tanto sea Alérgenos
        wine['alergenos'] = [x for x in product.xpath('.//dl') if "genos" in x.extract()][0].xpath('.//dd/text()').extract()
        wine['precio'] = response.xpath('//span[@itemprop="price"]/text()').extract_first()
#        wine['tipouvas'] = product.xpath('//p[@itemprop="description"]').extract()
#         if wine['tipouvas']!=[]:
#             if "UVAS" in wine['tipouvas'][0]:
#                 wine['tipouvas'] = wine['tipouvas'][0].split('UVAS')[1].split('BODEGA')[0]
#             else: #si no lo podemos sacar de la descripcion
#                 wine['tipouvas'] = product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract()
#         else: wine['tipouvas'] = product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract()
        tipouvas = ''.join(product.xpath('.//dt[@title="Uvas"]/../dd/a/strong/text()').extract())
        graduacion = ''.join(product.xpath('.//dt[@title="Vol. de alcohol"]/../dd/text()').extract())
        wine['puntuacionrp'] = ''.join(product.xpath('//dd[@class="guides"]/span[@class="guia_pk guide"]/text()').extract())
        wine['puntuacionws'] = ''.join(product.xpath('//dd[@class="guides"]/span[@class="guia_ws guide"]/text()').extract())
        wine['puntuacionrvf'] = ''.join(product.xpath('//dd[@class="guides"]/span[@class="guia_larvf guide"]/text()').extract())
        wine['puntuaciongp'] = ''.join(product.xpath('//dd[@class="guides"]/span[@class="guia_p guide"]/text()').extract())
        wine['nota_usuarios'] = ''.join(response.xpath('//div[@class="nota"]/p/strong[@itemprop="ratingValue"]/text()').extract())
        wine['numero_usuarios'] = ''.join(response.xpath('//div[@class="nota"]/meta[@itemprop="reviewCount"]/@content').extract())
        maridaje = ','.join(product.xpath('.//dl[@class="pairing"]/dd/a/strong/text()').extract())
        tempconsumo = ''.join(product.xpath('.//dt[@title="Temp. de consumo"]/../dd/text()').extract())
        
        notadecata = product.xpath('//p[@itemprop="description"]/text()').extract()
        #procesar la nota de cata:
        if notadecata:#los saltos de linea hacen que extract() obtenga cada parte de la nota de cata como un elemento de una lista
            notas = [x[3:] for x in notadecata if ("Vista" in x or "Nariz" in x or "Boca" in x)]#y cogemos los elementos de la lista que queramos
            if not notas:
                if ''.join(notadecata)[:12]=="NOTA DE CATA":#si la nota no esta en el formato Vista-Nariz-Boca, lo intentamos de nuevo
                    notas = ''.join(notadecata).split('\n')[1]
            wine['nota_de_cata'] = ''.join(x for x in notas)
            
            #aprovechar la info de porcentajes de uva si la hay
            uvas = [x[1:] for x in notadecata if "UVAS" in x]#cogemos solo la parte de uvas
            if uvas:
                tipouvas = ','.join(x for x in uvas).split(":")[1]
                
            #aprovechar la info de alcohol si la hay
            alcohol = [x[1:] for x in notadecata if "GRADUACI" in x]#evitando el acento de graduación
            if alcohol:
                graduacion = ''.join(x for x in alcohol).split(":")[1]
            #aprovechar la info de temperatura de consumo si la hay
            tconsumo = [x[1:] for x in notadecata if "TEMPERATURA DE CONSUMO" in x]
            if tconsumo:
                tempconusmo = ''.join(x for x in tconsumo).split(":")[1]
                
            #aprovechar la info de maridaje si la hay
            maridajes = [x[1:] for x in notadecata if "MARIDAJE" in x]
            if maridajes:
                maridaje = ','.join(x for x in maridajes).split(":")[1]
            
            #del envejecimiento o crianza    
            tipodecrianza = [x[1:] for x in notadecata if("ENVEJECIMIENTO" in x or "PERMANENCIA EN BARRICA" in x)]
            if tipodecrianza:
                wine['tipo_de_crianza'] = ''.join(x for x in tipodecrianza).split(":")[1]
                
        #los siguientes campos pueden obtenerse de dos formas distintas, por eso se almacenan primero en una variable que puede ser reescrita
        wine['tipo_de_uvas'] = tipouvas#p. ej. la variable tipouvas puede haber sido reescrita en la nota de cata, o ser el valor que se obtuvo antes
        wine['alcohol'] = graduacion
        wine['maridaje'] = maridaje
        wine['temperatura_de_consumo'] = tempconsumo
        
        #las fotos
        wine['image_urls'] = response.xpath('//a[@id="fancy_photo"]/@href').extract()
   
        with open("urls.txt","a") as f:
            f.write(response.url)
        return wine
