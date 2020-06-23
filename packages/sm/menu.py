#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# contAbile:sm (schema manager), an automated processor for data based on
# models and flexible processing logic built by users.
# Copyright (C) 2020 Massimo Masson
# 
# This program is dual-licensed.
# 
# Option 1:
# If you respect the terms of GNU GPL license, AND
# you agree to give the copyright for modifications or derivative work
# to the original author Massimo Masson, the GPL license applies.
# In this case:
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# Option 2:
# If you do not agree with any of the statements in option 1, then
# a proprietary license applies. In this case, contact the author
# for a dedicated propietary license.
# 

def config(root,application=None):
    contAbile = root.branch('contAbile')

    # menu schema
    schema = contAbile.branch('!![it]Gestione')

    schema.thpage('!![it]Schemi', table = 'sm.sd_data_registry')
    schema.thpage('!![it]Elaborazioni', table = 'sm.sd_process_batch')

    #schema.thpage('!![it]Parametri globali', table='sm.sd_parameter_global')
    # menu schema parameters
    schema_parameters = schema.branch('!![it]Parametri')
    schema_parameters.thpage('!![it]Parametri globali', table = 'sm.sd_parameter_global')
    schema_parameters.thpage('!![it](Parametri categorie)', table = 'sm.sd_parameter_category')
    schema_parameters.thpage('!![it](Parametri modelli)', table = 'sm.sd_parameter_model')
    schema_parameters.thpage('!![it](Parametri schemi)', table = 'sm.sd_parameter_schema')

    # menu schema import
    schema_import = schema.branch('!![it]Importazioni')
    schema_import.thpage('!![it]Da bilancio di verifica', table = 'sm.si_bilver_01_lot')
    
    # # menu schema import bilver
    # schema_import_bilver01 = schema_import.branch('!![it]Da Bilancio di verifica')

    # schema_import_bilver01.thpage('!![it]Lotti importazione', 
    #                 table='sm.si_bilver_01_lot')
    # schema_import_bilver01.thpage('!![it]Righe lotti', 
    #                 table='sm.si_bilver_01_lot_row')


    # menu configurazione
    config = contAbile.branch('!![it]Configurazione')

    # menu modelli
    #config_model = config.branch('!![it]Modelli')
    config.thpage('!![it]Categorie',table = 'sm.sm_category')
    config.thpage('!![it]Modelli', table = 'sm.sm_model')
    config.thpage('!![it]Regole elaborazione', table = 'sm.sm_ruleset')
    #config.thpage('!![it]Ruleset entry', table='sm.sm_ruleset_entry')
    #config.thpage('!![it]Tipi riga',table='sm.sm_row_type')
    config.thpage('!![it]Classificazione parametri', table = 'sm.sm_parameter_class')

    # menu importazioni
    config_import = config.branch('!![it]Importazioni')
    
    config_import.thpage('!![it]Collegamenti bilancio di verifica', \
                        table='sm.si_bilver_01_model')

    # menu utilities
    utilities = contAbile.branch('!![it]Utilities')

    utilities.thpage('!![it]Modifica manuale dati schema', 
            table = 'sm.sd_data_registry',
            #viewResoruce = '',
            formResource = 'FormEditable')

    # utilities - raw tables
    utilities_rawtabs = utilities.branch('!![it]Tabelle')
    utilities_rawtabs.thpage('!![it]Modelli - righe', table = 'sm.sm_model_row')
    utilities_rawtabs.thpage('!![it]Modelli - colonne', table = 'sm.sm_model_col')
