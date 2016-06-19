#!/usr/bin/env python
# coding=utf-8

import MySQLdb, sys
from libs.config import Config
from libs.utils import Utils

class DB(object):
    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __conn = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
             cls.__instance = super(DB, cls).__new__(cls,*args,**kwargs)
        return cls.__instance
    ## End def __new__

    def __init__(self):
        __config = Config()
        
        self.__host     = __config.get('MySQL','Host')
        self.__user     = __config.get('MySQL','User')
        self.__password = __config.get('MySQL','Pass')
        self.__database = __config.get('MySQL','Base')

        try:
            self.__conn = MySQLdb.connect(self.__host, self.__user, self.__password, self.__database)
        except MySQLdb.Error as e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    ## End def __init__

    def __del__(self):
        self.__conn.close()

    def select(self, cmd, params = ()):
        result = None
        cur = None

        try:
            newParams = ()
            for item in params:
                newParams = newParams + (self.__conn.escape_string(item) if isinstance(item, str) else item,)

            cur = self.__conn.cursor()
            cur.execute(cmd % newParams)

            number_rows = cur.rowcount
            number_columns = len(cur.description)
            name_columns = [column[0] for column in cur.description]

            if number_rows >= 1 and number_columns > 1:
                result = [dict(zip(name_columns, item)) for item in cur.fetchall()]
            else:
                result = [dict(zip(name_columns, item[0]))  for item in cur.fetchall()]
            
            result = {'total': number_rows, 'itens': result}
            result = Utils.structReturn(False, result)

        except MySQLdb.Error, e:
            result = Utils.structReturn(True, "Error %d: %s" % (e.args[0],e.args[1]))
        finally:
            if cur:
                cur.close()

        return result
    ## enddef

    def execute(self, cmd, params = ()):
        result = None

        try:
            newParams = ()
            for item in params:
                newParams = newParams + (self.__conn.escape_string(item) if isinstance(item, str) else item,)

            cur = self.__conn.cursor()

            cur.execute(cmd % newParams)
            self.__conn.commit()

            result = Utils.structReturn(False, {'total': cur.rowcount if hasattr(cur, 'rowcount') else 0, 'id': self.__conn.lastrowid if hasattr(self.__conn,'lastrowid') else 0})

        except MySQLdb.Error, e:
            result = Utils.structReturn(True, "Error %d: %s" % (e.args[0],e.args[1]))
        finally:
            if cur:
                cur.close()

        return result
    ## enddef
## End class
