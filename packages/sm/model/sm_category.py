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
        '''sm: schema management, categories'''
        tbl = pkg.table('sm_category', pkey='id', 
                name_long='!![it]Categoria modello',
                name_plural='!![it]Categorie modello',
                caption_field='code')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice categoria',
                unique=True, validate_notnull=True, indexed=True)

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione categoria', 
                validate_notnull=True)

        tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')
