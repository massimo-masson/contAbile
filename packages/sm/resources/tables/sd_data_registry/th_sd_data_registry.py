#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

from gnr.core.gnrbag import Bag
import datetime
import random

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
        r.fieldcell('last_import')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column = 'code', op = 'contains', val = '', runOnStart = True)

    #def th_top_barmodel_category(self, top):
    #    top.slotToolbar('5,sections@model_category,*',
    #            childname='dummy',
    #            _position='<bar', 
    #            sections_model_category_multiButton=6)

    def th_top_barcategory(self, top):
        top.slotToolbar('5,sections@category,*',
                childname = 'category', _position = '<bar', 
                sections_category_multiButton = 7)

    def th_sections_category(self):
        categories = self.db.table('sm.sm_category').query(
                        columns = '$code, $description',
                        #where='$sm_model__id=:model__id', model__id=current_model,
                        order_by = '$description'
                        ).fetch()

        dict_categories = []
        dict_categories.append(dict(code = 'tutti', caption = '!![it]Tutti'))
        
        for d in categories:
            dict_categories.append(
                # dict(code=d['description'], 
                #         caption=d['description'],
                #         condition='@sm_model__id.@sm_category__id.description=:desc',
                #         condition_desc=d['description'])
                dict(code = d['code'], 
                        caption = d['description'],
                        condition = '@sm_model__id.@sm_category__id.code=:code',
                        condition_code = d['code'])
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

        self.registryHeader(bc.contentPane(region = 'top', datapath = '.record'))
        self.registryBody(bc.contentPane(region = 'center'))
        self.registryButtons(bc.contentPane(region = 'bottom'))

    def registryHeader(self, pane):
        div1 = pane.div(margin = '2px', 
                border = '1px solid silver',
                rounded = 5,
                shadow = '4px 4px 8px #666')

        fb = div1.formbuilder(cols = 3, border_spacing = '4px')

        fb.field('code', validate_nodup = True, validate_case = 'upper')
        fb.field('@sm_model__id.@sm_category__id.description', readOnly = True)
        fb.field('last_import', readOnly = True)

        fb.field('sm_model__id', auxColumns = '$description,@sm_category__id.description', 
                hasDownArrow = True)
        fb.field('@sm_model__id.description', readOnly = True,
                background_color = 'light_grey',
                colspan = 2, width = '100%')

        fb.field('date_ref_period')
        fb.field('date_ref_from')
        fb.field('date_ref_to')

        fb.field('description', colspan = 1, width = '100%')
        fb.field('status', readOnly = True)
        fb.field('is_protected')

        fb.field('notes', tag = 'simpletextarea', colspan = 3, widht = '100%', height = '5em')

    def registryBody(self, pane):
        tc = pane.tabContainer()

        # storebag schema
        sb = tc.contentPane(title = '!![it]Schema')

        frame = sb.bagGrid(#frameCode='registry_model',
                            datapath = '#FORM.model_dati',
                            storepath = '#FORM.record.storebag',
                            structpath = '#FORM.record.registrystruct')

        # schema parameters
        params = tc.contentPane(title = '!![it]Parametri schema')
        params.dialogTableHandler(relation = '@schema_parameters',
                 viewResource = 'ViewFromSchema',
                 formResource = 'FormFromSchema',
                 margin = '2px')

        # activities log
        log = tc.contentPane(title = '!![it]Log attività')
        log.dialogTableHandler(relation = '@data_registry_log',
                 viewResource = 'ViewFromDataRegistry',
                 formResource = 'FormFromDataRegistry',
                 margin = '2px')

        # Import data tab
        imp = tc.contentPane(title = '!![it]Importazione dati')
        self.registryImportPanel(imp)

    def registryImportPanel(self, pane):
        fb = pane.formbuilder(cols = 1, border_spacing = '4px', colswidth = 'auto')
        
        fb.div('!![it]Selezionare un lotto di dati da bilancio di verifica e importare',
                background_color = 'lightgreen')
        fb.div('!![it]Si possono selezionare solo lotti con modello corrispondente \
                a quello dello schema corrente', background_color = 'lightgreen'
                )

        action_runImport = '''
            var optsel = confirm("Importazione dati lotto nello schema?"); 
            if (optsel == true) {  
                FIRE .action_run_import;
                //window.location.reload(false);
                //this.form.reload()
                }  
            else {  
                alert("Operazione annullata...");
                }
            '''
        pane.dataRpc('.dummy', self.proxyImportBilVer01_lot, 
                    record = '=.record', 
                    lot_code = '=.import.lot',
                    _fired = '^.action_run_import',
                    _onResult = 'this.form.reload()'
                    )

        fb.dbselect(value = '^.import.lot',
                    lbl = '!![it]Lotto da importare',
                    table = 'sm.si_bilver_01_lot', rowcaption = '$lot_code,$description',
                    condition = '@si_bilver_01_model__code.@sm_model__id.id=:current_model',
                    condition_current_model = '=.record.@sm_model__id.id',
                    hasDownArrow = True
                    )

        fb.button('!![it]Importazione', width='20em', 
                action = action_runImport,
                disabled = '^.controller.locked',
                _onResult = '''alert("Operazione terminata");'''
                )

    def registryButtons(self, pane):
        fb = pane.formbuilder(cols = 10, border_spacing = '4px', align = 'left')
        
        self.registryButtonRicrea(fb)
        self.registryButtonValoriACaso(fb)
        self.registryButtonStampaBag(fb)

    def registryButtonRicrea(self, pane):
        pane.dataRpc('.reloadSchema', self.proxyRebuildStoreBag, 
        record = '=.record', 
        _fired = '^.action_recreate_storeBag',
        _onResult = 'this.form.reload()'
        )

        action_ricrea = '''
            var optsel = confirm("Ricostruzione schema?"); 
            if (optsel == true) {  
                FIRE .action_recreate_storeBag;
                //window.location.reload(false);
                }  
            else {  
                alert("Operazione annullata...");
                }
            '''
        pane.button('!![it]Ricrea schema', 
                action = action_ricrea,
                disabled='^.controller.locked')
                #fire='.action_run_batch')

    def registryButtonValoriACaso(self, pane):
        pane.dataRpc('.dummy', self.ValoriACaso, 
        record = '=.record',
        _fired = '^.ValoriACaso',
        _onResult = 'this.form.reload()'
        )

        action_random = '''
            var optsel = confirm("Riempio con valori a caso?"); 
            if (optsel == true) {  
                FIRE .ValoriACaso;
                //window.location.reload(false);
                }  
            '''
        pane.button('!![it]Valori a caso', 
                action = action_random,
                disabled = '^.controller.locked')

    def registryButtonStampaBag(self, pane):
        pane.dataRpc('.dummy', self.StampaBag,
                record = '=.record',
                _fired = '^.StampaBag',
                #_onResult = 'this.form.reload()'                
                )

        action_StampaBag = '''
            var optsel = confirm("Stampo Bag?"); 
            if (optsel == true) {  
                FIRE .StampaBag;
                }  
            '''
        pane.button('!![it]Stampa Bag', 
                action = action_StampaBag,
                disabled = '^.controller.locked')

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        structure_bag = self.db.table('sm.sm_model').getStructBagFromModel(record['sm_model__id'])
        record['registrystruct'] = structure_bag

    @public_method
    def proxyRebuildStoreBag(self, record = None, **kwargs):
        b = self.db.table('sm.sd_data_registry').buildUpStoreBag(record, 0)

        record['storebag'] = b
        record['status'] = 'ELABORABILE'
        record['last_import'] = ''
        self.db.table('sm.sd_data_registry').update(record)
        self.db.commit()
        return b

    @public_method
    def proxyImportBilVer01_lot(self, record, lot_code, **kwargs):
        b = self.db.table('sm.si_bilver_01_lot').import_lot(
                        record['id'],
                        lot_code
                        )
        #print('storebag ottenuta:', b)
        record['storebag'] = b
        record['status'] = 'IMPORTED'
        record['last_import'] = datetime.datetime.now()
        self.db.table('sm.sd_data_registry').calcStoreBag(record['sm_model__id'], record['storebag'])
        self.db.table('sm.sd_data_registry').update(record)
        self.db.commit()
        return b

    @public_method
    def ValoriACaso(self, record = None, **kwargs):
        for r in record['storebag'].keys():
            for c in record['storebag'][r].keys():
                if c == 'code':
                    pass
                elif c == 'description':
                    pass
                else:
                    #record['storebag'][r][c] = random.randrange(200, 3000)
                    v  = random.randrange(200, 3000)
                    self.db.table('sm.sd_data_registry')\
                        .setStoreBagCellValue(record['storebag'], r, c, v)        
        record['status'] = 'RANDOM'
        record['last_import'] = ''
        self.db.table('sm.sd_data_registry').calcStoreBag(record['sm_model__id'], record['storebag'])
        self.db.table('sm.sd_data_registry').update(record)
        self.db.commit()
        return

    @public_method
    def StampaBag(self, record = None, **kwargs):
        print(record['storebag'])