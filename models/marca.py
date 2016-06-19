from libs.model import Model

class MarcaModel(Model):
	def __init__(self, db):
		Model.__init__(self, db)

		self._table = 'Marca'
		self._selectItens = ['codigoMarca','codigoTipoVeiculo','codigoTabelaReferencia','titulo','hasCrawled'] 

	def add(self, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo):
		sql = "INSERT INTO %s (codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo) VALUES (%d, %d, %d, '%s')"

		return self._db.execute(sql, (self._table, codigoMarca, codigoTipoVeiculo, codigoTabelaReferencia, titulo))

	def setCrawled(self, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca):
		sql = "UPDATE %s SET hasCrawled=1 WHERE codigoTipoVeiculo=%d AND codigoTabelaReferencia=%d AND codigoMarca=%d"

		return self._db.execute(sql, (self._table, codigoTipoVeiculo, codigoTabelaReferencia, codigoMarca))