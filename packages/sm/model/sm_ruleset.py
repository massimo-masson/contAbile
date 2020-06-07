#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self, pkg):
        '''sm: set of schema/model transofmration rules'''
        tbl = pkg.table('sm_ruleset', pkey = 'id', 
                name_long = '!![it]Regola di trasformazione',
                name_plural = '!![it]Regole di trasformazione',
                caption_field = 'code_description')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22',
                name_long = '!![it]Codice set di regole',
                unmodifiable = True,      # can set code only on new record
                unique = True,
                validate_notnull = True,
                indexed = True)
        
        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione')

        tbl.column('notes', dtype = 'A', size = ':1024', 
                name_long = '!![it]Note')

        tbl.column('initialize_destination', dtype = 'B', 
                name_long = '!![it]Inizializza destinazione', 
                name_short = '!![it]Inizializza',
                default = True
                )
                
        # source model reference
        tbl_src_sm_model__id = tbl.column('src_sm_model__id', size = '22',
                unmodifiable = True,
                name_long = '!![it]Modello sorgente',
                validate_notnull = True
                )
        tbl_src_sm_model__id.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'ruleset_src',
                onDelete = 'raise'
                )

        # destination model reference
        tbl_dst_sm_model__id = tbl.column('dst_sm_model__id', size = '22',
                unmodifiable = True,
                name_long = '!![it]Modello destinazione',
                validate_notnull = True
                )
        tbl_dst_sm_model__id.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'ruleset_dst',
                onDelete = 'raise'
                )

        # virtual columns
        tbl.formulaColumn('code_description', 
                '"("||$code||") - "||$description', name_long = '!![it]Regole')
