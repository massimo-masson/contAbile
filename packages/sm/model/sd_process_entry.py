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
        '''sd: process batch entry'''
        tbl = pkg.table('sd_process_entry', pkey='id', 
                name_long='!![it]Fase elaborazione',
                name_plural='!![it]Fasi elaborazione',
                caption_field='description')

        self.sysFields(tbl)

        tbl.column('position', dtype='N',
                name_long='!![it]Posizione', name_short='!![it]Fase')

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione')

        # relation to sd_process_batch
        tbl.column('sd_process_batch__id', size='22', group='_', 
                name_long='!![it]Lotto di elaborazione', name_short='!![it]Lotto',
                validate_notnull=True
                ).relation('sm.sd_process_batch.id', relation_name='process_entries', 
                mode='foreignkey', onDelete='raise')
        
        # relation to sm_ruleset
        tbl.column('sm_ruleset__id', size='22', group='_', 
                name_long='!![it]Regole di elaborazione', name_short='!![it]Regole',
                validate_notnull=True
                ).relation('sm.sm_ruleset.id', relation_name='process_entries', 
                mode='foreignkey', onDelete='raise')

        # relation to source schema
        tbl.column('src_sd_data_registry__id', size='22', group='_', 
                name_long='!![it]Schema sorgente', name_short='!![it]Src',
                validate_notnull=True
                ).relation('sm.sd_data_registry.id', relation_name='src_process_entries', 
                mode='foreignkey', onDelete='raise')

        # relation to destination schema
        tbl.column('dst_sd_data_registry__id', size='22', group='_', 
                name_long='!![it]Schema destinazione', name_short='!![it]Dst',
                validate_notnull=True
                ).relation('sm.sd_data_registry.id', relation_name='dst_process_entries', 
                mode='foreignkey', onDelete='raise')
