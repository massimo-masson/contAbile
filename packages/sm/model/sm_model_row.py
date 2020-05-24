#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, model rows'''
        tbl = pkg.table('sm_model_row', pkey='id', 
                name_long='!![it]Riga modello',
                name_plural='!![it]Righe modello',
                caption_field='code')

        self.sysFields(tbl)

        tbl_code=tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Riga modello',
                unique=True, validate_notnull=True, indexed=True)

        tbl_description=tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione riga', 
                validate_notnull=True)

        # TODO: tipo riga indica la modalita' di visualizzazione del dato
        # nelle colonne. Penso ai seguenti tipi:
        # desc = descrittiva: marcatore di riga, nessun valore nelle colonne
        # data = dati: il dato visualizzato nella cella della colonna va recuperato
        #       dalla tabella dati
        # formula = calcolata: il dato visualizzato deriva da una formula
        tbl.column('row_type', dtype='A', size=':22',
                name_long='!![it]Tipo riga',
                validate_notnull=True)

        tbl_position=tbl.column('position', dtype='N', 
                name_long='!![it]Posizione riga')

        tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # sm_anagrafica: foreign key to sm_anagrafica
        tbl_sm_model__id=tbl.column('sm_model__id', dtype='A', size='22',
                name_long='!![it]Anagrafica modello',
                validate_notnull=True)
        tbl_sm_model__id.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='rows',
                onDelete='raise')

    def CONST_row_type(self):
        '''Return the constant values for the "row_type" field.
            In reference to the value of the destination cell:
            desc: description
            data: data
            formula: formula
        '''
        CONST = 'data:Dati,desc:Descrizione,formula:Formula'
        return CONST