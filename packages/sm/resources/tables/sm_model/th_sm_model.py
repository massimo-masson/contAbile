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
        r.fieldcell('sm_category__id')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)

    def th_top_barcategory(self, top):
        top.slotToolbar('5,sections@sm_category__id,*',
                childname='dummy',
                _position='<bar', 
                sections_sm_category__id_multiButton=6)
                #, gradient_from='#999', gradient_to='#666')


class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.anagraficaInfo(bc.contentPane(region='top', datapath='.record'))
        self.anagraficaRows(bc.contentPane(region='left', width='50%'))
        self.anagraficaCols(bc.contentPane(region='right', width='50%'))
        

    def anagraficaInfo(self, pane):
        fb = pane.formbuilder(cols=4, border_spacing='4px')
        fb.field('code')
        fb.field('description')
        fb.field('sm_category__id', hasDownArrow=True)
        fb.field('@sm_category__id.description', readonly=True,
            lbl=':', lbl_color='darkblue', fld_background='lightgrey')
        fb.field('notes', colspan=4, width='100%', 
            tag='simpleTextArea', height='10ex')

    def anagraficaRows(self, pane):
        pane.inlineTableHandler(relation='@rows',
                pbl_classes=True,
                viewResource='ViewFromModel',
                grid_selfDragRows=True,
                margin='2px',
                searchOn=True)

    def anagraficaCols(self, pane):
        pane.inlineTableHandler(relation='@columns',
                pbl_classes=True,
                viewResource='ViewFromModel',
                grid_selfDragRows=True,
                margin='2px',
                searchOn=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
