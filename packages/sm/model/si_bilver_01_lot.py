#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''si: schema import, bilancio verifica tipo 1'''
        tbl = pkg.table('si_bilver_01_lot', pkey='lot_code',
                name_long='!![it]Lotto importazione bilancio di verifica',
                name_plural='!![it]Lotti importazione bilancio di verifica',
                caption_field='lot_code')

        self.sysFields(tbl)

        tbl.column('lot_code', dtype='A', size=':22',
                unmodifiable=True,
                name_long='!![it]Codice lotto importazione',
                unique=True, validate_notnull=True)

        tbl.column('description', dtype='A', size=':256',
                name_long='!![it]Descrizione lotto importazione')

        # fk = tbl.column('ref_model', dtype='A', size=':22',
        #         name_long='!![it]Modello di schema di riferimento'
        #         )
        # fk.relation('sm.sm_model.id', relation_name='bilver_01_lot_codes', 
        #             mode='foreignkey', onDelete='raise')

        fk = tbl.column('si_bilver_01_model__id', dtype='A', size=':22',
                name_long='!![it]Modello di importazione',
                validate_notnull=True)
        fk.relation('sm.si_bilver_01_model.id', relation_name='bilver_01_import_lots',
                    mode='foreignkey', onDelete='raise')


    def import_lot(self, schema_id, lot_code):
        # get the schema by schema_id
        # get the storebag
        # clear the storebag
        # get the lot, by lot_id
        # loop on every record of the lot
        #    get row reference from model_link
        #    get col reference from model_link
        #    update the storebag or error

        # get schema and storebag
        schema = self.db.table('sm.sd_data_registry').record(schema_id).output('bag')
        storebag = schema['storebag']

        # clear the storebag (fill with 0)
        for r in storebag.keys():
            for c in storebag[r].keys():
                if c not in ('code', 'description'):
                    storebag[r][c] = 0

        # get the lot and lot rows
        lot = self.db.table('sm.si_bilver_01_lot').record(lot_code).output('bag')
        lot_rows = self.db.table('sm.si_bilver_01_lot_row').query(
                        columns = '$ext_code,$ext_value',
                        where = '$si_bilver_01_lot__lot_code = :selected_lot_code',
                        selected_lot_code = lot_code,
                        )

        # loop every lot row
        for row in lot_rows.fetch():
            #print('id modello riferimento:', lot['@si_bilver_01_model__id.id'])
            (dst_row, dst_col) = self.import_lot_get_model_ref(
                                lot['@si_bilver_01_model__id.id'], row['ext_code'])
            #print(row['ext_code'], row['ext_value'], ' -> ', dst_row, dst_col)

            if storebag.has_key(dst_row):
                # situazione normale, aggiunta del valore imortato
                storebag[dst_row][dst_col] += row['ext_value']
            else:
                # situazione di errore: nuova riga codice err_ e imposta valore
                storebag.setItem(dst_row, Bag())
                storebag[dst_row].setItem('code', dst_row)
                storebag[dst_row].setItem('description', row['ext_value'])
                #storebag[dst_row].setItem(dst_col, row['ext_value'])

        # end of import_lot
        return storebag

    def import_lot_get_model_ref(self, model_id, ext_code):
        # return storebag row and col for ext_code in si_bilver_01_lot
        qry = self.db.table('sm.si_bilver_01_model_link').query(
                    columns = '@sm_model_row__id.code AS rcode,@sm_model_col__id.code AS ccode',
                    where = '$si_bilver_01_model__id=:par_model_id AND $ext_code=:par_ext_code',
                    par_model_id = model_id,
                    par_ext_code = ext_code
                    )
        rs = qry.fetch()

        if len(rs) > 0:
            # record found, use code. should be only one...
            r = rs[0]['rcode']
            c = rs[0]['ccode']
        else:
            # record not found, use err_codes
            r = 'err_' + ext_code
            c = 'err'

        return r, c