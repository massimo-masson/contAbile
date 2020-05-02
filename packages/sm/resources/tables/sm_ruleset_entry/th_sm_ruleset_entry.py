#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('sm_ruleset__id')

        # columnset row
        rows=r.columnset('rows', name='!![it]Righe', color='black', background='lightblue')
        rows.fieldcell('src_sm_model_row__id')
        rows.fieldcell('dst_sm_model_row__id')

        # columnset col
        cols=r.columnset('cols', name='!![it]Colonne', color='black', background='lightgreen')
        cols.fieldcell('src_sm_model_col__id')
        cols.fieldcell('dst_sm_model_col__id')

        # columnset operations
        ops=r.columnset('operations', name='!![it]Operazioni', color='darkblue', background='lightyellow')
        ops.fieldcell('operation')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)

class ViewFromRuleset(View):
    pass

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.div(margin='10px').formbuilder(cols=4, border_spacing='4px')
        fb.field('code')
        fb.field('description')
        fb.field('sm_ruleset__id', hasDownArrow=True)
        fb.field('@sm_ruleset__id.code', readonly=True)
        #fb.field('@sm_ruleset__id.@src_sm_model__id.code', readonly=True)

        # riga
        fb.div('!![it]RIGHE', #lbl='!![it]ATTENZIONE', 
                colspan=2, width='100%',
                background_color='lightgrey')
        fb.div('!![it]COLONNE', #lbl='!![it]ATTENZIONE', 
                colspan=2, width='100%',
                background_color='lightgrey')

        # riga
        fb.field('src_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.code',
                fld_background='lightyellow')
        fb.field('@src_sm_model_row__id.description', readonly=True, fld_background='lightyellow')
        fb.field('src_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.code',
                fld_background='lightyellow')
        fb.field('@src_sm_model_col__id.description', readonly=True, fld_background='lightyellow')

        # riga
        fb.field('dst_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.code',
                fld_background='lightgreen')
        fb.field('@dst_sm_model_row__id.description', readonly=True, fld_background='lightgreen')
        fb.field('dst_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.code',
                fld_background='lightgreen')
        fb.field('@dst_sm_model_col__id.description', readonly=True, fld_background='lightgreen')

        valori='0:set=0,1:sum,2:subtract'
        fb.field('operation', tag='filteringSelect', values=valori)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromRuleset(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.95, modal=True)