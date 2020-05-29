#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, models'''
        tbl = pkg.table('sm_model', pkey = 'id', 
                name_long = '!![it]Modello di schema',
                name_plural = '!![it]Modelli di schemi',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22',
                unmodifiable = True,
                name_long = '!![it]Codice modello',
                unique = True, validate_notnull = True, indexed = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione modello', 
                validate_notnull = True)

        tbl.column('notes', dtype = 'A', size = ':1024', 
                name_long = '!![it]Note')

        # foreign key to sm_category
        tbl_category__id = tbl.column('sm_category__id', dtype = 'A', size = '22',
                name_long = '!![it]Categoria schema',
                validate_notnull = True)
        tbl_category__id.relation('sm.sm_category.id', mode = 'foreignkey',
                relation_name = 'models',
                onDelete = 'raise')

        tbl.column('dynamic_rows', dtype = 'B', default = False, 
                name_long = '!![it]Righe dinamiche', 
                name_short = '!![it]Righe dinamiche')

        tbl.column('dynamic_cols', dtype = 'B', default = False, 
                name_long = '!![it]Colonne dinamiche', 
                name_short = '!![it]Colonne dinamiche')

        tbl.column('progressive_version', dtype='N', default = 1,
                name_long = '!![it]Progressivo versione interna',
                name_short = '!![it]int.vers.'
                )

        # END OF config_db

    def trigger_onUpdating(self, record = None, old_record = None):
        last = old_record['progressive_version'] or 1
        record['progressive_version'] = last + 1

    def formulasSyncronize(self, model_id=None):
        self.formulasInsertOrUpdate(model_id)
        self.formulasDelete(model_id)

    def formulasInsertOrUpdate(self, model_id = None):
        if model_id == None:
            return

        # # model record from id
        # rs_model = self.db.table('sm.sm_model').record(model_id).output('bag')
        
        # recordset model rows
        rs_rows = self.db.table('sm.sm_model_row').query(
            columns = '$id,$code',
            where = '@sm_model__id.id = :current_model AND $row_type = :formula',
            current_model = model_id,
            formula = 'formula'
        ).selection()

        # recordset model cols
        rs_cols = self.db.table('sm.sm_model_col').query(
            columns = '$id,$code',
            where = '@sm_model__id.id = :current_model',
            current_model = model_id
        ).selection()

        # loop through rows and columns,
        # look for formula record for row,col
        # if not found, add "placeholder" record
        for r in rs_rows:
            for c in rs_cols:
                #print(r['code'],c['code'])
                f = self.db.table('sm.sm_model_formula').query(
                    columns = '@sm_model_row__id.code AS rowcode,\
                        @sm_model_col__id.code AS colcode',
                    where = '@sm_model__id.id = :current_model \
                        AND @sm_model_row__id.code = :current_row \
                        AND @sm_model_col__id.code = :current_col',
                    current_model = model_id,
                    current_row = r['code'],
                    current_col = c['code']
                ).selection().output('bag')
                
                found = False
                for v in f['rows'].values():
                    if (r['code'] == v['rowcode']) and (c['code'] == v['colcode']):
                        found = True

                if not found:
                    # need to insert cell formula
                    #print('INSERT:', r['code'], c['code'])
                    new_record = dict(sm_model__id = model_id,
                        sm_model_row__id = r['id'],
                        sm_model_col__id = c['id']
                        #formula = '=0'
                        )
                    self.db.table('sm.sm_model_formula').insert(new_record)
                    self.db.commit()
                else:
                    # this wold be an update
                    # print('UPDATE:', r['code'], c['code'])
                    pass

        # END OF formulasInsertOrUpdate

    def formulasDelete(self, model_id = None):
        # cycle on every formula, look for presence in model
        rs_formulas = self.db.table('sm.sm_model_formula').query(
            columns = '$id, @sm_model_row__id.code AS rowcode, \
                @sm_model_col__id.code AS colcode',
            where = '@sm_model__id.id = :current_model',
            current_model = model_id
        ).selection()

        found_one = False

        for f in rs_formulas:

            # does the row exists?
            rs_r = self.db.table('sm.sm_model_row').query(
                columns = '$id, $code',
                where = '$code = :frow AND $row_type = :formula',
                frow = f['rowcode'],
                formula = 'formula'
            ).fetch()

            # does the column exists?
            rs_c = self.db.table('sm.sm_model_col').query(
                columns = '$id, $code',
                where = '$code = :fcol',
                fcol = f['colcode']
            ).fetch()

            # if both row and column doesn't exists, delete formula row
            if (len(rs_r) == 0) or (len(rs_c) == 0):
                self.db.table('sm.sm_model_formula').delete(f['id'])
                found_one = True

        # if something was found, commit...
        if found_one:
            self.db.commit()

        # END OF formulasDelete

    def getStructBagFromModel(self, model):
        structBag = Bag()
        
        # model columns
        model_cols = self.db.table('sm.sm_model_col').query(
                columns = '$code, $description',
                where = '$sm_model__id=:model__id', model__id = model,
                order_by = '$position'
                ).fetch()

        # first two columns, fixed:
        # code: row code
        # description: row description
        # view_0 is "magic" (legacy)
        cols = structBag['view_0.rows_0'] = Bag()
        cols.addItem('code', None, name = '!![it]Codice', width = '6em')
        cols.addItem('description', None, name = '!![it]Descrizione', width = '20em')

        # add model columns from model
        for c in model_cols:
                cols.addItem(c['code'], None, name = c['description'], width = '10em')
         
        return structBag
        # END OF getStructBagFromModel