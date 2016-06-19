#!/usr/bin/env python
# coding=utf-8

from scrapy import *
from models.marca import MarcaModel
from models.tabelareferencia import TabelaReferenciaModel
from libs.utils import Utils
import json

class MarcaSpider(Spider):
	name, start_urls = "Marcas", ["http://"]

	rate = 2

	_db = None
	_model = None

	def __init__(self, db):
		self.download_delay = 1/float(self.rate)

		self._db = db
		self._model = MarcaModel(db)

	def parse(self, response):
		tabelaReferencia = TabelaReferenciaModel(self._db)

		ret = tabelaReferencia.listAll(0,0,' AND hasCrawled=0 ')

		if ret['err'] is True:
			print tabelaReferencia.getError()
		else:
			for item in ret['ret']['itens']:
				yield Request("http://www2.fipe.org.br/IndicesConsulta-ConsultarMarcas?codigoTabelaReferencia=%d&codigoTipoVeiculo=%d" % (item['codigoTabelaReferencia'], item['codigoTipoVeiculo']), 
					callback=self.execute, meta={'codigoTabelaReferencia':item['codigoTabelaReferencia'], 'codigoTipoVeiculo': item['codigoTipoVeiculo']})
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
					value = int(Utils.toUTF8(item['Value']))
					label = Utils.toUTF8(item['Label'])
					
					countSaved = countSaved + 1;

					print self._model.add(value, metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], label)

				if countSaved > 0:
					tabelaReferencia = TabelaReferenciaModel(self._db)
					print tabelaReferencia.setCrawled(metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'])
		except e:
			print e
	# enddef