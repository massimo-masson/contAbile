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
        r.fieldcell('sm_model__id')
        r.fieldcell('sm_model_row__id')
        r.fieldcell('sm_model_col__id')
        r.fieldcell('formula')
        r.fieldcell('description')

    def th_order(self):
        # return 'sm_model_row__id'
        return 'caption'

    def th_query(self):
        return dict(column='sm_model__id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        
        fb.field('sm_model__id', hasDownArrow=True)
        fb.field('@sm_model__id.description', readonly=True)

        fb.field('sm_model_row__id', hasDownArrow=True,
            condition='@sm_model__id.id=:modello AND $row_type=:formula',
            condition_modello='=.@sm_model__id.id',
            condition_formula='formula'
            )
        fb.field('@sm_model_row__id.description', readonly=True)

        fb.field('sm_model_col__id', hasDownArrow=True,
            condition='@sm_model__id.id=:modello',
            condition_modello='=.@sm_model__id.id'
            )
        fb.field('@sm_model_col__id.description', readonly=True)

        fb.field('description', colspan=2, width='100%')

        fb.field('formula', colspan=2, width='100%')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromModel(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sm_model__id')
        r.fieldcell('sm_model_row__id', edit=True)
        r.fieldcell('sm_model_col__id', edit=True)
        r.fieldcell('formula', edit=True)
        r.fieldcell('description', edit=True)

class FormFromModel(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.8, modal=False)
