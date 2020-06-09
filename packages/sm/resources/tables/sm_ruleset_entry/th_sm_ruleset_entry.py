#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
        self.rulesetEntryBody(bc.contentPane(region = 'center'))

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
        fb = tab_formula.div(margin = '10px').formbuilder(cols = 1, border_spacing = '4px')
        fb.field('formula', tag = 'simpleTextArea', lbl = '',
                disabled = '^.record.operation?=#v!="f"',
                width = '80em', height = '6em')

        fb.div('!![it]Promemoria sintassi formule: \
                Valgono le normali operazioni aritmetiche.\
                I parametri sono delimitati da parentesi quadre, \
                e vengono interpretati nel modo seguente:')
        fb.div('!![it]<b>[$]</b> valore della cella sorgente indicata nella regola.\
                <b>[@]</b> valore della cella destinazione indicata nella regola (vedi sopra)')
        fb.div('!![it]<b>[$Rx.Cy]</b> valore della cella sorgente Rx.Cy. \
                <b>[@Rx.Cy]</b> valore della cella destinazione Rx.Cy')
        fb.div('!![it]<b>[#G#nome]</b> valore del parametro globale definito da "nome"')
        fb.div('!![it]<b>[#C#nome]</b> valore del parametro di categoria definito da "nome"')
        fb.div('!![it]<b>[#M#nome]</b> valore del parametro di modello definito da "nome"')
        fb.div('!![it]<b>[#S#nome]</b> valore del parametro di schema definito da "nome"')

        # tab python
        tab_python = tc.contentPane(title = '!![it]Python')
        fb = tab_python.div(margin = '10px').formbuilder(cols = 1, border_spacing = '4px')
        fb.div('!![it]Non implementato.')

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')

class FormFromRuleset(Form):

    def th_options(self):
        return dict(dialog_parentRatio = 0.95) #, modal=True)