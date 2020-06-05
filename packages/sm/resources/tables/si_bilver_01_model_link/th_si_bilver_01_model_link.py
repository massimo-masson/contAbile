#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('si_bilver_01_model__code')
        #r.fieldcell('si_bilver_01_model__id')
        r.fieldcell('ext_code')
        r.fieldcell('ext_description')
        r.fieldcell('sm_model_row__id')
        r.fieldcell('@sm_model_row__id.description')
        r.fieldcell('sm_model_col__id')
        r.fieldcell('@sm_model_col__id.description')
        r.fieldcell('invert_sign')

    def th_order(self):
        return 'si_bilver_01_model__code'

    def th_query(self):
        return dict(column = 'si_bilver_01_model__code', op = 'contains', val = '')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols = 2, border_spacing = '4px')
        fb.field('si_bilver_01_model__code', hasDownArrow = True)
        fb.field('ext_code', hasDownArrow = True)
        
        fb.field('ext_description', hasDownArrow = True,
                colspan = 2, width = '100%')

        fb.field('sm_model_row__id', hasDownArrow = True,
                columns = '$code,$description',       # colonne su cui si ricerca
                auxColumns = '$code,$description',    # colonne visualizzate
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@si_bilver_01_model__code.@sm_model__id.id'
                )
        fb.field('@sm_model_row__id.description', readonly = True)
        
        fb.field('sm_model_col__id', hasDownArrow = True,
                columns = '$code,$description',
                auxColumns = '$code,$description',
                condition = '@sm_model__id.id = :selected_model',
                condition_selected_model = '=.@si_bilver_01_model__code.@sm_model__id.id'
                )
        fb.field('@sm_model_col__id.description', readonly = True)

        fb.field('invert_sign')

    def th_options(self):
        return dict(dialog_height = '400px', dialog_width = '600px')


class ViewFromBilVer01Model(View):
    
    def th_top_lotrows(self, top):
        top.bar.replaceSlots('#','#,importer') 


class FormFromBilVer01Model(Form):
    
    def th_options(self):
        return dict(dialog_parentRatio = 0.8, modal = False)