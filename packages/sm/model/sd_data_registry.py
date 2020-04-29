#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gnr.core.gnrbag import Bag

class Table(object):
        def config_db(self, pkg):
                '''sd: schema data, registry of schema'''
                tbl = pkg.table('sd_data_registry', pkey='id', 
                        name_long='!![it]Anagrafica schema',
                        name_plural='!![it]Anagrafiche schemi',
                        caption_field='code')

                self.sysFields(tbl)

                tbl_code=tbl.column('code', dtype='A', size=':22',
                        unmodifiable=True,      # can set code only on new record
                        name_long='!![it]Codice schema',
                        unique=True, validate_notnull=True, indexed=True)
                
                tbl_description=tbl.column('description', dtype='A', size=':256', 
                        name_long='!![it]Descrizione schema')
                
                tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                        name_long='!![it]Note')

                # model reference
                tbl_sm_model_id=tbl.column('sm_model_id', size='22',
                        name_long='!![it]Modello di riferimento',
                        validate_notnull=True
                        )
                tbl_sm_model_id.relation('sm.sm_model.id', mode='foreignkey',
                        relation_name='registry',
                        onDelete='raise'
                        )

                # local data
                tbl_storebag=tbl.column('storebag', dtype='X', 
                        name_long='!![it]StoreBag')

                # # foreign key to store
                # tbl_sd_data_store_id=tbl.column('sd_data_store_id', size='22',
                #         name_long='!![it]Dati',
                #         validate_notnull=True)
                # tbl_sd_data_store_id.relation('sm.sd_data_store.id', mode='foreignkey',
                #         one_one=True,
                #         relation_name='registry',
                #         onDelete='raise')
                
                #status: vuoto, elaborabile, elaborato
                tbl_status=tbl.column('status', dtype='A', size=':22',
                        default='EMPTY',
                        name_long='!![it]Stato schema')

                tbl_is_protected=tbl.column('is_protected', dtype='B', 
                        name_long='!![it]Protetto')

                # date e periodo di riferimento        
                tbl_date_ref_from=tbl.column('date_ref_from', dtype='D', 
                        name_long='!![it]Data da') #, validate_notnull=True)

                tbl_date_ref_to=tbl.column('date_ref_to', dtype='D', 
                        name_long='!![it]Data a') #, validate_notnull=True)

                tbl_date_ref_period=tbl.column('date_ref_period', dtype='A', size=':22',
                        name_long='!![it]Periodo di riferimento', validate_notnull=True)

        def trigger_onInserted(self, record=None):
                self.buildUpStoreBag(record)

        def buildUpStoreBag(self, record=None):
                '''Make a storage schema based on selected model'''
                testbag = Bag()
                righe=('riga1', 'riga2', 'riga3', 'riga4')
                colonne=('col1','col2')
                for r in righe:
                        testbag[r]=Bag()
                        for c in colonne:
                                testbag[r][c]=f'{r}:{c}'

                with self.recordToUpdate(record['id']) as currentRecord:
                        currentRecord['storebag']=testbag
                        currentRecord['status']='ELABORABILE'