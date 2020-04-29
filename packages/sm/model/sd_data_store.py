#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# ATTUALMENTE NON USATA
#

""" class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, store for data Bags'''
        tbl = pkg.table('sd_data_storebag', pkey='id', 
                name_long='!![it]Dati schema')
                #caption_field='id')

        self.sysFields(tbl)

        tbl_data=tbl.column('data', dtype='X', 
                name_long='!![it]Schema')
        
        # foreign key to data_registry
        #tbl_sd_data_registry_id=tbl.column('sd_data_registry_id', size='22',
        #        name_long='!![it]Anagrafica schema',
        #        validate_notnull=True)
        #tbl_sd_data_registry_id.relation('sm.sd_data_registry.id', mode='foreignkey',
        #        relation_name='databags',
        #        onDelete='raise')
         """