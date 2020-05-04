#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sd: process batch entry'''
        tbl = pkg.table('sd_process_entry', pkey='id', 
                name_long='!![it]Fase elaborazione',
                name_plural='!![it]Fasi elaborazione',
                caption_field='description')

        self.sysFields(tbl)

        tbl.column('position', dtype='N',
                name_long='!![it]Posizione', name_short='!![it]Fase')

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione')

        # relation to sd_process_batch
        tbl.column('sd_process_batch__id', size='22', group='_', 
                name_long='!![it]Lotto di elaborazione', name_short='!![it]Lotto',
                validate_notnull=True
                ).relation('sm.sd_process_batch.id', relation_name='process_entries', 
                mode='foreignkey', onDelete='raise')
        
        # relation to sm_ruleset
        tbl.column('sm_ruleset__id', size='22', group='_', 
                name_long='!![it]Regole di elaborazione', name_short='!![it]Regole',
                validate_notnull=True
                ).relation('sm.sm_ruleset.id', relation_name='process_entries', 
                mode='foreignkey', onDelete='raise')

        # relation to source schema
        tbl.column('src_sd_data_registry__id', size='22', group='_', 
                name_long='!![it]Schema sorgente', name_short='!![it]Src',
                validate_notnull=True
                ).relation('sm.sd_data_registry.id', relation_name='src_process_entries', 
                mode='foreignkey', onDelete='raise')

        # relation to destination schema
        tbl.column('dst_sd_data_registry__id', size='22', group='_', 
                name_long='!![it]Schema destinazione', name_short='!![it]Dst',
                validate_notnull=True
                ).relation('sm.sd_data_registry.id', relation_name='dst_process_entries', 
                mode='foreignkey', onDelete='raise')
