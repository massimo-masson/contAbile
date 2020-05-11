#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, bilancio verifica tipo 1'''
        tbl = pkg.table('si_bilver_01_lot', pkey='lot_code',
                name_long='!![it]Lotto importazione bilancio di verifica',
                name_plural='!![it]Lotti importazione bilancio di verifica',
                caption_field='lot_code')

        self.sysFields(tbl)

        tbl.column('lot_code', dtype='A', size=':22', 
                name_long='!![it]Codice lotto importazione',
                unique=True, validate_notnull=True)

        tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione lotto importazione')
