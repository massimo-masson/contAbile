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
        '''sm: schema management, model formula'''
        tbl = pkg.table('sm_model_formula', pkey = 'id', 
                name_long = '!![it]Formula cella',
                name_plural = '!![it]Formule modello',
                caption_field = 'caption')

        self.sysFields(tbl)

        # foreign key to model
        fk_row = tbl.column('sm_model__id', dtype = 'A', size = '22',
                name_long = '!![it]Modello',
                validate_notnull = True)
        fk_row.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'raise')

        # foreign key to schema row
        fk_row = tbl.column('sm_model_row__id', dtype = 'A', size = '22',
                name_long = '!![it]Riga modello',
                validate_notnull = True)
        fk_row.relation('sm.sm_model_row.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'cascade')

        # foreign key to schema column
        fk_col = tbl.column('sm_model_col__id', dtype = 'A', size = '22',
                name_long = '!![it]Colonna modello',
                validate_notnull = True)
        fk_col.relation('sm.sm_model_col.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'cascade')

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione formula')

        tbl.column('formula', dtype = 'A', size = ':2048', 
                name_long = '!![it]Formula', 
                validate_notnull = True)

        tbl.formulaColumn('caption', '@sm_model_row__id.code||","||@sm_model_col__id.code',
                name_long = '!![it]Cella di riferimento')
