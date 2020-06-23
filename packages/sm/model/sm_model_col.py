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

        tbl.column('field_format', dtype='A', size=':128', 
                name_long='!![it]Formattazione campo', 
                name_short='!![it]Formato col.')

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

    def CONST_field_type(self):
        '''Return the constant values for the "field_type" field.
        '''
        CONST = 'N: Numerico'
        return CONST

    def CONST_field_format(self):
        '''Return the constant values for the "field_format" field.
        '''
        CONST = "#_###.00:Con decimali, #_###: Arrotondati all'intero"
        return CONST

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
