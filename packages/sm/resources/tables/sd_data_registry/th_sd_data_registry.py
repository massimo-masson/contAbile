#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('date_ref_period')
        r.fieldcell('description')
        #r.fieldcell('notes')
        r.fieldcell('status')
        r.fieldcell('date_ref_from')
        r.fieldcell('date_ref_to')
        r.fieldcell('is_protected')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        # fb = pane.formbuilder(cols=2, border_spacing='4px')
        # fb.field('code')
        # fb.field('description')
        # fb.field('notes')
        # fb.field('status', readOnly=True)
        # fb.field('date_ref_from')
        # fb.field('date_ref_to')
        # fb.field('date_ref_period')
        # fb.field('is_protected')
        #fb.field('storebag', tag='simpletextarea', colspan=2, width='100%')
        bc = pane.borderContainer()
        self.registryHeader(bc.contentPane(region='top'))
        self.registryBody(bc.contentPane(region='center'))
        self.registryButtons(bc.contentPane(region='bottom'))

    def registryHeader(self, pane):
        div1 = pane.div(margin='2px', 
                border='1px solid silver',
                rounded=5,
                shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=3, border_spacing='4px')

        fb.field('code', validate_nodup=True)
        fb.field('sm_model_id', hasDownArrow=True)
        fb.field('@sm_model_id.description', lbl=':', readOnly=True,
                background_color='light_grey')

        fb.field('date_ref_period')
        fb.field('date_ref_from')
        fb.field('date_ref_to')

        fb.field('description', colspan=1, width='100%')
        fb.field('status', readOnly=True)
        fb.field('is_protected')

        fb.field('notes', tag='simpletextarea', colspan=3, widht='100%', height='5em')

    def registryBody(self, pane):
        tc = pane.tabContainer()

        # storebag schema
        sb = tc.contentPane(title='!![it]Schema')
        sb.quickGrid('^.storebag', height='auto', widht='auto', margin='20px')

    def registryButtons(self, pane):
        fb = pane.formbuilder(cols=10, border_spacing='4px', align='right')
        action_ricostruzione = '''
            var optsel = confirm("Ricostruzione schema?"); 
            if (optsel == true) {  
                alert("Ora dovrei ricostruire...");
                }  
            else {  
                alert("Allora resta uguale...");
                }
            '''
        fb.button('!![it]Ricostruzione schema', action=action_ricostruzione)
        fb.button('!![it]BU!!', action='alert("Bu!")')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
