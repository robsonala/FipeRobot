#!/usr/bin/env python
# coding=utf-8

from scrapy import *
from models.anomodelo import AnoModeloModel
from models.versao import VersaoModel
from libs.utils import Utils
import json, re, random, time
import Queue

class VersaoSpider(Spider):
	name, start_urls = "Versao", ["http://"]

	rate = 2

	_db = None
	_model = None

	def __init__(self, db):
		self.download_delay = 1/float(self.rate)

		self._db = db
		self._model = VersaoModel(db)

	def proccessItem(self, item):	
		veiculo = ''
		if item['codigoTipoVeiculo'] == 1:
			veiculo = 'carro'
		elif item['codigoTipoVeiculo'] == 2:
			veiculo = 'moto'
		elif item['codigoTipoVeiculo'] == 3:
			veiculo = 'caminhao'

		(ano, combustivel) = item['codigoAnoModelo'].split('-')
		ano = int(ano)
		combustivel = int(combustivel)

		item['veiculo'] = veiculo
		item['ano'] = ano
		item['combustivel'] = combustivel

		return item

	def parse(self, response):
		anoModelo = AnoModeloModel(self._db)

		ret = anoModelo.listAll(1,50,' AND hasCrawled=0 ')

		if ret['err'] is True:
			print anoModelo.getError()
		else:
			for item in ret['ret']['itens']:
				item = self.proccessItem(item)

				yield Request("http://www2.fipe.org.br/IndicesConsulta-ConsultarValorComTodosParametros?codigoTabelaReferencia=%d&codigoTipoVeiculo=%d&codigoMarca=%d&codigoModelo=%d&anoModelo=%d&codigoTipoCombustivel=%d&tipoVeiculo=%s&modeloCodigoExterno=&tipoConsulta=tradicional" % (item['codigoTabelaReferencia'], item['codigoTipoVeiculo'], item['codigoMarca'], item['codigoModelo'], item['ano'], item['combustivel'], item['veiculo']), 
					callback=self.execute, meta={'codigoAnoModelo': item['codigoAnoModelo'], 'codigoModelo': item['codigoModelo'], 'codigoMarca': item['codigoMarca'], 'codigoTabelaReferencia': item['codigoTabelaReferencia'], 'codigoTipoVeiculo': item['codigoTipoVeiculo']})

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
				print "Deu erro :("
			else:
				countSaved = 0
				CodigoFipe = Utils.toUTF8(jsonValue['CodigoFipe'])
				Modelo = Utils.toUTF8(jsonValue['Modelo'])
				Valor = Utils.toUTF8(jsonValue['Valor'])

				try:
					Valor = float((re.sub("[^0-9,]+", "", Valor)).replace(",","."))
				except e:
					Valor = 0
	
				if Valor>0:
					print self._model.add(CodigoFipe, metas['codigoAnoModelo'], metas['codigoModelo'], metas['codigoMarca'], metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], Modelo, Valor)
					countSaved = countSaved + 1

				if countSaved > 0:
					anoModelo = AnoModeloModel(self._db)
					anoModelo.setCrawled(metas['codigoTipoVeiculo'], metas['codigoTabelaReferencia'], metas['codigoMarca'], metas['codigoModelo'], metas['codigoAnoModelo'])

		except e:
			print 'Except =>'
			print e
	# enddef