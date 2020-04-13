#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, tipologia riga dello schema'''
        tbl = pkg.table('sm_riga_tipo', pkey='id', lookup=True,
                name_long='!![it]Tipo riga',
                name_plural='!![it]Tipi riga',
                caption_field='codice')

        self.sysFields(tbl)

        tbl_codice=tbl.column('codice', dtype='A', size=':15', 
                name_long='!![it]Codice tipo riga',
                unique=True, validate_notnull=True, indexed=True)

        tbl_descrizione=tbl.column('descrizione', dtype='A', size=':64', 
                name_long='!![it]Descrizione classe', 
                validate_notnull=True)
