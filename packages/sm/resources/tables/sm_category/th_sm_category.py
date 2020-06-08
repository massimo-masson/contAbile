#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('notes')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='', runOnStart=True)

    def th_options(self):
        return dict(widget='border')


class Form(BaseComponent):

    def th_form(self, form):
        # pane = form.record
        # fb = pane.formbuilder(cols=2, border_spacing='4px')
        bc = form.center.borderContainer()
        self.categoryInfo(bc.contentPane(region = 'top', datapath = '.record'))
        self.categoryBody(bc.contentPane(region = 'center'))

    def categoryInfo(self, pane):
        fb = pane.formbuilder(cols = 3, border_spacing = '4px')

        fb.field('code')
        fb.field('description', colspan = 2, width = '100%')

        fb.field('notes', colspan = 2, width = '100%', height = '100%')

    def categoryBody(self, pane):
        tc = pane.tabContainer()

        # tab parameters
        tab_parameters = tc.contentPane(title = '!![it]Parametri')
        tab_parameters.dialogTableHandler(relation = '@category_parameters',
                pbl_classes = True,
                viewResource = 'ViewFromCategory',
                formResource = 'FormFromCategory',
                grid_selfDragRows = True,
                margin = '2px',
                searchOn = True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
