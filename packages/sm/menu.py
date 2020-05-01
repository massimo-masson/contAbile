#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu schema
    schema = contAbile.branch('!![it]Gestione')
    schema.thpage('!![it]Schemi', table='sm.sd_data_registry')

    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')

    # menu modelli
    #config_model = config.branch('!![it]Modelli')
    config.thpage('!![it]Anagrafiche Modelli', table='sm.sm_model')
    config.thpage('!![it]Regole', table='sm.sm_ruleset')
    config.thpage('!![it]Regole entry', table='sm.sm_ruleset_entry')


    config.thpage('!![it]Categorie Modelli',table='sm.sm_category')
    config.thpage('!![it]Tipi riga',table='sm.sm_row_type')
