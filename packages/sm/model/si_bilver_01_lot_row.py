#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, righe bilancio verifica tipo 01, per lotto'''
        tbl = pkg.table('si_bilver_01_lot_row', pkey='id',
                name_long='!![it]Riga bilancio per lotto',
                caption_field='ext_code')

        self.sysFields(tbl)

        tbl.column('ext_code', dtype='A', size=':22', 
                name_long='!![it]Codice esterno riga',
                validate_notnull=True)

        tbl.column('ext_description', dtype='A', size=':256',
                name_long='!![it]Descrizione esterna riga')

        tbl.column('ext_value', dtype='N', name_long='!![it]Valore')

        fk = tbl.column('si_bilver_01_lot__lot_code',size='22', group='_', 
                    name_long='!![it]Lotto importazione',
                    validate_notnull=True
                    )
        fk.relation('sm.si_bilver_01_lot.lot_code', relation_name='bilver_01_rows', 
                    mode='foreignkey', onDelete='raise')