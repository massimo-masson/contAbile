#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, schema parameter
        
        A schema parameter can be accessed from the single schema elaboration.
        '''
        tbl = pkg.table('sd_parameter_schema', pkey = 'id',
                name_long = '!![it]Parametro di schema',
                name_plural='!![it]Parametri di schema',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22', 
                name_long = '!![it]Codice parametro di schema',
                unique = True, validate_notnull = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione parametro di schema')

        tbl.column('value', dtype = 'N',
                name_long = '!![it]Valore', name_short = '!![it]Val')        

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype = 'A', size = '22',
                name_long = '!![it]Classe')
        fk.relation('sm.sm_parameter_class.id', mode = 'foreignkey',
                relation_name = 'class_schema_parameters', onDelete = 'raise')

        # foreign key to the referenced schema
        fk = tbl.column('sd_data_registry__id', dtype = 'A', size = '22',
                name_long = '!![it]Rif. schema')
        fk.relation('sm.sd_data_registry.id', mode = 'foreignkey',
                relation_name = 'schema_parameters', onDelete = 'raise')
