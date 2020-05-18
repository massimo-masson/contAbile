#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, class for parameter'''
        tbl = pkg.table('sm_parameter_class', pkey='id', lookup=True,
                name_long='!![it]Classe del parametro',
                name_plural='!![it]Classi dei parametri',
                caption_field='code')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice tipo parametro',
                unique=True, validate_notnull=True, indexed=True)

        tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione classe parametro'
                )
