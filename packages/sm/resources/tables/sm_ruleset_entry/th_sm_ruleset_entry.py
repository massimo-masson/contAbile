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

from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('position')
        r.fieldcell('description')
        r.fieldcell('sm_ruleset__id')

        # columnset row
        rows = r.columnset('rows', name = '!![it]Righe', 
                color = 'black', background = 'lightblue')
        rows.fieldcell('src_sm_model_row__id')
        rows.fieldcell('dst_sm_model_row__id')

        # columnset col
        cols = r.columnset('cols', name = '!![it]Colonne', 
                color = 'black', background = 'lightgreen')
        cols.fieldcell('src_sm_model_col__id')
        cols.fieldcell('dst_sm_model_col__id')

        # columnset operations
        ops = r.columnset('operations', name = '!![it]Operazioni', 
                color = 'black', background = 'gold')
        ops.fieldcell('recalculate_before')
        ops.fieldcell('operation')
        ops.fieldcell('formula')

    def th_order(self):
        return 'position'

    def th_query(self):
        return dict(column = 'position', op = 'contains', val = '', runOnStart = True)


class ViewFromRuleset(View):
    pass


class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()

        self.rulesetEntryHeader(bc.contentPane(region = 'top', datapath = '.record'))
        self.rulesetEntryBody(bc.contentPane(region = 'center', datapath = '.record'))

    def rulesetEntryHeader(self, pane):
        fb = pane.div(margin = '10px').formbuilder(cols = 4, border_spacing = '4px')
        fb.field('position')
        fb.field('description', colspan = 3, width = '100%')

        fb.field('recalculate_before')
        fb.field('sm_ruleset__id', hasDownArrow = True)
        fb.field('@sm_ruleset__id.code', colspan = 2, width = '100%', readonly = True)

        # riga
        fb.div('!![it]RIGHE', 
                colspan = 2, width = '100%',
                background_color = 'lightgrey')
        fb.div('!![it]COLONNE', 
                colspan = 2, width = '100%',
                background_color = 'lightgrey')

        # riga
        fb.field('src_sm_model_row__id', hasDownArrow = True,
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@sm_ruleset__id.@src_sm_model__id.id',
                columns = '$code, $description',
                auxColumns = '$code, $description',
                fld_background = 'gold')
        fb.field('@src_sm_model_row__id.description', 
                readonly = True, fld_background = 'gold')
        fb.field('src_sm_model_col__id', hasDownArrow = True,
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@sm_ruleset__id.@src_sm_model__id.id',
                columns = '$code, $description',
                auxColumns = '$code, $description',
                fld_background = 'gold')
        fb.field('@src_sm_model_col__id.description', 
                readonly = True, fld_background = 'gold')

        # riga
        fb.field('dst_sm_model_row__id', hasDownArrow = True,
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@sm_ruleset__id.@dst_sm_model__id.id',
                columns = '$code,$description',
                auxColumns = '$code,$description',
                fld_background = 'lightgreen')
        fb.field('@dst_sm_model_row__id.description', 
                readonly = True, fld_background = 'lightgreen')
        fb.field('dst_sm_model_col__id', hasDownArrow = True,
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@sm_ruleset__id.@dst_sm_model__id.id',
                columns = '$code, $description',
                auxColumns = '$code, $description',
                fld_background = 'lightgreen')
        fb.field('@dst_sm_model_col__id.description', 
                readonly = True, fld_background = 'lightgreen')

        valori = self.db.table('sm.sm_ruleset_entry').CONST_operation()
        fb.field('operation', tag = 'filteringSelect', values = valori)
        # fb.div()
        # fb.div()
        # fb.div()

        # fb.field('src_sm_model__id')
        # fb.field('dst_sm_model__id')

    def rulesetEntryBody(self, pane):
        tc = pane.tabContainer()

        # tab formula
        tab_formula = tc.contentPane(title = '!![it]Formula')
        fb = tab_formula.div(margin = '10px').formbuilder(cols = 2, border_spacing = '4px')
        fb.field('formula', tag = 'simpleTextArea', lbl = '',
                disabled = '^.operation?=#v!="f"',
                width = '80em', height = '6em',
                colspan = 2)

        fb.div('!![it]Promemoria sintassi formule: \
                Valgono le normali operazioni aritmetiche.\
                I parametri sono delimitati da parentesi quadre [ e ], \
                e vengono interpretati nel modo seguente:'
                , colspan = 2, width = '100%')

        fb.div('!![it]DA SORGENTE', fld_background = 'gold')
        fb.div('!![it]DA DESTINAZIONE', fld_background = 'lightgreen')

        fb.div('!![it]<b>[$]</b> valore della cella sorgente indicata nella regola (vedi sopra)')
        fb.div('!![it]<b>[@]</b> valore della cella destinazione indicata nella regola (vedi sopra)')

        fb.div('!![it]<b>[$Rx.Cy]</b> valore della cella sorgente riga Rx colonna Cy')
        fb.div('!![it]<b>[@Rx.Cy]</b> valore della cella destinazione riga Rx colonna Cy')

        fb.div('!![it]<b>[#G#nome]</b> valore del parametro globale definito da "nome"',
                colspan = 2, width = '100%', align = 'center')
        
        fb.div('!![it]<b>[#C$nome]</b> valore del parametro della categoria \
                sorgente definito da "nome"')
        fb.div('!![it]<b>[#C@nome]</b> valore del parametro della categoria \
                destinazione definito da "nome"')

        fb.div('!![it]<b>[#M$nome]</b> valore del parametro del modello \
                sorgente definito da "nome"')
        fb.div('!![it]<b>[#M@nome]</b> valore del parametro del modello \
                destinazione definito da "nome"')

        fb.div('!![it]<b>[#S$nome]</b> valore del parametro dello schema \
                sorgente definito da "nome"')
        fb.div('!![it]<b>[#S@nome]</b> valore del parametro dello schema \
                destinazione definito da "nome"')

        # tab python
        tab_python = tc.contentPane(title = '!![it]Python')
        fb = tab_python.div(margin = '10px').formbuilder(cols = 1, border_spacing = '4px')
        fb.div('!![it]Non implementato.')

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')

class FormFromRuleset(Form):

    def th_options(self):
        return dict(dialog_parentRatio = 0.95) #, modal=True)