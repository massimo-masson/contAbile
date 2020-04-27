#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu modelli
    models = contAbile.branch('!![it]Modelli')
    models.thpage('!![it]Anagrafiche Modelli', table='sm.sm_model')

    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')
    config.thpage('!![it]Categorie Modelli',table='sm.sm_category')
    config.thpage('!![it]Tipi riga',table='sm.sm_row_type')
