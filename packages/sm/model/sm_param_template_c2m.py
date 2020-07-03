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
        '''sm: schema model, parameters template from category to model
        
        Schema template parameter that will be automatically added
        to the model(s) belonging to this category
        '''
        tbl = pkg.table('sm_param_template_c2m', pkey = 'id',
                name_long = '!![it]Template parametri per modello',
                name_plural='!![it]Template parametri per modelli',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22', 
                name_long = '!![it]Codice template parametro',
                validate_notnull = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione template parametro')

        tbl.column('value', dtype = 'N',
                name_long = '!![it]Valore default', name_short = '!![it]Default')        

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype = 'A', size = '22',
                name_long = '!![it]Classe parametro')
        fk.relation('sm.sm_parameter_class.id', mode = 'foreignkey',
                relation_name = 'class_category_param_template_c2m', onDelete = 'raise')

        # foreign key to the referenced category
        fk = tbl.column('sm_category__id', dtype = 'A', size = '22',
                name_long = '!![it]Rif. schema')
        fk.relation('sm.sm_category.id', mode = 'foreignkey',
                relation_name = 'category_param_template_c2m', onDelete = 'raise')

    def protect_validate(self, record):
        if self.validateCodeUniquePer_param_template_c2m(record) == True:
            raise self.exception('protect_validate', record = record,
                                msg = '!![it]Codice riga template duplicato nella categoria'
                                )

    def validateCodeUniquePer_param_template_c2m(self, record = None):
        '''parameter's template code must be unique inside a single category'''

        duplicated = False

        rs = self.db.table('sm.sm_param_template_c2m').query(
            columns = '$id, $code, $description',
            where = '@sm_category__id.id = :current_category \
                    AND $code = :current_code',
            current_category = record['sm_category__id'],
            current_code = record['code']
        ).fetch()

        if len(rs) > 0:
            duplicated = True

        return duplicated
