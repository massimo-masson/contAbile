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
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('notes')
        r.fieldcell('sm_category__id')
        r.fieldcell('dynamic_rows')
        r.fieldcell('dynamic_cols')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column = 'code', op = 'contains', val = '', runOnStart = True)

    def th_top_barcategory(self, top):
        top.slotToolbar('5,sections@sm_category__id,*',
                childname = 'dummy',
                _position = '<bar', 
                sections_sm_category__id_multiButton = 6)
                #, gradient_from='#999', gradient_to='#666')


class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.anagraficaInfo(bc.contentPane(region = 'top', datapath = '.record'))
        self.anagraficaBody(bc.contentPane(region = 'center'))

    def anagraficaInfo(self, pane):
        fb = pane.formbuilder(cols = 4, border_spacing = '4px')

        fb.field('code')
        fb.field('description')
        fb.field('sm_category__id', hasDownArrow = True)
        fb.field('@sm_category__id.description', readonly = True,
            lbl=':', lbl_color='darkblue', fld_background = 'lightgrey')

        fb.field('dynamic_rows')
        fb.field('dynamic_cols')
        # fb.div(lbl='!![it]Se spuntati, diventa possibile usare righe e colonne non \
        #     predefinite nello schema.', 
        #     colspan = 1, width = '100%')
        fb.field('progressive_version', readonly = True, fld_background = 'lightgrey')
        fb.div()

        fb.field('notes', colspan = 4, width = '100%', 
            tag = 'simpleTextArea', height = '10ex')

    def anagraficaBody(self, pane):
        tc = pane.tabContainer()

        # tab rows
        tab_rows = tc.contentPane(title = '!![it]Righe')
        tab_rows.inlineTableHandler(relation = '@rows',
                pbl_classes = True,
                viewResource = 'ViewFromModel',
                grid_selfDragRows = True,
                margin = '2px',
                searchOn = True)

        # tab cols
        tab_cols = tc.contentPane(title = '!![it]Colonne')
        tab_cols.inlineTableHandler(relation = '@columns',
                pbl_classes = True,
                viewResource = 'ViewFromModel',
                grid_selfDragRows = True,
                margin = '2px',
                searchOn = True)

        # tab formula
        tab_formula = tc.contentPane(title = '!![it]Formule')
        tab_formula.dialogTableHandler(relation = '@model_formula',
                viewResource = 'ViewFromModel',
                formResource = 'FormFromModel',
                margin = '2px',
                searchOn = True)

        # tab parameters
        tab_params = tc.contentPane(title = '!![it]Parametri modello')
        tab_params.dialogTableHandler(relation = '@model_parameters',
                viewResource = 'ViewFromModel',
                formResource = 'FormFromModel',
                margin = '2px',
                searchOn = True)

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')
