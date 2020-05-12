#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('lot_code')
        r.fieldcell('description')

    def th_order(self):
        return 'lot_code'

    def th_query(self):
        return dict(column='lot_code', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()

        self.LotHeader(bc.contentPane(region='top', datapath='.record'))
        self.LotBody(bc.contentPane(region='center'))

    def LotHeader(self, pane):
        div1 = pane.div(margin='2px', border='1px solid silver',
                        rounded=5, shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=2, border_spacing='4px')
        fb.field('lot_code')
        fb.field('description')

        fb.div('!![it]Per importazione dati utilizzare nella prima colonna il codice del lotto.',
                colspan=2, width='100%', background='lightgreen')

    def LotBody(self, pane):
        tc = pane.tabContainer()

        # Lot rows
        lot = tc.contentPane(title='!![it]Dati')

        # activities log
        cp = lot.contentPane(title='!![it]Righe lotto')
        cp.dialogTableHandler(relation='@bilver_01_rows',
                 viewResource='ViewFromLot',
                 formResource='FormFromLot',
                 export=True,
                 margin='2px')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
