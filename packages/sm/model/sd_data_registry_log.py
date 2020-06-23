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
        '''sd: schema data, log for data registry'''
        tbl = pkg.table('sd_data_registry_log', pkey='id', 
                name_long='!![it]Log operazioni',
                caption_field='date_elab')

        self.sysFields(tbl)

        tbl_sd_data_registry__id=tbl.column('sd_data_registry__id',size='22', 
                group='_', name_long='!![it]Schema')
        tbl_sd_data_registry__id.relation('sd_data_registry.id', 
                relation_name='data_registry_log', 
                mode='foreignkey', onDelete='cascade')

        tbl_date_elab = tbl.column('date_elab', dtype='D', 
                name_long='!![it]Data elaborazione', name_short='!![it]Data')

        tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        tbl_current_user=tbl.column('current_user', size=':22', 
                name_long='!![it]Utente')

        tbl_ruleset=tbl.column('ruleset', size=':22', 
                name_long='!![it]Set regole')

        tbl_schema_source=tbl.column('schema_source', size=':22', 
                name_long='!![it]Schema origine')
        
        tbl.column('source_storebag', dtype='X',
                name_long='!![it]StoreBag sorgente dati')

        tbl.column('previous_storebag', dtype='X',
                name_long='!![it]StoreBag pre-elaborazione')
