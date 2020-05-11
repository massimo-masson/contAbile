#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('si_bilver_01_lot__lot_code')
        r.fieldcell('ext_code')
        r.fieldcell('ext_description')
        r.fieldcell('ext_value')

    def th_order(self):
        return 'ext_code'

    def th_query(self):
        return dict(column='ext_code', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px')

        # row
        fb.field('si_bilver_01_lot__lot_code', hasDownArrow=True)
        fb.field('@si_bilver_01_lot__lot_code.description', readonly=True)

        # row
        fb.field('ext_code')
        fb.field('ext_description')

        # row
        fb.field('ext_value')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromLot(View):
    pass

class FormFromLot(Form):
    pass