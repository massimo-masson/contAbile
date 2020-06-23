#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# contAbile:sm (schema manager), an automated processor for data based on
# models and flexible processing logic built by users.
# Copyright (C) 2020 Massimo Masson
# 
# This program is dual-licensed.
# 
# Option 1:
# If you respect the terms of GNU GPL license, AND
# you agree to give the copyright for modifications or derivative work
# to the original author Massimo Masson, the GPL license applies.
# In this case:
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# Option 2:
# If you do not agree with any of the statements in option 1, then
# a proprietary license applies. In this case, contact the author
# for a dedicated propietary license.
# 

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
                _onResult = 'this.form.reload(); alert("Elaborazione completata")'
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