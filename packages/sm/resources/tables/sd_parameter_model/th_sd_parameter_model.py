#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('value')
        r.fieldcell('sm_parameter_class__id')
        #r.fieldcell('sm_model__id')
        r.fieldcell('@sm_model__id.description')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column = 'code', op = 'contains', val = '', runOnStart = True)


class ViewFromModel(View):
    pass


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols = 3, border_spacing = '4px')
        
        fb.field('code')
        fb.field('description', colspan = 2, width = '100%')

        fb.field('sm_parameter_class__id')
        fb.field('@sm_parameter_class__id.description', readonly = True, 
                colspan = 2, width = '100%')

        fb.field('sm_model__id')
        fb.field('@sm_model__id.description', readonly = True,
                colspan = 2, width = '100%')

        fb.field('value')
        fb.div(colspan = 2)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class FormFromModel(Form):

    def th_options(self):
        return dict(dialog_parentRatio = 0.9, modal = False)