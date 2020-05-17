#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, model connections'''
        tbl = pkg.table('si_bilver_01_model', pkey='code',
                name_long='!![it]Collegamenti modello',
                caption_field='description')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22',
                name_long='!![it]Codice modello importazione',
                unmodifiable=True,
                unique=True, validate_notnull=True)
        
        tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione modello importazione')

        fk=tbl.column('sm_model__id', dtype='A', size=':22', 
                name_long='!![it]Codice modello',
                validate_notnull=True)
        fk.relation('sm.sm_model.id', relation_name='bilver_01_models',
                    mode='foreignkey', onDelete='raise')