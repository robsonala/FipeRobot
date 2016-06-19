#!/usr/bin/env python
# coding=utf-8

from scrapy import *
from models.tabelareferencia import TabelaReferenciaModel
from libs.utils import Utils

class TabelaReferenciaSpider(Spider):
	name, start_urls = "TabelaReferencia", ["http://"]

	_DOMtree = None
	_db = None
	_model = None

	def __init__(self, db):
		self._db = db
		self._model = TabelaReferenciaModel(db)

	def parse(self, response):
		return Request("http://www2.fipe.org.br/pt-br/indices/veiculos", callback=self.execute)
	# enddef

	def execute(self, response):
		self._DOMtree = response

		self.parseById(1, 'selectTabelaReferenciacarro')
		self.parseById(2, 'selectTabelaReferenciamoto')
		self.parseById(3, 'selectTabelaReferenciacaminhao')
	# enddef

	def parseById(self, tipoVeiculo, id):
		for sel in self._DOMtree.xpath('//select[@id="%s"]/option' % (id)):
			text = sel.xpath('text()').extract()
			value = sel.xpath('@value').extract()

			if type(text).__name__ == 'list':
				text = text[0]

			if type(value).__name__ == 'list':
				value = value[0]
				
			value = int(Utils.toUTF8(value))
			text = str(Utils.toUTF8(text))

			print self._model.add(value, tipoVeiculo, text)
		# endfor
	# enddef