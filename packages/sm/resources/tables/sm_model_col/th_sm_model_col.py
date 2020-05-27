#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('field_type')
        r.fieldcell('position')
        r.fieldcell('notes')
        r.fieldcell('sm_model__id')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='')

class ViewFromModel(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('position', edit=True)
        r.fieldcell('code', edit=True)
        r.fieldcell('description', edit=True)
        r.fieldcell('field_type', edit=True)
        r.fieldcell('notes', edit=True)

    def th_order(self):
        return 'position'

    def th_query(self):
        return dict(column='code', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('code')
        fb.field('description')
        fb.field('field_type')
        fb.field('notes')
        fb.field('sm_model__id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
