#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, classe di appartenenza'''
        tbl = pkg.table('sm_classe', pkey='id', 
                name_long='!![it]Classe schema',
                name_plural='!![it]Classi schemi',
                caption_field='codice')

        self.sysFields(tbl)

        tbl_codice=tbl.column('codice', dtype='A', size=':15', 
                name_long='!![it]Codice classe',
                unique=True, validate_notnull=True, indexed=True)

        tbl_descrizione=tbl.column('descrizione', dtype='A', size=':64', 
                name_long='!![it]Descrizione classe', 
                validate_notnull=True)

        tbl_note=tbl.column('note', dtype='A', size=':255', 
                name_long='!![it]Note')
