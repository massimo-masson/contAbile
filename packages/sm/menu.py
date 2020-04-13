#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch(u'contAbile')

    # menu configurazione
    config = contAbile.branch(u'!![it]Configurazione')

    # menu configurazione -> schemi
    sm_config = config.branch(u'!![it]Gestione Schemi')
    sm_config.thpage(u'!![it]Classificazione schemi',table='sm.sm_classe')
    sm_config.thpage(u'!![it]Anagrafiche schemi', table='sm.sm_anagrafica')
    #sm_config.thpage(u'!![it]--Righe schema', table='sm.sm_anagrow')
    #sm_config.thpage(u'!![it]--Colonne schema', table='sm.sm_anagcol')
    #sm_config.lookups(u'!![it]Tabelle lookup', lookup_manager='sm')
