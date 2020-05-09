#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

from gnr.core.gnrbag import Bag

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
                        #where='$sm_model__id=:model__id', model__id=current_model,
                        order_by='$description'
                        ).fetch()

        dict_categories = []
        dict_categories.append(dict(code='tutti', caption='!![it]Tutti'))
        
        for d in categories:
            dict_categories.append(
                dict(code=d['description'], 
                        caption=d['description'],
                        condition='@sm_model__id.@sm_category__id.description=:desc',
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
        bc = form.center.borderContainer()

        self.registryHeader(bc.contentPane(region='top', datapath='.record'))
        self.registryBody(bc.contentPane(region='center'))
        self.registryButtons(bc.contentPane(region='bottom'))

    def registryHeader(self, pane):
        div1 = pane.div(margin='2px', 
                border='1px solid silver',
                rounded=5,
                shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=3, border_spacing='4px')

        fb.field('code', validate_nodup=True, validate_case='upper')
        fb.field('@sm_model__id.@sm_category__id.description', readOnly=True)
        fb.div()

        fb.field('sm_model__id', auxColumns='$description,@sm_category__id.description', 
                hasDownArrow=True)
        fb.field('@sm_model__id.description', readOnly=True,
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

        frame = sb.bagGrid(#frameCode='registry_model',datapath='#FORM.model_dati',
                            storepath='#FORM.record.storebag',
                            structpath='#FORM.record.registrystruct')

        # activities log
        log = tc.contentPane(title='!![it]Log attività')
        log.dialogTableHandler(relation='@data_registry_log',
                 viewResource='ViewFromDataRegistry',
                 formResource='FormFromDataRegistry',
                 margin='2px')

    def registryButtons(self, pane):
        fb = pane.formbuilder(cols=10, border_spacing='4px', align='left')

        fb.dataRpc('.reloadSchema', self.proxyRebuildStoreBag, 
        record='=.record', 
        _fired='^.action_recreate_storeBag')

        action_ricrea = '''
            var optsel = confirm("Ricostruzione schema?"); 
            if (optsel == true) {  
                FIRE .action_recreate_storeBag;
                }  
            else {  
                alert("Operazione annullata...");
                }
            '''
        fb.button('!![it]Ricrea schema', action=action_ricrea,
                disabled='^.controller.locked')
                #fire='.action_run_batch')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        structure_bag = self.db.table('sm.sm_model').getStructBagFromModel(record['sm_model__id'])
        record['registrystruct'] = structure_bag

    @public_method
    def proxyRebuildStoreBag(self, record=None, **kwargs):
        return self.db.table('sm.sd_data_registry').buildUpStoreBag(record, 0)
