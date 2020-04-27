#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, categories'''
        tbl = pkg.table('sm_category', pkey='id', 
                name_long='!![it]Categoria modello',
                name_plural='!![it]Categorie modello',
                caption_field='code')

        self.sysFields(tbl)

        tbl_codice=tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice categoria',
                unique=True, validate_notnull=True, indexed=True)

        tbl_descrizione=tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione categoria', 
                validate_notnull=True)

        tbl_note=tbl.column('notes', dtype='A', size=':1024', 
                name_long='!![it]Note')
