#!/usr/bin/env python
# coding=utf-8

from scrapy import *
from models.marca import MarcaModel
from models.modelo import ModeloModel
from libs.utils import Utils
import json

class ModeloSpider(Spider):
	name, start_urls = "Modelos", ["http://"]

	rate = 2

	_db = None
	_model = None

	def __init__(self, db):
		self.download_delay = 1/float(self.rate)

		self._db = db
		self._model = ModeloModel(db)

	def parse(self, response):
		marca = MarcaModel(self._db)

		ret = marca.listAll(0,0,' AND hasCrawled=0 ')

		if ret['err'] is True:
			print marca.getError()
		else:
			for item in ret['ret']['itens']:
				yield Request("http://www2.fipe.org.br/IndicesConsulta-ConsultarModelos?codigoTabelaReferencia=%d&codigoTipoVeiculo=%d&codigoMarca=%d" % (item['codigoTabelaReferencia'], item['codigoTipoVeiculo'], item['codigoMarca']), 
					callback=self.execute, meta={'codigoMarca':item['codigoMarca'], 'codigoTabelaReferencia':item['codigoTabelaReferencia'], 'codigoTipoVeiculo': item['codigoTipoVeiculo']})
	
	# enddef

	def execute(self, response):
		metas = response.meta

		try: 
			jsonValue = json.loads(response.body)

			print response.url
			print response.status
			print len(jsonValue)
			print "---"

			if 'erro' in jsonValue:
				print jsonValue
			else:
				countSaved = 0
				for item in jsonValue['Modelos']:
					value = int(Utils.toUTF8(item['Value']))
					label = Utils.toUTF8(item['Label'])

					print self._model.add(value, metas['codigoMarca'], metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], label)
					
					countSaved = countSaved + 1

				if countSaved > 0:
					marca = MarcaModel(self._db)
					marca.setCrawled(metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], metas['codigoMarca'])

		except e:
			print e
	# enddef