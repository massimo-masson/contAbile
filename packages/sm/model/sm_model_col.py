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

        tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Colonna modello', #unique=True,
                validate_notnull=True, indexed=True)

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione colonna', 
                validate_notnull=True)

        # TODO: da sistemare la gestione del tipo di campo
        tbl.column('field_type', dtype='A', size=':22', 
                name_long='!![it]tipo campo')

        tbl.column('position', dtype='N', 
                name_long='!![it]posizione colonna')

        tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # sm_anagrafica: foreign key to sm_anagrafica
        tbl_sm_model__id=tbl.column('sm_model__id', dtype='A', size='22',
                name_long='!![it]Anagrafica modello',
                validate_notnull=True)
        tbl_sm_model__id.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='columns',
                onDelete='raise')

    def validateCodeUniquePerModel(self, record = None):
        '''code must be unique inside a single model'''

        duplicated = False

        rs = self.db.table('sm.sm_model_col').query(
            columns = '$id, $code, $description',
            where = '@sm_model__id.id = :current_model \
                    AND $code = :current_code',
            current_model = record['sm_model__id'],
            current_code = record['code']
        ).fetch()

        if len(rs) > 0:
            duplicated = True

        return duplicated

    def trigger_onInserting(self, record):
        if self.validateCodeUniquePerModel(record) == True:
            raise self.exception('protect_validate', record = record,
                                msg = '!![it]Codice colonna duplicato nel modello'
        )

    def trigger_onInserted(self, record = None):
        self.db.table('sm.sm_model').formulasSyncronize(record['sm_model__id'])

    def trigger_onUpdated(self, record = None, old_record = None):
        self.db.table('sm.sm_model').formulasSyncronize(record['sm_model__id'])

    def trigger_onDeleted(self, record = None):
        self.db.table('sm.sm_model').formulasSyncronize(record['sm_model__id'])
