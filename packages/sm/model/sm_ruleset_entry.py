#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gnr.core.gnrbag import Bag

class Table(object):
        def config_db(self, pkg):
                '''sm: single transofmration rule for ruleset'''
                tbl = pkg.table('sm_ruleset_entry', pkey='id', 
                        name_long='!![it]Trasformazione cella modello',
                        name_plural='!![it]Trasformazione celle modello',
                        caption_field='code_description')

                self.sysFields(tbl)

                tbl_code=tbl.column('code', dtype='A', size=':22',
                        unmodifiable=True,      # can set code only on new record
                        name_long='!![it]Regola trasformazione cella',
                        unique=True, validate_notnull=True, indexed=True)
                
                tbl_description=tbl.column('description', dtype='A', size=':256', 
                        name_long='!![it]Descrizione')

                tbl_code_description=tbl.formulaColumn('code_description', 
                        '"("||$code||") - "||$description', name_long='!![it]Regole')

                # ruleset reference entry
                tbl_sm_ruleset__id=tbl.column('sm_ruleset__id', size='22',
                        unmodifiable=True,
                        name_long='!![it]Ruleset',
                        validate_notnull=True
                        )
                tbl_sm_ruleset__id.relation('sm.sm_ruleset.id', mode='foreignkey',
                        relation_name='ruleset_entries',
                        onDelete='raise'
                        )

                # source row
                tbl_src_sm_model_row__id=tbl.column('src_sm_model_row__id', size='22',
                        name_long='!![it]Riga sorgente',
                        validate_notnull=True
                        )
                tbl_src_sm_model_row__id.relation('sm.sm_model_row.id', mode='foreignkey',
                        relation_name='ruleset_rows_src',
                        onDelete='raise'
                        )
                # and it's reference id model
                tbl.aliasColumn('src_sm_model__id', name_long='!![it]src_sm_model__id',
                        relation_path='@src_sm_model_row__id.@sm_model__id.id')

                # source col
                tbl_src_sm_model_col__id=tbl.column('src_sm_model_col__id', size='22',
                        name_long='!![it]Colonna sorgente',
                        validate_notnull=True
                        )
                tbl_src_sm_model_col__id.relation('sm.sm_model_col.id', mode='foreignkey',
                        relation_name='ruleset_cols_src',
                        onDelete='raise'
                        )

                # destination row
                tbl_dst_sm_model_row__id=tbl.column('dst_sm_model_row__id', size='22',
                        name_long='!![it]Riga destinazione',
                        validate_notnull=True
                        )
                tbl_dst_sm_model_row__id.relation('sm.sm_model_row.id', mode='foreignkey',
                        relation_name='ruleset_rows_dst',
                        onDelete='raise'
                        )
                # and it's reference id model
                tbl.aliasColumn('dst_sm_model__id', name_long='!![it]dst_sm_model__id',
                        relation_path='@dst_sm_model_row__id.@sm_model__id.id')

                # destination col
                tbl_dst_sm_model_col__id=tbl.column('dst_sm_model_col__id', size='22',
                        name_long='!![it]Colonna destinazione',
                        validate_notnull=True
                        )
                tbl_dst_sm_model_col__id.relation('sm.sm_model_col.id', mode='foreignkey',
                        relation_name='ruleset_cols_dst',
                        onDelete='raise'
                        )

                # operation set entry
                tbl_operation=tbl.column('operation', dtype='A', size=':22',
                        name_long='!![it]Operazione')
