#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, righe collegamento a modello'''
        tbl = pkg.table('si_bilver_01_model_link', pkey='id',
                name_long='!![it]Regola collegamento modello',
                caption_field='ext_description')

        self.sysFields(tbl)

        fk = tbl.column('si_bilver_01_model__code', dtype='A', size=':22', 
                name_long='!![it]Modello di impostazione',
                validate_notnull=True)
        fk.relation('sm.si_bilver_01_model.code', relation_name='bilver_01_links', 
                    mode='foreignkey', onDelete='raise')

        # fk = tbl.column('si_bilver_01_model__id', dtype='A', size=':22', 
        #         name_long='!![it]Modello di riferimento',
        #         validate_notnull=True)
        # fk.relation('sm.si_bilver_01_model.id', relation_name='bilver_01_links', 
        #             mode='foreignkey', onDelete='raise')

        tbl.column('ext_code', dtype='A', size=':22', 
                name_long='!![it]Codice esterno riga',
                validate_notnull=True)

        tbl.column('ext_description', dtype='A', size=':256',
                name_long='!![it]Descrizione esterna riga')

        # model row
        fk = tbl.column('sm_model_row__id', dtype='A', size=':22', 
                name_long='!![it]Riga modello collegata',
                validate_notnull=True)
        fk.relation('sm.sm_model_row.id', relation_name='bilver_01_links', 
                    mode='foreignkey', onDelete='raise')

        # model col
        fk = tbl.column('sm_model_col__id', dtype='A', size=':22', 
                name_long='!![it]Colonna modello collegata',
                validate_notnull=True)
        fk.relation('sm.sm_model_col.id', relation_name='bilver_01_links', 
                    mode='foreignkey', onDelete='raise')
