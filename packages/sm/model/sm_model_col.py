#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, model column'''
        tbl = pkg.table('sm_model_col', pkey='id', 
                name_long='!![it]Colonna modello',
                name_plural='!![it]Colonne modello',
                caption_field='code')

        self.sysFields(tbl)

        tbl_code=tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Colonna modello',
                unique=True, validate_notnull=True, indexed=True)

        tbl_description=tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione colonna', 
                validate_notnull=True)

        # TODO: da sistemare la gestione del tipo di campo
        tbl_field_type=tbl.column('field_type', dtype='A', size=':22', 
                name_long='!![it]tipo campo')

        tbl_position=tbl.column('position', dtype='N', 
                name_long='!![it]posizione colonna')

        tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # sm_anagrafica: foreign key to sm_anagrafica
        tbl_sm_model_id=tbl.column('sm_model_id', dtype='A', size='22',
                name_long='!![it]Anagrafica modello',
                validate_notnull=True)
        tbl_sm_model_id.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='columns',
                onDelete='raise')
