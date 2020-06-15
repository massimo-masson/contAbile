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
        self.batchButtons(bc.contentPane(region='bottom'))

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

    def batchButtons(self, pane):

        fb = pane.formbuilder(cols=10, border_spacing='4px', align='left')
        action_run_batch = '''
            var optsel = confirm("Avviare elaborazione?"); 
            if (optsel == true) {  
                FIRE .action_run_batch;
                }  
            else {  
                alert("Elaborazione non avviata.");
                }
            '''
        # Attento, max!
        # in batch_id, NON usare ^.record.id, perche' sottoscrive il path
        # e verrebbe chiamato anche al load della form, che NON voglio!!!
        # con '=.record.id' invece prende il valore attuale, e basta. 
        # E all'on load non c'è l'id.
        # Quando invece viene attivato il "fired", allora scatta.
        fb.dataRpc('.runBatch', self.runBatch, 
                batch_id='=.record.id', 
                _fired='^.action_run_batch',
                _onResult = 'this.form.reload()'
                )

        # button enabled only if form is not locked (edit mode)
        fb.button('!![it]Elabora batch', action=action_run_batch,
                disabled='^.controller.locked',
                fire='.action_run_batch')

        # END OF Form
        
    @public_method
    def runBatch(self, batch_id=None, **kwargs):
        status = self.db.table('sm.sd_process_batch').runBatch(batch_id)
        return status

    def th_options(self):
        #return dict(dialog_height='400px', dialog_width='600px')
        return dict(dialog_parentRatio=0.9)        