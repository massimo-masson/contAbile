#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('notes')
        r.fieldcell('src_sm_model__id')
        r.fieldcell('dst_sm_model__id')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        # pane = form.record
        # bc = pane.borderContainer()
        # self.rulesetHeader(bc.contentPane(region='top'))
        # self.rulesetBody(bc.contentPane(region='center'))
        
        bc = form.center.borderContainer()
        self.rulesetHeader(bc.contentPane(region='top', datapath='.record'))
        self.rulesetBody(bc.contentPane(region='center'))

    def rulesetHeader(self, pane):
        fb = pane.formbuilder(cols=4, border_spacing='4px')
        fb.field('code')
        fb.field('description', colspan=3, width='100%')

        fb.field('src_sm_model__id', hasDownArrow=True)
        fb.field('@src_sm_model__id.@sm_category__id.description', readonly=True)
        fb.field('dst_sm_model__id', hasDownArrow=True)
        fb.field('@dst_sm_model__id.@sm_category__id.description', readonly=True)

        fb.field('@src_sm_model__id.description', readonly=True,
                colspan=2, width='100%')
        fb.field('@dst_sm_model__id.description', readonly=True,
                colspan=2, width='100%')


        fb.field('notes', colspan=4, width='100%',
                editor=True, tag='simpleTextArea',
                height='8em')

    def rulesetBody(self, pane):
        tc = pane.tabContainer()

        # storebag schema
        sb = tc.contentPane(title='!![it]Operazioni componenti la regola')
        sb.dialogTableHandler(relation='@ruleset_entries',
                 viewResource='ViewFromRuleset',
                 formResource='FormFromRuleset',
                 margin='2px')
        

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
