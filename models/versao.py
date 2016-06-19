from libs.model import Model

class VersaoModel(Model):
	def __init__(self, db):
		Model.__init__(self, db)

		self._table = 'Versao'
		self._selectItens = ['codigoFipe', 'codigoAnoModelo','codigoModelo','codigoMarca','codigoTipoVeiculo','codigoTabelaReferencia','titulo','valor'] 

	def add(self, codigoFipe, codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo, valor):
		sql = "INSERT INTO %s (codigoFipe, codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo, valor) VALUES ('%s', '%s', %d, %d, %d, %d, '%s', %f)"

		return self._db.execute(sql, (self._table, codigoFipe, codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo, valor))