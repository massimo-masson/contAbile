#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu schema
    schema = contAbile.branch('!![it]Gestione')
    schema.thpage('!![it]Schemi', table='sm.sd_data_registry')
    schema.thpage('!![it]Elaborazioni', table='sm.sd_process_batch')

    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')

    # menu modelli
    #config_model = config.branch('!![it]Modelli')
    config.thpage('!![it]Categorie',table='sm.sm_category')
    config.thpage('!![it]Modelli', table='sm.sm_model')
    config.thpage('!![it]Regole elaborazione', table='sm.sm_ruleset')
    #config.thpage('!![it]Ruleset entry', table='sm.sm_ruleset_entry')
    config.thpage('!![it]Tipi riga',table='sm.sm_row_type')

    # menu utilities
    utilities = contAbile.branch('!![it]Utilities')
    utilities_impexp = utilities.branch('!![it]Import/export')
