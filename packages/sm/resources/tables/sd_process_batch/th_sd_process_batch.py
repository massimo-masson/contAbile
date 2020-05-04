#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('date_ref_period')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.batchHeader(bc.contentPane(region='top', datapath='.record'))
        self.batchBody(bc.contentPane(region='center'))

    def batchHeader(self, pane):
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('code')
        fb.field('date_ref_period')

        fb.field('description', colspan=2, width='100%')

        fb.field('notes', tag='simpleTextArea',
                colspan=2, width='100%', height='6em')

    def batchBody(self, pane):
        tc = pane.tabContainer()
        entries = tc.contentPane(title='!![it]Fasi del processo di elaborazione')
        entries.dialogTableHandler(relation='@process_entries',
                 viewResource='ViewFromProcessBatch',
                 formResource='FormFromProcessBatch',
                 margin='2px')        

    def th_options(self):
        #return dict(dialog_height='400px', dialog_width='600px')
        return dict(dialog_parentRatio=0.9)        