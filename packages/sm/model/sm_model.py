#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, models'''
        tbl = pkg.table('sm_model', pkey='id', 
                name_long='!![it]Modello di schema',
                name_plural='!![it]Modelli di schemi',
                caption_field='code')

        self.sysFields(tbl)

        tbl_code=tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice modello',
                unique=True, validate_notnull=True, indexed=True)

        tbl_description=tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione modello', 
                validate_notnull=True)

        tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # foreign key to sm_category
        tbl_category_id=tbl.column('sm_category_id', dtype='A', size='22',
                name_long='!![it]Categoria schema',
                validate_notnull=True)
        tbl_category_id.relation('sm.sm_category.id', mode='foreignkey',
                relation_name='models',
                onDelete='raise')
