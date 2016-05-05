# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UvinumItem(scrapy.Item):
    # define the fields for your item here like:
    
    nombre_del_vino = scrapy.Field()#
    bodega = scrapy.Field()#
    DO = scrapy.Field()#
    anada = scrapy.Field()#
    tipo = scrapy.Field()#
    volumen = scrapy.Field()#
    tipo_de_uvas = scrapy.Field()#
    alcohol = scrapy.Field()#
    alergenos = scrapy.Field()#
    tipo_de_crianza = scrapy.Field()#
    maridaje = scrapy.Field()#
    temperatura_de_consumo = scrapy.Field()#
    
    precio = scrapy.Field()#
    
    #puntuaciones de guias/criticos
    puntuacionrp = scrapy.Field()#sobre 100
    puntuacionws = scrapy.Field()#sobre 100
    puntuacionrvf = scrapy.Field()#sobre 20
    puntuaciongp = scrapy.Field()#sobre 100
    
    nota_usuarios = scrapy.Field()#sobre 5
    numero_usuarios = scrapy.Field()
    
    nota_de_cata = scrapy.Field()
    #textogeneral = scrapy.Field()
    #crianza = scrapy.Field()#
    #ean = scrapy.Field()
    #consumopreferente = scrapy.Field()#
    #vinopremium = scrapy.Field()
    #tipodedisponibilidad = scrapy.Field()
    #afinidadpersonalizada = scrapy.Field()#
    #store = scrapy.Field()
    
    #los campos de imagen deben llamarse así para que funcione el Image Pipeline que las obtiene
    image_urls = scrapy.Field()#
    images = scrapy.Field()#
    