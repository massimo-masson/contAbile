#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, tipologia riga dello schema'''
        tbl = pkg.table('sm_row_type', pkey='id', lookup=True,
                name_long='!![it]Tipo riga',
                name_plural='!![it]Tipi riga',
                caption_field='code')

        self.sysFields(tbl)

        tbl_code=tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice tipo riga',
                unique=True, validate_notnull=True, indexed=True)

        tbl_description=tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione tipo riga', 
                validate_notnull=True)
