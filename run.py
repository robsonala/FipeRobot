#!/usr/bin/env python
# coding=utf-8

import sys, getopt

from libs.db import DB

def runParser(arg):
	from twisted.internet import reactor
	from scrapy.crawler import Crawler
	from scrapy import log, signals, Spider
	from scrapy.utils.project import get_project_settings

	from libs.parser.tabelareferencia import TabelaReferenciaSpider
	from libs.parser.marca import MarcaSpider
	from libs.parser.modelo import ModeloSpider
	from libs.parser.anomodelo import AnoModeloSpider
	from libs.parser.versao import VersaoSpider
	
	db = DB()

	spider = None
	if arg == "tabelareferencia":
		spider = TabelaReferenciaSpider(db)
	if arg == "marca":
		spider = MarcaSpider(db)
	if arg == "modelo":
		spider = ModeloSpider(db)
	if arg == "anomodelo":
		spider = AnoModeloSpider(db)
	if arg == "versao":
		spider = VersaoSpider(db)

	if spider is None:
		print 'Parser não encontrado ->' + arg
		sys.exit(2)

	crawler = Crawler(get_project_settings())
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()
	#log.start()
	reactor.run()

def getAll(arg):
	from models.tabelareferencia import TabelaReferenciaModel
	from models.marca import MarcaModel
	from models.modelo import ModeloModel
	from models.anomodelo import AnoModeloModel
	from models.versao import VersaoModel
	
	db = DB()
	
	model = None
	if arg == "tabelareferencia":
		model = TabelaReferenciaModel(db)
	if arg == "marca":
		model = MarcaModel(db)
	if arg == "modelo":
		model = ModeloModel(db)
	if arg == "anomodelo":
		model = AnoModeloModel(db)
	if arg == "versao":
		model = VersaoModel(db)

	if model is None:
		print 'Model não encontrado'
		sys.exit(2)

	ret = model.listAll(0,10)

	if ret['err'] is True:
		print model.getError()
	else:
		print ret

def main(argv):

	try:
		opts, args = getopt.getopt(argv,"hp:l:",["parser=","list="])
	except getopt.GetoptError:
		print '[FILE].py -p <model> -list<model>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print '[FILE].py -p <model> -list<model>'
			sys.exit()
		elif opt in ("-p", "--parser"):
			runParser(arg)
		elif opt in ("-l", "--list"):
			getAll(arg)


if __name__ == '__main__':
	main(sys.argv[1:])