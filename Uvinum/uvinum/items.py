# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UvinumItem(scrapy.Item):
    # define the fields for your item here like:
    
    cellar = scrapy.Field()#
    store = scrapy.Field()
    name = scrapy.Field()#
    precio = scrapy.Field()#
    anada = scrapy.Field()#
    tipo = scrapy.Field()#
    puntuacionrp = scrapy.Field()#sobre 100
    puntuacionws = scrapy.Field()#sobre 100
    puntuacionrvf = scrapy.Field()#sobre 20
    puntuaciongp = scrapy.Field()#
    notausuarios = scrapy.Field()#sobre 5
    numerovotos = scrapy.Field()
    DO = scrapy.Field()#
    volumen = scrapy.Field()#
    tipouvas = scrapy.Field()#
    alcohol = scrapy.Field()#
    alergenos = scrapy.Field()#
    notadecata = scrapy.Field()
    textogeneral = scrapy.Field()
    foto = scrapy.Field()
    crianza = scrapy.Field()#
    ean = scrapy.Field()
    tipodecrianza = scrapy.Field()#
    maridaje = scrapy.Field()#
    consumopreferente = scrapy.Field()#
    vinopremium = scrapy.Field()
    tipodedisponibilidad = scrapy.Field()
    temperaturaconsumo = scrapy.Field()#
    afinidadpersonalizada = scrapy.Field()#
    