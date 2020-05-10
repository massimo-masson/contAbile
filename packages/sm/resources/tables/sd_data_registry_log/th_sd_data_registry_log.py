#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('sd_data_registry__id')
        r.fieldcell('date_elab')
        r.fieldcell('notes')
        r.fieldcell('current_user')
        r.fieldcell('ruleset')
        r.fieldcell('schema_source')
        r.fieldcell('source_storebag')
        r.fieldcell('previous_storebag')

    def th_order(self):
        return 'sd_data_registry__id'

    def th_query(self):
        return dict(column='sd_data_registry__id', op='contains', val='')

class ViewFromDataRegistry(View):
    pass

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('sd_data_registry__id', hasDownArrow=True)
        fb.field('date_elab')
        fb.field('notes')
        fb.field('current_user')
        fb.field('ruleset')
        fb.field('schema_source')
        fb.field('source_storebag', readonly=True)
        fb.field('previous_storebag', readonly=True)


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormFromDataRegistry(Form):
    pass    
