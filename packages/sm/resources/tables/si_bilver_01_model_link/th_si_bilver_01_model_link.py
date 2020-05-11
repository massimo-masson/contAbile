#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('si_bilver_01_model__id')
        r.fieldcell('ext_code')
        r.fieldcell('ext_description')
        r.fieldcell('sm_model_row__id')
        r.fieldcell('sm_model_col__id')

    def th_order(self):
        return 'si_bilver_01_model__id'

    def th_query(self):
        return dict(column='si_bilver_01_model__id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('si_bilver_01_model__id')
        fb.field('ext_code')
        fb.field('ext_description')
        fb.field('sm_model_row__id')
        fb.field('sm_model_col__id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
