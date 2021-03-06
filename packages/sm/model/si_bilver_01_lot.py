#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# contAbile:sm (schema manager), an automated processor for data based on
# models and flexible processing logic built by users.
# Copyright (C) 2020 Massimo Masson
# 
# This program is dual-licensed.
# 
# Option 1:
# If you respect the terms of GNU GPL license, AND
# you agree to give the copyright for modifications or derivative work
# to the original author Massimo Masson, the GPL license applies.
# In this case:
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# Option 2:
# If you do not agree with any of the statements in option 1, then
# a proprietary license applies. In this case, contact the author
# for a dedicated propietary license.
# 

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

        fk = tbl.column('si_bilver_01_model__code', dtype='A', size=':22',
                name_long='!![it]Modello di importazione',
                validate_notnull=True)
        fk.relation('sm.si_bilver_01_model.code', relation_name='bilver_01_import_lots',
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
                        columns = '$ext_code, $ext_value, $ext_description',
                        where = '$si_bilver_01_lot__lot_code = :selected_lot_code',
                        selected_lot_code = lot_code,
                        )

        # loop every lot row
        for row in lot_rows.fetch():
            #print('id modello riferimento:', lot['@si_bilver_01_model__id.id'])
            (dst_row, dst_col, invert_sign) = self.import_lot_get_model_ref(
                                lot['@si_bilver_01_model__code.code'], row['ext_code'])
            #print(row['ext_code'], row['ext_value'], ' -> ', dst_row, dst_col)

            # assegnazione valore, eventualmente con il segno
            if (invert_sign == True):
                value = -1 * row['ext_value']
            else:
                value = row['ext_value']

            if storebag.has_key(dst_row):
                # situazione normale, aggiunta del valore imortato
                storebag[dst_row][dst_col] += value
            else:
                # situazione di errore: nuova riga codice err_ e imposta valore
                # subtle bug, if the imported code has dots, the bag builds
                # a hierarchy, so replace '.' with something else..
                normalized_dst_row = dst_row.replace('.', '_')
                value_and_descr = '(' + str(value) + ') ' + row['ext_description']
                storebag.setItem(normalized_dst_row, Bag())
                storebag[normalized_dst_row].setItem('code', dst_row)
                storebag[normalized_dst_row].setItem('description', value_and_descr)
                #storebag[dst_row].setItem(dst_col, row['ext_value'])

        return storebag

    def import_lot_get_model_ref(self, model_code, ext_code):
        # return storebag row and col for ext_code in si_bilver_01_lot
        qry = self.db.table('sm.si_bilver_01_model_link').query(
                    columns = '@sm_model_row__id.code AS rcode, \
                        @sm_model_col__id.code AS ccode, \
                        $invert_sign',
                    where = '$si_bilver_01_model__code = :par_model_code \
                        AND $ext_code = :par_ext_code',
                    par_model_code = model_code,
                    par_ext_code = ext_code
                    )
        rs = qry.fetch()

        if len(rs) > 0:
            # record found, use code. should be only one...
            row_code = rs[0]['rcode']
            col_code = rs[0]['ccode']
            invert_sign = rs[0]['invert_sign']
        else:
            # record not found, use err_codes
            row_code = 'err_' + ext_code
            col_code = 'err'
            invert_sign = False

        return row_code, col_code, invert_sign