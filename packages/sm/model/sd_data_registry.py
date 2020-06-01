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
        current_model_id = record['sm_model__id']
        model_storeBag = self.getStoreBagFromModel(current_model_id, filler)

        # i keep the following lines as an example
        # they where the way to update a record to dbms
        # changing from onInserted to onInserting, they have no more meaning
        # ...but i have something to copy from in the future...
        # # update the storeBag
        # with self.recordToUpdate(record['id']) as currentRecord:
        #         currentRecord['storebag']=current_storeBag
        #         currentRecord['status']='ELABORABILE'
        record['storebag'] = model_storeBag
        record['status'] = 'ELABORABILE'
        return model_storeBag

    def getFormulaFromModel(self, model_id, row, col):
        #f = self.db.table('sm.sm_model').record(model_id).output('bag')
        formula = None
        rs = self.db.table('sm.sm_model_formula').query(
                columns = '$formula',
                where = '$sm_model__id=:model__id',
                model__id = model_id
                ).fetch()
        for r in rs:
            formula = r['formula']
        return formula
        
    def setStoreBagCellValue(self, storebag, row, col, value):
        '''can write only in "data" items'''

        if storebag.getAttr(row, 'row_type') == 'data':
            storebag[row][col] = value

    def getStoreBagFromModel(self, model_id, filler=None):
        current_storeBag = Bag()

        model = self.db.table('sm.sm_model').record(model_id).output('bag')

        # model rows and cols
        row_columns = '$code, $description,$row_type,'
        model_rows = self.db.table('sm.sm_model_row').query(
                columns = row_columns,
                where = '$sm_model__id=:model__id',
                model__id = model_id,
                order_by = '$position'
                ).fetch()

        col_columns = '$code, $description,$field_type'
        model_cols = self.db.table('sm.sm_model_col').query(
                columns = col_columns,
                where = '$sm_model__id=:model__id',
                model__id = model_id,
                order_by = '$position'
                ).fetch()

        # create bag rows, columns. placeholder for formulas
        for r in model_rows:
            current_storeBag.setItem(r['code'], Bag())
            current_storeBag.setAttr(r['code'], row_type = r['row_type'])
            current_storeBag.setAttr(r['code'], 
                             progressive_version = model['progressive_version'])

            # first 2 columns, fixed: 'code', 'description'
            current_storeBag[r['code']].setItem('code', r['code'])
            current_storeBag[r['code']].setItem('description', r['description'])

            for c in model_cols:
                current_storeBag[r['code']].setItem(c['code'], '')
                current_storeBag[r['code']].setAttr(c['code'], field_type = c['field_type'])
                # data, formula or description?
                if (r['row_type'] == 'desc'):
                    # description
                    pass
                elif (r['row_type'] == 'formula'):
                    # formula
                    # self.setStoreBagFormula(model_id, current_storeBag, 
                    #                     r['code'], c['code'],
                    #                     formula = None  # get formula from model
                    #                     )
                    current_storeBag[r['code']][c['code']] = '-'
                elif (r['row_type'] == 'data'):
                    # data
                    self.setStoreBagCellValue(current_storeBag, 
                                        r['code'], c['code'], filler)
                else:
                    # Nespresso, what else?
                    print("ERRORE TIPO:", r['code'], c['code'])

        self.calcStoreBag(model_id, current_storeBag)

        return current_storeBag

    def calcStoreBag(self, model_id, storebag):
        # all rows, get "formula" ones
        for rk, rv, ra in storebag.digest('#k,#v,#a'):
            # r(k)eys, r(v)alues, r(a)ttributes
            # use get for dict keys, so "no-key, no-error"
            if (ra.get('row_type') == 'formula'):
                # this row has formula columns
                # the row code is in rk
                for ck, cv, ca in storebag[rk].digest('#k,#v,#a'):
                    # column in ck, calc if not 'code', or 'description'
                    if not (ck in ('code', 'description')):
                        value = self.calcStoreBagCell(model_id, rk, ck, storebag)
                        storebag[rk][ck] = value
        return
    
    def calcStoreBagCell(self, model_id, row, col, storebag):
        # model rows and cols
        rs_formula = self.db.table('sm.sm_model_formula').query(
                columns = '$formula',
                where = '$sm_model__id = :model__id \
                    AND @sm_model_row__id.code = :row_code \
                    AND @sm_model_col__id.code = :col_code',
                model__id = model_id,
                row_code = row,
                col_code = col
                ).fetch()

        value = '#n/d'
        for record in rs_formula:
            f = record['formula']
            #print('formula: ', f)
            refs = self.parseFormulaCellReference(f)
            for c in refs:
                # references are in the form: [Rx.Cy]
                # need to strip the [ ]
                bagRef = c[1:-1]
                # get the cell value
                tmpval = storebag[bagRef]
                # substitute the value found
                f = f.replace(c, str(tmpval))
            #print('parsed formula:', f)
        value = eval(f)
        return value

    def parseFormulaCellReference(self, formula):
        result = list()
        i = 0
        f = formula

        while (i >= 0):
            pos_start = f.find('[', i)
            i = pos_start
            pos_end = pos_start + 1
            if (pos_start >= 0):
                pos_end = f.find(']', i + 1)
                result.append(f[pos_start:pos_end + 1])
                i = pos_end

        return result