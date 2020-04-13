#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, riga di anagrafica'''
        tbl = pkg.table('sm_anagrow', pkey='id', 
                name_long='!![it]Riga schema',
                name_plural='!![it]Righe schema',
                caption_field='codice')

        self.sysFields(tbl)

        tbl_codice=tbl.column('codice', dtype='A', size=':15', 
                name_long='!![it]Riga schema',
                unique=True, validate_notnull=True, indexed=True)

        tbl_descrizione=tbl.column('descrizione', dtype='A', size=':64', 
                name_long='!![it]Descrizione riga', 
                validate_notnull=True)

        tbl_posizione=tbl.column('posizione', dtype='N', 
                name_long='!![it]posizione riga')

        tbl_note=tbl.column('note', dtype='A', size=':255', 
                name_long='!![it]Note')

        # sm_anagrafica: foreign key to sm_anagrafica
        tbl_sm_anagrafica=tbl.column('sm_anagrafica', dtype='A', size=':15',
                name_long='!![it]Anagrafica schema',
                validate_notnull=True)
        tbl_sm_anagrafica.relation('sm.sm_anagrafica.codice', mode='foreignkey',
                relation_name='righe',
                onDelete='raise')
