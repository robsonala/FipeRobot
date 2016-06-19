from libs.model import Model

class ModeloModel(Model):
	def __init__(self, db):
		Model.__init__(self, db)

		self._table = 'Modelo'
		self._selectItens = ['codigoModelo','codigoMarca','codigoTipoVeiculo','codigoTabelaReferencia','titulo','hasCrawled'] 

	def add(self, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo):
		sql = "INSERT INTO %s (codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo) VALUES (%d, %d, %d, %d, '%s')"

		return self._db.execute(sql, (self._table, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo))

	def setCrawled(self, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca, codigoModelo):
		sql = "UPDATE %s SET hasCrawled=1 WHERE codigoTipoVeiculo=%d AND codigoTabelaReferencia=%d AND codigoMarca=%d AND codigoModelo=%d"

		return self._db.execute(sql, (self._table, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca, codigoModelo))