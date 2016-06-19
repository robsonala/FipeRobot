from libs.model import Model

class AnoModeloModel(Model):
	def __init__(self, db):
		Model.__init__(self, db)

		self._table = 'AnoModelo'
		self._selectItens = ['codigoAnoModelo','codigoModelo','codigoMarca','codigoTipoVeiculo','codigoTabelaReferencia','titulo','hasCrawled'] 

	def add(self, codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo):
		sql = "INSERT INTO %s (codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo) VALUES ('%s', %d, %d, %d, %d, '%s')"

		return self._db.execute(sql, (self._table, codigoAnoModelo, codigoModelo, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo))

	def setCrawled(self, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca, codigoModelo, codigoAnoModelo):
		sql = "UPDATE %s SET hasCrawled=1 WHERE codigoTipoVeiculo=%d AND codigoTabelaReferencia=%d AND codigoMarca=%d AND codigoModelo=%d AND codigoAnoModelo='%s'"

		return self._db.execute(sql, (self._table, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca, codigoModelo, codigoAnoModelo))