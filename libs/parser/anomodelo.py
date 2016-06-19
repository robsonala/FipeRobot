#!/usr/bin/env python
# coding=utf-8

from scrapy import *
from models.modelo import ModeloModel
from models.anomodelo import AnoModeloModel
from libs.utils import Utils
import json

class AnoModeloSpider(Spider):
	name, start_urls = "AnosModelo", ["http://"]

	rate = 2

	_db = None
	_model = None

	def __init__(self, db):
		self.download_delay = 1/float(self.rate)

		self._db = db
		self._model = AnoModeloModel(db)

	def parse(self, response):
		modelo = ModeloModel(self._db)

		ret = modelo.listAll(0,0,' AND hasCrawled=0 ')

		if ret['err'] is True:
			print modelo.getError()
		else:
			for item in ret['ret']['itens']:
				yield Request("http://www2.fipe.org.br/IndicesConsulta-ConsultarAnoModelo?codigoTabelaReferencia=%d&codigoTipoVeiculo=%d&codigoMarca=%d&codigoModelo=%d" % (item['codigoTabelaReferencia'], item['codigoTipoVeiculo'], item['codigoMarca'], item['codigoModelo']), 
					callback=self.execute, meta={'codigoModelo':item['codigoModelo'], 'codigoMarca':item['codigoMarca'], 'codigoTabelaReferencia':item['codigoTabelaReferencia'], 'codigoTipoVeiculo': item['codigoTipoVeiculo']})
	
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
				for item in jsonValue:
					value = Utils.toUTF8(item['Value'])
					label = Utils.toUTF8(item['Label'])

					print self._model.add(value, metas['codigoModelo'], metas['codigoMarca'], metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], label)
					
					countSaved = countSaved + 1

				if countSaved > 0:
					modelo = ModeloModel(self._db)
					modelo.setCrawled(metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], metas['codigoMarca'], metas['codigoModelo'])

		except e:
			print e
	# enddef