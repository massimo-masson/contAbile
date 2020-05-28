#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sd: process batch

        batch of elaborations from schema to schema
        '''
        tbl = pkg.table('sd_process_batch', pkey = 'id', 
                name_long = '!![it]Lotto elaborazioni',
                name_plural = '!![it]Lotti elaborazioni',
                caption_field = 'code_description')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22',
                unmodifiable = True,      # can set code only on new record
                name_long = '!![it]Codice lotto',
                unique = True, validate_notnull = True)
        
        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione schema')

        tbl.formulaColumn('code_description', 
                '"("||$code||") - "||$description', name_long = '!![it]Lotti')
        
        tbl.column('notes', dtype = 'A', size = ':1024', 
                name_long = '!![it]Note')

        tbl.column('date_ref_period', dtype = 'A', size = ':22',
                name_long = '!![it]Periodo di riferimento')

    def runBatch(self, batch_id = None):
        '''Run the process entries on specified schema'''
        if batch_id == None:
            print("No process batch to run")
        
        # 1.    get the batch from sd_process_batch, based on batch_id
        # 2.    get the batch_entries from the batch
        # 3.    loop on batch entries, get single sd_proces_entry
        # 4.        get the destination schema from sd_process_entry
        # 5.        verify that the destination is not protected
        # 6.        make "history/backup" copy of destination schema "before processing"
        # 7.        get the source schema from sd_process_entry
        # 8.        get the ruleset_entry list for the current sd_process_entry
        # 9.        loop on every rule of the ruleset
        # 10.          apply the rule from source to destination
        # 11.       update destination schema record
        # 12.       log activities and previous version schema
        # 13.   update batch status

        status = ''

        # 1. get batch record to work on, in rsbag_batch
        # rsbag is recordset in bag form
        rsbag_batch = self.getBatchFromId(batch_id)

        # 2. get batch entries
        rs_batch_entries = self.getBatchEntriesList(batch_id)

        # 3. loop every entry for processing, IN ORDER!
        for batch_entry in rs_batch_entries:

            # 4. get destination schema from sd_process_entry
            rs_dst_store = self.getSchemaStore(batch_entry['dst_sd_data_registry__id'])
            dst_storeBag = rs_dst_store['storebag']
            status += '\nprocessing ' + rs_dst_store['code']

            # 5. verify that destination is not protected
            # ***TO DO...***

            # 6. make a history copy of original storeBag before processing
            bkup_dst_storeBag = dst_storeBag.deepcopy()

            # 7. get source schema from sd_process_entry
            rs_src_store = self.getSchemaStore(batch_entry['src_sd_data_registry__id'])
            src_storeBag = rs_src_store['storebag']

            # 8. get ruleset enries list to apply, one by one, IN ORDER!
            rs_ruleset_entries = self.getRulesetEntriesList(batch_entry['sm_ruleset__id'])

            # 9. loop on every rule (ordered)
            for rule_entry in rs_ruleset_entries:
                #print('operazione', rule_entry['operation'])
                src_row = self.getModelRowById(rule_entry['src_sm_model_row__id'])
                src_col = self.getModelColById(rule_entry['src_sm_model_col__id'])
                dst_row = self.getModelRowById(rule_entry['dst_sm_model_row__id'])
                dst_col = self.getModelColById(rule_entry['dst_sm_model_col__id'])
                sr = src_row['code']
                sc = src_col['code']
                dr = dst_row['code']
                dc = dst_col['code']
                # print ('FROM: ', src_row['code'], '-', src_col['code'])
                # print ('  TO: ', dst_row['code'], '-', dst_col['code'])

                # 10. apply the single rule
                #dst_storeBag[dr][dc] = src_storeBag[sr][sc]
                self.applySingleRule(rule_entry['operation'], 
                        src_storeBag, sr, sc,
                        dst_storeBag, dr, dc)

            # 11. update destination schema
            self.updateDataRegistryStoreBag(rs_dst_store['id'], dst_storeBag)

            # 12. log processing for the destination schema
            self.logDestSchemaProcessing(rsbag_batch, rule_entry, 
                                            rs_src_store, rs_dst_store,
                                            src_storeBag,
                                            bkup_dst_storeBag)
        
        # 13. update status
        status += '\nprocessed.'
        # END OF runBatch()
        return status


    def getBatchFromId(self, batch_id):
        '''return the recordset with pk id=batch_id in bag form'''
        rs = self.db.table('sm.sd_process_batch').record(batch_id).output('bag')
        return rs

    def getBatchEntriesList(self, batch_id):
        '''returns the ordered list of entries for the given process_batch'''
        rs = self.db.table('sm.sd_process_entry').query(
                columns = '*',
                where = '$sd_process_batch__id = :selected_batch_id',
                order_by = 'position',
                selected_batch_id = batch_id,
                mode = 'bag'
                ).fetch()
        return rs

    def getRulesetEntriesList(self, ruleset_id):
        '''returns the ordered list of entries for the give ruleset'''
        rs = self.db.table('sm.sm_ruleset_entry').query(
                columns = '*',
                where = '$sm_ruleset__id = :selected_ruleset_id',
                order_by = 'position',
                selected_ruleset_id = ruleset_id,
                mode = 'bag'
                ).fetch()
        return rs

    def getSchemaStore(self, data_registry_id):
        '''return the record from schema registry'''
        rs = self.db.table('sm.sd_data_registry').record(data_registry_id).output('bag')
        return rs

    def getModelRowById(self, model_row_id):
        rs = self.db.table('sm.sm_model_row').record(model_row_id).output('bag')
        return rs

    def getModelColById(self, model_col_id):
        rs = self.db.table('sm.sm_model_col').record(model_col_id).output('bag')
        return rs

    def applySingleRule(self, operation = None, 
            srcBag = None, sr = None, sc = None,
            dstBag = None, dr = None, dc = None):
        if operation == '0':
            # set value
            dstBag[dr][dc] = srcBag[sr][sc]
        elif operation == '1':
            # sum
            dstBag[dr][dc] = dstBag[dr][dc] + srcBag[sr][sc]
        elif operation == '2':
            # subtraction
            dstBag[dr][dc] = dstBag[dr][dc] - srcBag[sr][sc]
        else:
            pass

    def updateDataRegistryStoreBag(self, registry_id, storeBag):
        # update the storeBag
        with self.db.table('sm.sd_data_registry').recordToUpdate(registry_id) as record:
                record['storebag'] = storeBag
                record['status'] = 'PROCESSED'
        self.db.commit()
        return record

    def logDestSchemaProcessing(self, batch, rs_ruleset, 
                                src_recordset, dst_recordset, 
                                source_storebag, previous_storebag,
                                **kwargs):
        record = self.newrecord()
        record['sd_data_registry__id'] = dst_recordset['id']
        record['date_elab'] = datetime.datetime.now()
        record['ruleset'] = 'todo'
        record['schema_source'] = src_recordset['code']
        record['current_user'] = 'unused'
        record['notes'] = 'process batch: ' + batch['code']
        record['source_storebag'] = source_storebag
        record['previous_storebag'] = previous_storebag
        self.db.table('sm.sd_data_registry_log').insert(record)
        self.db.commit()
        return