#!/usr/bin/env python
# coding=utf-8
from libs.utils import Utils

class Model(object):
	_db = None
	_table = None
	_selectItens = list()
	_error = None
	_id = None

	def __init__(self, db):
		self._db = db

	def __setError(self, msg):
		self._error = msg

	def getError(self):
		return self._error

	def __setId(self, id):
		self._id = id

	def getId(self):
		return self._id

	def __listAllBase(self, showDeleted, page = 1, tpp = 50, search = ''):
		params = (','.join(self._selectItens), self._table, ('1=1' if showDeleted else 'ativo=1'), search)

		sql = "SELECT %s FROM %s WHERE %s %s"
		result = self._db.select(sql, params)

		if result['err'] is True:
			self.__setError(result['ret'])
			return Utils.structReturn(True, 0)
		else:
			total = result['ret']['total']
			totalpag = 0
			if page > 0:
				ini = (page * tpp) - tpp
				if ini <= 0:
					ini = 0

				sql += " LIMIT %d, %d "
				params = params + (ini, tpp)

				result = self._db.select(sql, params)

				totalpag = result['ret']['total']
			## endif

			if (total and not page) or (totalpag and page):
				return result
			else:
				self.__setError("Nenhum dado encontrado!")
				return Utils.structReturn(True, 0)
			## endif
		## endif
	## enddef

	def listAll(self, page = 1, tpp = 50, search = ''):
		return self.__listAllBase(True, page, tpp, search)

	def listAllActive(self, page = 1, tpp = 50, search = ''):
		return self.__listAllBase(False, page, tpp, search)

	def get(self, id):
		if not id:
			return False

		sql = "SELECT %s FROM %s WHERE id = %d"
		result = self._db.select(sql, [','.join(self._selectItens), self._table, id])

		if result['err'] is True:
			self.__setError(result['ret'])
			return Utils.structReturn(True, 0)
		else:
			if result['ret']['total'] > 0:
				return Utils.structReturn(False, result['ret']['itens'])
			else:
				self.__setError("Nenhum dado encontrado!")
				return Utils.structReturn(True, 0)
			## endif
		## endif
	## enddef

	def delete(self, id):
		if str(id).find(",") != -1:
			sql = "UPDATE %s SET ativo = 0 WHERE id IN (%s)"
		else:
			sql = "UPDATE %s SET ativo = 0 WHERE id = %d"

		return self._db.execute(sql, [self._table, id])
	## enddef

	def restore(self, id):
		if str(id).find(",") != -1:
			sql = "UPDATE %s SET ativo = 1 WHERE id IN (%s)"
		else:
			sql = "UPDATE %s SET ativo = 1 WHERE id = %d"

		return self._db.execute(sql, [self._table, id])
	## enddef