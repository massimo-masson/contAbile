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
        rows=r.columnset('rows', name='!![it]Righe', color='black', background='lightblue')
        rows.fieldcell('src_sm_model_row__id')
        rows.fieldcell('dst_sm_model_row__id')

        # columnset col
        cols=r.columnset('cols', name='!![it]Colonne', color='black', background='lightgreen')
        cols.fieldcell('src_sm_model_col__id')
        cols.fieldcell('dst_sm_model_col__id')

        # columnset operations
        ops=r.columnset('operations', name='!![it]Operazioni', color='black', background='gold')
        ops.fieldcell('operation')

    def th_order(self):
        return 'position'

    def th_query(self):
        return dict(column='position', op='contains', val='', runOnStart=True)

class ViewFromRuleset(View):
    pass

class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()

        self.rulesetEntryHeader(bc.contentPane(region='top', datapath='.record'))
        self.rulesetEntryBody(bc.contentPane(region='center'))

    def rulesetEntryHeader(self, pane):
        fb = pane.div(margin='10px').formbuilder(cols=4, border_spacing='4px')
        fb.field('position')
        fb.field('description')
        fb.field('sm_ruleset__id', hasDownArrow=True)
        fb.field('@sm_ruleset__id.code', readonly=True)

        # riga
        fb.div('!![it]RIGHE', 
                colspan=2, width='100%',
                background_color='lightgrey')
        fb.div('!![it]COLONNE', 
                colspan=2, width='100%',
                background_color='lightgrey')

        # riga
        fb.field('src_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.id=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.id',
                columns = '$code,$description',
                auxColumns = '$code,$description',
                fld_background='gold')
        fb.field('@src_sm_model_row__id.description', readonly=True, fld_background='gold')
        fb.field('src_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.id=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@src_sm_model__id.id',
                columns = '$code,$description',
                auxColumns = '$code,$description',
                fld_background='gold')
        fb.field('@src_sm_model_col__id.description', readonly=True, fld_background='gold')

        # riga
        fb.field('dst_sm_model_row__id', hasDownArrow=True,
                condition='@sm_model__id.id=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.id',
                columns = '$code,$description',
                auxColumns = '$code,$description',
                fld_background='lightgreen')
        fb.field('@dst_sm_model_row__id.description', readonly=True, fld_background='lightgreen')
        fb.field('dst_sm_model_col__id', hasDownArrow=True,
                condition='@sm_model__id.id=:selected_model',
                condition_selected_model='=.@sm_ruleset__id.@dst_sm_model__id.id',
                columns = '$code,$description',
                auxColumns = '$code,$description',
                fld_background='lightgreen')
        fb.field('@dst_sm_model_col__id.description', readonly=True, fld_background='lightgreen')

        valori = self.db.table('sm.sm_ruleset_entry').CONST_operation()
        fb.field('operation', tag='filteringSelect', values=valori)
        # fb.div()
        # fb.div()
        # fb.div()

        # fb.field('src_sm_model__id')
        # fb.field('dst_sm_model__id')

    def rulesetEntryBody(self, pane):
        tc = pane.tabContainer()

        # tab operations
        tm = tc.contentPane(title='!![it]Operazioni')
        tm.div('...todo...')
    
    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromRuleset(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.95) #, modal=True)