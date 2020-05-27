#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, model formula'''
        tbl = pkg.table('sm_model_formula', pkey='id', 
                name_long='!![it]Formula cella',
                name_plural='!![it]Formule modello',
                caption_field='caption')

        self.sysFields(tbl)

        # foreign key to model
        fk_row = tbl.column('sm_model__id', dtype='A', size='22',
                name_long='!![it]Modello',
                validate_notnull=True)
        fk_row.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='model_formula',
                onDelete='raise')

        # foreign key to schema row
        fk_row = tbl.column('sm_model_row__id', dtype='A', size='22',
                name_long='!![it]Riga modello',
                validate_notnull=True)
        fk_row.relation('sm.sm_model_row.id', mode='foreignkey',
                relation_name='model_formula',
                onDelete='raise')

        # foreign key to schema column
        fk_col = tbl.column('sm_model_col__id', dtype='A', size='22',
                name_long='!![it]Colonna modello',
                validate_notnull=True)
        fk_col.relation('sm.sm_model_col.id', mode='foreignkey',
                relation_name='model_formula',
                onDelete='raise')

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione formula')

        tbl.column('formula', dtype='A', size=':2048', 
                name_long='!![it]Formula', 
                validate_notnull=True)

        tbl.formulaColumn('caption', '@sm_model_row__id.code||","||@sm_model_col__id.code',
                name_long='!![it]Cella di riferimento')