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
        r.fieldcell('model_category')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)

    #def th_top_barmodel_category(self, top):
    #    top.slotToolbar('5,sections@model_category,*',
    #            childname='dummy',
    #            _position='<bar', 
    #            sections_model_category_multiButton=6)

    def th_top_barcategory(self, top):
        top.slotToolbar('5,sections@category,*',
                childname='category', _position='<bar', 
                sections_category_multiButton=6)

    def th_sections_category(self):
        categories=self.db.table('sm.sm_category').query(
                        columns='$code, $description',
                        #where='$sm_model_id=:model_id', model_id=current_model,
                        order_by='$description'
                        ).fetch()

        dict_categories = []
        dict_categories.append(dict(code='tutti', caption='!![it]Tutti'))
        
        for d in categories:
            dict_categories.append(
                dict(code=d['description'], 
                        caption=d['description'],
                        condition='@sm_model_id.@sm_category_id.description=:desc',
                        condition_desc=d['description'])
            )

        #return [
        #    dict(code='tutti', caption='!![it]Tutti'),
        #    dict(code='clienti', caption='!![it]Clienti', condition='$is_cliente=1'),
        #    dict(code='fornitori', caption='!![it]Fornitori', condition='$is_fornitore=1')
        #]
        return dict_categories


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        bc = pane.borderContainer()
        self.registryHeader(bc.contentPane(region='top'))
        self.registryBody(bc.contentPane(region='center'))
        # self.registryButtons(bc.contentPane(region='bottom'))

    def registryHeader(self, pane):
        div1 = pane.div(margin='2px', 
                border='1px solid silver',
                rounded=5,
                shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=3, border_spacing='4px')

        fb.field('code', validate_nodup=True, validate_case='upper')
        fb.field('@sm_model_id.@sm_category_id.description', readOnly=True)
        fb.div()

        fb.field('sm_model_id', auxColumns='$description,@sm_category_id.description', 
                hasDownArrow=True)
        fb.field('@sm_model_id.description', readOnly=True,
                background_color='light_grey',
                colspan=2, width='100%')

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
