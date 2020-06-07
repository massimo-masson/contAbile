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
        r.fieldcell('initialize_destination')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column = 'code', op = 'contains', val = '', runOnStart = True)


class Form(BaseComponent):

    def th_form(self, form):
        # pane = form.record
        # bc = pane.borderContainer()
        # self.rulesetHeader(bc.contentPane(region='top'))
        # self.rulesetBody(bc.contentPane(region='center'))
        
        bc = form.center.borderContainer()
        #self.rulesetHeader(bc.contentPane(region = 'top', datapath = '.record', nodeId = 'PIERO'))
        self.rulesetHeader(bc.contentPane(region = 'top', datapath = '.record'))
        self.rulesetBody(bc.contentPane(region = 'center'))

    def rulesetHeader(self, pane):
        fb = pane.formbuilder(cols = 4, border_spacing = '4px')
        fb.field('code')
        fb.field('description', colspan = 3, width = '100%')

        fb.field('src_sm_model__id', hasDownArrow = True, background = 'gold')
        fb.field('@src_sm_model__id.@sm_category__id.description',
                readonly = True, background = 'gold')
        fb.field('dst_sm_model__id', hasDownArrow = True, background = 'lightgreen')
        fb.field('@dst_sm_model__id.@sm_category__id.description',
                readonly = True, background = 'lightgreen')

        fb.field('@src_sm_model__id.description', readonly = True,
                colspan = 2, width = '100%', background = 'gold')
        fb.field('@dst_sm_model__id.description', readonly = True,
                colspan = 2, width = '100%', background = 'lightgreen')

        fb.field('initialize_destination')
        fb.field('notes', colspan = 3, width = '100%',
                editor = True, tag = 'simpleTextArea',
                height = '6em')

    def rulesetBody(self, pane):
        tc = pane.tabContainer()

        # schema modesl, source and destination
        smsd = tc.contentPane(title = '!![it]Modelli origine e destinazione')
        bc = smsd.borderContainer()
        self.getModelSrc(bc.contentPane(region = 'left', width = '50%'))
        self.getModelDst(bc.contentPane(region = 'right', width = '50%'))

        # registry entries rules
        rer = tc.contentPane(title = '!![it]Operazioni componenti la regola')
        rer.dialogTableHandler(relation = '@ruleset_entries',
                 viewResource = 'ViewFromRuleset',
                 formResource = 'FormFromRuleset',
                 margin = '2px')        

    @public_method
    def proxyStoreBagFromModel(self, model = None, **kwargs):
        '''Interroga il metodo getStoreBagFromModel per avere la bag che descrive
        la struttura del modello'''
        modelBag = self.db.table('sm.sd_data_registry').getStoreBagFromModel(model)
        return modelBag

    # QUESTA VERSIONE RESTITUIREBBE LE DUE BAG CONTEMPORANEAMENTE
    # ---------------------------------------------------------
    # @public_method
    # def proxyStoreBagFromModel(self, model_src=None, model_dst=None, **kwargs):
    #     srcModelBag = self.db.table('sm.sd_data_registry').getStoreBagFromModel(model_src)
    #     dstModelBag = self.db.table('sm.sd_data_registry').getStoreBagFromModel(model_dst)
    #     return Bag(dict(srcModelBag=srcModelBag, dstModelBag=dstModelBag))

    def getModelSrc(self, pane):
        pane.div('!![it]Modello sorgente', 
                color = 'black', background = 'gold')

        # VERSIONE CON DUE BAG CONTEMPORANEAMENTE
        # pane.dataRpc('.ModelBag', self.proxyStoreBagFromModel, 
        #             #modello='^#FORM.record.src_sm_model_row__id', _if='modello')
        #             model_src='^#PIERO.src_sm_model_row__id', #_if='model_src',
        #             model_dst='=#PIERO.dst_sm_model_row__id')

        pane.dataRpc('.srcModelBag', self.proxyStoreBagFromModel, 
                model = '^.record.src_sm_model__id',
                _fired = '^.record.src_sm_model__id')
        
        pane.quickGrid('^.srcModelBag', border = '1px solid silver',
                height = '90%', width = '90%', margin = '20px')

    def getModelDst(self, pane):
        pane.div('!![it]Modello destinazione',
                color = 'black', background = 'lightgreen')
        pane.dataRpc('.dstModelBag', self.proxyStoreBagFromModel, 
                model = '^.record.dst_sm_model__id',
                _fired = '^.record.dst_sm_model__id')
        
        pane.quickGrid('^.dstModelBag', border = '1px solid silver',
                height = '90%', widht = '90%', margin = '20px')

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')