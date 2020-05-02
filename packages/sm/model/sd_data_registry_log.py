#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
        def config_db(self, pkg):
                '''sd: schema data, log for data registry'''
                tbl = pkg.table('sd_data_registry_log', pkey='id', 
                        name_long='!![it]Log operazioni',
                        caption_field='date_elab')

                self.sysFields(tbl)

                tbl_sd_data_registry__id=tbl.column('sd_data_registry__id',size='22', 
                        group='_', name_long='!![it]Schema')
                tbl_sd_data_registry__id.relation('sd_data_registry.id', 
                        relation_name='data_registry_log', 
                        mode='foreignkey', onDelete='raise')

                tbl_date_elab = tbl.column('date_elab', dtype='D', 
                        name_long='!![it]Data elaborazione', name_short='!![it]Data')

                tbl_notes=tbl.column('notes', dtype='A', size=':1024', 
                        name_long='!![it]Note')

                tbl_current_user=tbl.column('current_user', size=':22', 
                        name_long='!![it]Utente')

                tbl_ruleset=tbl.column('ruleset', size=':22', 
                        name_long='!![it]Set regole')

                tbl_schema_source=tbl.column('schema_source', size=':22', 
                        name_long='!![it]Schema origine')
