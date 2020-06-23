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
        r.fieldcell('sm_model__id')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()

        self.ModelHeader(bc.contentPane(region='top', datapath='.record'))
        self.ModelBody(bc.contentPane(region='center'))

    def ModelHeader(self, pane):
        div1 = pane.div(margin='2px', border='1px solid silver',
                        rounded=5, shadow='4px 4px 8px #666')

        fb = div1.formbuilder(cols=2, border_spacing='4px')

        fb.field('code')
        fb.field('description')

        fb.field('sm_model__id', hasDownArrow=True)
        fb.field('@sm_model__id.description')

        fb.field('code', background='lightgreen', readonly=True,
                lbl='!![it]Codice per importazione'
                )
        fb.div('!![it]Utilizzare il codice indicato come colonna chiave per importazione dati.')

    def ModelBody(self, pane):
        tc = pane.tabContainer()

        # links
        lp = tc.contentPane(title='!![it]Dettaglio')

        # activities log
        cp = lp.contentPane(title='!![it]Collegamenti')
        cp.dialogTableHandler(relation='@bilver_01_links',
                 viewResource='ViewFromBilVer01Model',
                 formResource='FormFromBilVer01Model',
                 export=True,
                 margin='2px')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
