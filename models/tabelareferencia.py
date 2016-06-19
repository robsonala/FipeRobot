from libs.model import Model

class TabelaReferenciaModel(Model):
	def __init__(self, db):
		Model.__init__(self, db)

		self._table = 'TabelaReferencia'
		self._selectItens = ['codigoTabelaReferencia','codigoTipoVeiculo','titulo','hasCrawled'] 

	def add(self, codigoTabelaReferencia, codigoTipoVeiculo, titulo):
		sql = "INSERT INTO %s (codigoTabelaReferencia, codigoTipoVeiculo, titulo) VALUES (%d, %d, '%s')"

		return self._db.execute(sql, (self._table, codigoTabelaReferencia, codigoTipoVeiculo, titulo))

	def setCrawled(self, codigoTipoVeiculo, codigoTabelaReferencia):
		sql = "UPDATE %s SET hasCrawled=1 WHERE codigoTipoVeiculo=%d AND codigoTabelaReferencia=%d"

		return self._db.execute(sql, (self._table, codigoTipoVeiculo, codigoTabelaReferencia))