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

    def runBatch(self, batch_id=None):
        '''Run the process entries on specified schema'''
        if batch_id==None:
            print("No process batch to run")
        
        # 1.    get the batch from sd_process_batch, based on batch_id
        # 2.    get the batch_entries from the batch
        # 3.    loop on batch entries, get single sd_proces_entry
        # 4.        get the ruleset for the sd_process_entry
        # 5.        get the source schema from sd_process_entry
        # 6.        get the destination schema from sd_process_entry
        # 7.        verify that the destination is not protected
        # 8.            make "history/backup" copy of source schema before processing
        # 9.            apply the ruleset from source to destination
        # 10.            update destination schema
        # 11.            log activities and previous version schema
        # 12.   update status
        # 13.   protect destination schemas? (maybe not...)

        status = 'process_batch starting...'

        # 1. get batch record to work on, in rsbag_batch
        # rsbag is recordset in bag form
        rsbag_batch = self.getBatchFromId(batch_id)
        #print('****running batch: ', rsbag_batch)

        # 2. get batch entries
        rs_entries = self.getBatchEntriesList(batch_id)
        #print('****rsbag_entries: ', rs_entries_id)

        # 3. loop every entry for processing
        for entry in rs_entries:
            print('elabora sd_batch_entry:', entry['description'])

        # END OF runBatch()
        return status


    def getBatchFromId(self, batch_id):
        '''return the recordset with pk id=batch_id in bag form'''
        rs = self.db.table('sm.sd_process_batch').record(batch_id).output('bag')
        return rs

    def getBatchEntriesList(self, batch_id):
        '''return the ordered list of entries for the given process_batch'''
        rs = self.db.table('sm.sd_process_entry').query(
                columns='*',
                where='$sd_process_batch__id = :selected_batch_id',
                order_by='position',
                selected_batch_id=batch_id,
                mode='bag'
                ).fetch()
        return rs

