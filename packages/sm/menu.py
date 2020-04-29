#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu modelli
    models = contAbile.branch('!![it]Modelli')
    models.thpage('!![it]Anagrafiche Modelli', table='sm.sm_model')

    # menu schema
    schema = contAbile.branch('!![it]Schemi')
    schema.thpage('!![it]Gestione Schemi', table='sm.sd_data_registry')

    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')
    config.thpage('!![it]Categorie Modelli',table='sm.sm_category')
    config.thpage('!![it]Tipi riga',table='sm.sm_row_type')
