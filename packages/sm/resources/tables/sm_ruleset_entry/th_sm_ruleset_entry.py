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
        r.fieldcell('src_sm_model_row__id')
        r.fieldcell('dst_sm_model_row__id')
        r.fieldcell('src_sm_model_col__id')
        r.fieldcell('dst_sm_model_col__id')
        r.fieldcell('operation')

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
        fb.div('!![it]Per poter selezionare righe e colonne, scegliere prima il ruleset', 
                lbl='!![it]ATTENZIONE', colspan=4, width='100%',
                background_color='light-yellow')

        # riga
        fb.field('src_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.code')
        fb.field('@src_sm_model_row__id.description', readonly=True)
        fb.field('src_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.code')
        fb.field('@src_sm_model_col__id.description', readonly=True)

        # riga
        fb.field('dst_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.code')
        fb.field('@dst_sm_model_row__id.description', readonly=True)
        fb.field('dst_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.code=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.code')
        fb.field('@dst_sm_model_col__id.description', readonly=True)

        fb.field('operation')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromRuleset(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.95, modal=True)