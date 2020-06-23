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

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('position')
        r.fieldcell('description')
        r.fieldcell('sd_process_batch__id')
        r.fieldcell('sm_ruleset__id')
        r.fieldcell('src_sd_data_registry__id')
        r.fieldcell('dst_sd_data_registry__id')

    def th_order(self):
        return 'position'

    def th_query(self):
        return dict(column='position', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=4, border_spacing='4px')
        # row 1, rule
        fb.field('position')
        fb.field('description')

        # row 2, batch
        fb.field('sd_process_batch__id', hasDownArrow=True)
        fb.field('@sd_process_batch__id.description', readonly=True,
                lbl='!![it]Lotto:')
        
        # row 3, ruleset
        fb.field('sm_ruleset__id', hasDownArrow=True)
        fb.field('@sm_ruleset__id.description', colspan=3, readonly=True,
                width='100%', lbl='!![it]Set di regole')

        # row
        fb.field('@sm_ruleset__id.@src_sm_model__id.code', lbl='!![it]Da:',
                colspan=2, width='100%', fld_background='lightyellow')
        fb.field('@sm_ruleset__id.@dst_sm_model__id.code', lbl='!![it]A:',
                colspan=2, width='100%', fld_background='lightgreen')

        # row
        fb.field('@sm_ruleset__id.@src_sm_model__id.description', lbl='',
                colspan=2, width='100%', fld_background='lightyellow')
        fb.field('@sm_ruleset__id.@dst_sm_model__id.description', lbl='',
                colspan=2, width='100%', fld_background='lightgreen')

        # row, source
        # source schema's model must match ruleset source model
        fb.field('src_sd_data_registry__id', hasDownArrow=True,
                condition='$sm_model__id=:source_model',
                condition_source_model='=.@sm_ruleset__id.@src_sm_model__id.id')
        fb.field('@src_sd_data_registry__id.description', readonly=True)

        # row, destination
        # destination schema's model must match ruleset destination model
        # AND the destination schema must not be "protected" (0 or NULL)
        fb.field('dst_sd_data_registry__id', hasDownArrow=True,
                condition='($sm_model__id=:source_model) AND (($is_protected=:protect) OR ($is_protected IS NULL))',
                condition_source_model='=.@sm_ruleset__id.@dst_sm_model__id.id',
                condition_protect='0')
        fb.field('@dst_sd_data_registry__id.description', readonly=True)


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromProcessBatch(View):
    pass

class FormFromProcessBatch(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.9)
