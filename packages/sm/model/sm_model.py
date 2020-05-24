#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, models'''
        tbl = pkg.table('sm_model', pkey='id', 
                name_long='!![it]Modello di schema',
                name_plural='!![it]Modelli di schemi',
                caption_field='code')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22',
                unmodifiable=True,
                name_long='!![it]Codice modello',
                unique=True, validate_notnull=True, indexed=True)

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione modello', 
                validate_notnull=True)

        tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # foreign key to sm_category
        tbl_category__id=tbl.column('sm_category__id', dtype='A', size='22',
                name_long='!![it]Categoria schema',
                validate_notnull=True)
        tbl_category__id.relation('sm.sm_category.id', mode='foreignkey',
                relation_name='models',
                onDelete='raise')

        tbl.column('dynamic_rows', dtype='B', default=False, 
                name_long='!![it]Righe dinamiche', 
                name_short='!![it]Righe dinamiche')

        tbl.column('dynamic_cols', dtype='B', default=False, 
                name_long='!![it]Colonne dinamiche', 
                name_short='!![it]Colonne dinamiche')

    def getStructBagFromModel(self, model):
        structBag = Bag()
        
        # model columns
        model_cols = self.db.table('sm.sm_model_col').query(
                columns='$code, $description',
                where='$sm_model__id=:model__id', model__id=model,
                order_by='$position'
                ).fetch()

        # first two columns, fixed:
        # code: row code
        # description: row description
        # view_0 is "magic" (legacy)
        cols = structBag['view_0.rows_0'] = Bag()
        cols.addItem('code', None, name='!![it]Codice', width='6em')
        cols.addItem('description',None, name='!![it]Descrizione',width='20em')

        # add model columns from model
        for c in model_cols:
                cols.addItem(c['code'], None, name=c['description'], width='10em')
        
        return structBag
