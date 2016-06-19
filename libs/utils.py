#!/usr/bin/env python
# coding=utf-8

class Utils(object):

	@staticmethod
	def structReturn(err, ret):
		return {
			'err': err,
			'ret': ret
		}

	@staticmethod
	def toUTF8(value):
		if type(value).__name__ != "unicode":
			return value

		try:
			return value.encode('utf-8')
		except e:
			return value