#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, model parameter
        
        A model parameter can be accessed from the schema elaboration
        if the schema belongs to that model.
        '''
        tbl = pkg.table('sd_parameter_model', pkey = 'id',
                name_long = '!![it]Parametro di modello',
                name_plural='!![it]Parametri di modello',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22', 
                name_long = '!![it]Codice parametro di modello',
                unique = True, validate_notnull = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione parametro di modello')

        tbl.column('value', dtype = 'N',
                name_long = '!![it]Valore', name_short = '!![it]Val')        

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype = 'A', size = '22',
                name_long = '!![it]Classe')
        fk.relation('sm.sm_parameter_class.id', mode = 'foreignkey',
                relation_name = 'class_model_parameters', onDelete = 'raise')

        # foreign key to the referenced model
        fk = tbl.column('sm_model__id', dtype = 'A', size = '22',
                name_long = '!![it]Rif. modello')
        fk.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'model_parameters', onDelete = 'raise')
