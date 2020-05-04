#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sd: process batch

        batch of elaborations from schema to schema
        '''
        tbl = pkg.table('sd_process_batch', pkey='id', 
                name_long='!![it]Lotto elaborazioni',
                name_plural='!![it]Lotti elaborazioni',
                caption_field='code_description')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22',
                unmodifiable=True,      # can set code only on new record
                name_long='!![it]Codice lotto',
                unique=True, validate_notnull=True)
        
        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione schema')

        tbl.formulaColumn('code_description', 
                '"("||$code||") - "||$description', name_long='!![it]Lotti')
        
        tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')

        tbl.column('date_ref_period', dtype='A', size=':22',
                name_long='!![it]Periodo di riferimento')
