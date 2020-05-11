#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, model connections'''
        tbl = pkg.table('si_bilver_01_model', pkey='id',
                name_long='!![it]Collegamenti modello',
                caption_field='code')

        self.sysFields(tbl)

        fk=tbl.column('sm_model__id', dtype='A', size=':22', 
                name_long='!![it]Codice modello',
                unique=True, validate_notnull=True)

        tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione collegamento')