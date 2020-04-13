#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice')
        r.fieldcell('descrizione')
        r.fieldcell('note')
        r.fieldcell('sm_classe')

    def th_order(self):
        return 'codice'

    def th_query(self):
        return dict(column='codice', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.anagraficaInfo(bc.contentPane(region='top', datapath='.record'))
        self.anagraficaRows(bc.contentPane(region='left', width='50%'))
        self.anagraficaCols(bc.contentPane(region='right', width='50%'))
        

    def anagraficaInfo(self, pane):
        fb = pane.formbuilder(cols=4, border_spacing='4px')
        fb.field('codice')
        fb.field('descrizione')
        fb.field('sm_classe', hasDownArrow=True)
        fb.field('@sm_classe.descrizione', readonly=True,
            lbl=':', lbl_color='darkblue', fld_background='lightgrey')
        fb.field('note', colspan=4, width='100%', 
            tag='simpleTextArea', height='10ex')

    def anagraficaRows(self, pane):
        pane.inlineTableHandler(relation='@righe',
                pbl_classes=True,
                viewResource='ViewFromAnagrafica',
                grid_selfDragRows=True,
                margin='2px',
                searchOn=True)

    def anagraficaCols(self, pane):
        pane.inlineTableHandler(relation='@colonne',
                pbl_classes=True,
                viewResource='ViewFromAnagrafica',
                grid_selfDragRows=True,
                margin='2px',
                searchOn=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
