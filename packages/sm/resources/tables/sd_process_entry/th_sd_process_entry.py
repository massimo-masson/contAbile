#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('position')
        r.fieldcell('description')
        r.fieldcell('sd_process_batch__id')
        r.fieldcell('sm_ruleset__id')
        r.fieldcell('src_sd_data_registry__id')
        r.fieldcell('dst_sd_data_registry__id')

    def th_order(self):
        return 'position'

    def th_query(self):
        return dict(column='position', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('position')
        fb.field('description')

        fb.field('sd_process_batch__id', hasDownArrow=True)
        fb.field('@sd_process_batch__id.description', readonly=True)

        fb.field('sm_ruleset__id', hasDownArrow=True)
        fb.field('@sm_ruleset__id.description', readonly=True)

        fb.field('src_sd_data_registry__id', hasDownArrow=True)
        fb.field('@src_sd_data_registry__id.description', readonly=True)

        fb.field('dst_sd_data_registry__id', hasDownArrow=True)
        fb.field('@dst_sd_data_registry__id.description', readonly=True)


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class ViewFromProcessBatch(View):
    pass

class FormFromProcessBatch(Form):

    def th_options(self):
        return dict(dialog_parentRatio=0.9)
