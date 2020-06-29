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
        '''sd: schema data, model parameter
        
        A model parameter can be accessed from the schema elaboration
        if the schema belongs to that model.
        '''
        tbl = pkg.table('sd_parameter_model', pkey = 'id',
                name_long = '!![it]Parametro di modello',
                name_plural='!![it]Parametri di modello',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22', 
                name_long = '!![it]Codice parametro di modello',
                validate_notnull = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione parametro di modello')

        tbl.column('value', dtype = 'N',
                name_long = '!![it]Valore', name_short = '!![it]Val')        

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype = 'A', size = '22',
                name_long = '!![it]Classe')
        fk.relation('sm.sm_parameter_class.id', mode = 'foreignkey',
                relation_name = 'class_model_parameters', onDelete = 'raise')

        # foreign key to the referenced model
        fk = tbl.column('sm_model__id', dtype = 'A', size = '22',
                name_long = '!![it]Rif. modello')
        fk.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'model_parameters', onDelete = 'raise')

    def protect_validate(self, record):
        if self.validateCodeUniquePerParameterModel(record) == True:
            raise self.exception('protect_validate', record = record,
                                msg = '!![it]Codice riga duplicato nel modello'
                                )

    def validateCodeUniquePerParameterModel(self, record = None):
        '''parameter's code must be unique inside a single model'''

        duplicated = False

        rs = self.db.table('sm.sd_parameter_model').query(
            columns = '$id, $code, $description',
            where = '@sm_model__id.id = :current_model \
                    AND $code = :current_code',
            current_model = record['sm_model__id'],
            current_code = record['code']
        ).fetch()

        if len(rs) > 0:
            duplicated = True

        return duplicated
