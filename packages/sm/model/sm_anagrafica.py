#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, registry of entries'''
        tbl = pkg.table('sm_anagrafica', pkey='id', 
                name_long='!![it]Anagrafica schemi',
                name_plural='!![it]Anagrafiche schemi',
                caption_field='codice')

        self.sysFields(tbl)

        tbl_codice=tbl.column('codice', dtype='A', size=':15', 
                name_long='!![it]Codice schema',
                unique=True, validate_notnull=True, indexed=True)

        tbl_descrizione=tbl.column('descrizione', dtype='A', size=':64', 
                name_long='!![it]Descrizione schema', 
                validate_notnull=True)

        tbl_note=tbl.column('note', dtype='A', size=':255', 
                name_long='!![it]Note')

        # sm_class: foreign key to sm_class
        tbl_classe=tbl.column('sm_classe', dtype='A', size=':15',
                name_long='!![it]Classe schema',
                validate_notnull=True)
        tbl_classe.relation('sm.sm_classe.codice', mode='foreignkey',
                relation_name='schemi',
                onDelete='raise')
