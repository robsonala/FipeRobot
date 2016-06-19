#!/usr/bin/env python
# coding=utf-8

import ConfigParser

class Config():
	cfg = None

	def __init__(self):
		try:
			self.cfg = ConfigParser.ConfigParser()
			self.cfg.read("libs/config.cfg")
		except Exception, e:
			raise
		finally:
			pass

	def get(self, section, key):
		return self.cfg.get(section, key)