#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice')
        r.fieldcell('descrizione')
        r.fieldcell('tipo_campo')
        r.fieldcell('posizione')
        r.fieldcell('note')
        r.fieldcell('sm_anagrafica')

    def th_order(self):
        return 'codice'

    def th_query(self):
        return dict(column='codice', op='contains', val='')

class ViewFromAnagrafica(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice', edit=True)
        r.fieldcell('descrizione', edit=True)
        r.fieldcell('tipo_campo', edit=True)
        r.fieldcell('posizione', edit=True)
        r.fieldcell('note', edit=True)
        #r.fieldcell('sm_anagrafica', edit=True)

    def th_order(self):
        return 'posizione'

    def th_query(self):
        return dict(column='codice', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('codice')
        fb.field('descrizione')
        fb.field('tipo_campo')
        fb.field('note')
        fb.field('sm_anagrafica')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
