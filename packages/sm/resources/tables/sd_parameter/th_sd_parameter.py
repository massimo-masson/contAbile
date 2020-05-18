#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('type')
        r.fieldcell('sm_parameter_class__id')
        r.fieldcell('sm_model__id')
        r.fieldcell('sd_data_registry__id')
        r.fieldcell('status')
        r.fieldcell('value')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')

        fb.field('code')
        fb.field('description')

        fb.field('type')
        fb.div()

        fb.field('sm_parameter_class__id', hasDownArrow=True)
        fb.field('@sm_parameter_class__id.description')

        fb.field('sm_model__id', hasDownArrow=True)
        fb.field('@sm_model__id.description')

        fb.field('sd_data_registry__id', hasDownArrow=True)
        fb.field('@sd_data_registry__id.description')

        fb.field('value')
        fb.field('status')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
