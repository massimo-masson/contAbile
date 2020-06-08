#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, category parameter
        
        A category parameter can be accessed from a schema elaboration
        if the schema's model belongs to that category
        '''
        tbl = pkg.table('sd_parameter_category', pkey = 'id',
                name_long = '!![it]Parametro di categoria',
                name_plural='!![it]Parametri di categoria',
                caption_field = 'code')

        self.sysFields(tbl)

        tbl.column('code', dtype = 'A', size = ':22', 
                name_long = '!![it]Codice parametro di categoria',
                unique = True, validate_notnull = True)

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione parametro di categoria')

        tbl.column('value', dtype = 'N',
                name_long = '!![it]Valore', name_short = '!![it]Val')

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype = 'A', size = '22',
                name_long = '!![it]Classe')
        fk.relation('sm.sm_parameter_class.id', mode = 'foreignkey',
                relation_name = 'class_category_parameters', onDelete = 'raise')

        # foreign key to the referenced category
        fk = tbl.column('sm_category__id', dtype = 'A', size = '22',
                name_long = '!![it]Rif. categoria')
        fk.relation('sm.sm_category.id', mode = 'foreignkey',
                relation_name = 'category_parameters', onDelete = 'raise')
