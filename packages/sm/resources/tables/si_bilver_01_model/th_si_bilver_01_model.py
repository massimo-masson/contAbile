#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('sm_model__id')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()

        self.ModelHeader(bc.contentPane(region='top', datapath='.record'))
        self.ModelBody(bc.contentPane(region='center'))

    def ModelHeader(self, pane):
        div1 = pane.div(margin='2px', border='1px solid silver',
                        rounded=5, shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=2, border_spacing='4px')

        fb.field('code')
        fb.field('description')

        fb.field('sm_model__id', hasDownArrow=True)
        fb.field('@sm_model__id.description')

        fb.field('code', background='lightgreen', readonly=True,
                lbl='!![it]Codice per importazione'
                )
        fb.div('!![it]Utilizzare il codice indicato come colonna chiave per importazione dati.')

    def ModelBody(self, pane):
        tc = pane.tabContainer()

        # links
        lp = tc.contentPane(title='!![it]Dettaglio')

        # activities log
        cp = lp.contentPane(title='!![it]Collegamenti')
        cp.dialogTableHandler(relation='@bilver_01_links',
                 viewResource='ViewFromBilVer01Model',
                 formResource='FormFromBilVer01Model',
                 export=True,
                 margin='2px')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
