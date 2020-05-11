#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu schema
    schema = contAbile.branch('!![it]Gestione')

    schema.thpage('!![it]Schemi', table='sm.sd_data_registry')
    schema.thpage('!![it]Elaborazioni', table='sm.sd_process_batch')
    
    # menu schema import
    schema_import = schema.branch('!![it]Importazioni')
    
    schema_import.thpage('!![it]Bilanci di verifica 01', table='sm.si_bilver_01_lot')
    schema_import.thpage('!![it]Righe bilanci di verifica 01', table='sm.si_bilver_01_lot_row')


    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')

    # menu modelli
    #config_model = config.branch('!![it]Modelli')
    config.thpage('!![it]Categorie',table='sm.sm_category')
    config.thpage('!![it]Modelli', table='sm.sm_model')
    config.thpage('!![it]Regole elaborazione', table='sm.sm_ruleset')
    #config.thpage('!![it]Ruleset entry', table='sm.sm_ruleset_entry')
    config.thpage('!![it]Tipi riga',table='sm.sm_row_type')

    # menu importazioni
    config_import = config.branch('!![it]Importazioni')
    
    config_import.thpage('!![it]Collegamenti bilver_01',table='sm.si_bilver_01_model')

    # menu utilities
    #utilities = contAbile.branch('!![it]Utilities')
    #utilities_impexp = utilities.branch('!![it]Import/export')
