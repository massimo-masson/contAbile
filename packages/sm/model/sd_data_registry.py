#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, registry of schema'''
        tbl = pkg.table('sd_data_registry', pkey='id', 
                name_long='!![it]Anagrafica schema',
                name_plural='!![it]Anagrafiche schemi',
                caption_field='code_description')

        self.sysFields(tbl)

        tbl_code=tbl.column('code', dtype='A', size=':22',
                unmodifiable=True,      # can set code only on new record
                name_long='!![it]Codice schema',
                unique=True, validate_notnull=True, indexed=True)
        
        tbl_description=tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione schema')

        tbl_code_description=tbl.formulaColumn('code_description', 
                '"("||$code||") - "||$description', name_long='!![it]Schema')
        
        tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        # model reference
        tbl_sm_model__id=tbl.column('sm_model__id', size='22',
                unmodifiable=True,
                name_long='!![it]Modello',
                validate_notnull=True
                )
        tbl_sm_model__id.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='registry',
                onDelete='raise'
                )

        tbl_model_category=tbl.aliasColumn('model_category',
                relation_path='@sm_model__id.@sm_category__id.description',
                name_long='!![it]Categoria')

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

    def trigger_onInserting(self, record=None):
        self.buildUpStoreBag(record)

    def buildUpStoreBag(self, record=None, filler=0):
        '''Make a storage schema based on selected model'''
        current_model = record['sm_model__id']
        model_storeBag = self.getStoreBagFromModel(current_model, filler)

        # i keep the following lines as an example
        # they where the way to update a record to dbms
        # changing from onInserted to onInserting, they have no more meaning
        # ...but i have something to copy from in the future...
        # # update the storeBag
        # with self.recordToUpdate(record['id']) as currentRecord:
        #         currentRecord['storebag']=current_storeBag
        #         currentRecord['status']='ELABORABILE'
        record['storebag']=model_storeBag
        record['status']='ELABORABILE'
        return model_storeBag

    def getStoreBagFromModel(self, model, filler=None):
        current_storeBag = Bag()
        
        # model rows and cols
        model_rows = self.db.table('sm.sm_model_row').query(
                columns='$code, $description',
                where='$sm_model__id=:model__id', model__id=model,
                order_by='$position'
                ).fetch()

        model_cols = self.db.table('sm.sm_model_col').query(
                columns='$code, $description',
                where='$sm_model__id=:model__id', model__id=model,
                order_by='$position'
                ).fetch()

        # build up store Bag as for model
        i=0

        for r in model_rows:
                i+=1
                # current_storeBag[i]=Bag()
                # current_storeBag[i]['cod']=r['code']
                # current_storeBag[i]['desc']=r['description']
                current_storeBag.setItem(r['code'], Bag())
                
                for c in model_cols:
                        #current_storeBag[i][c['code']] = filler  #f'{i},{j}'
                        current_storeBag[r['code']].setItem(c['code'], filler)
        
        return current_storeBag
