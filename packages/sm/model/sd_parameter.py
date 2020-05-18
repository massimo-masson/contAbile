#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sd: schema data, parameter'''
        tbl = pkg.table('sd_parameter', pkey='id',
                name_long='!![it]Parametro',
                name_plural='!![it]Parametri',
                caption_field='code')

        self.sysFields(tbl)

        tbl.column('code', dtype='A', size=':22', 
                name_long='!![it]Codice parametro',
                unique=True, validate_notnull=True)

        tbl.column('description', dtype='A', size=':256', 
                name_long='!![it]Descrizione parametro')

        # tbl.column('notes', dtype='A', size=':1024', 
        #         name_long='!![it]Note')

        #
        # type could be
        #   0:  general
        #   1:  model parameter
        #   2:  schema parameter
        #
        tbl.column('type', dtype='A', size=':22', name_long='!![it]Tipo parametro')

        # foreign key to the parameter's class
        fk = tbl.column('sm_parameter_class__id', dtype='A', size='22',
                name_long='!![it]Classe')
        fk.relation('sm.sm_parameter_class.id', mode='foreignkey',
                relation_name='class_parameters', onDelete='raise')

        # foreign key to the referenced model
        fk = tbl.column('sm_model__id', dtype='A', size='22',
                name_long='!![it]Rif. modello')
        fk.relation('sm.sm_model.id', mode='foreignkey',
                relation_name='models_parameters', onDelete='raise')

        # foreign key to the referenced schema
        fk = tbl.column('sd_data_registry__id', dtype='A', size='22',
                name_long='!![it]Rif. schema')
        fk.relation('sm.sd_data_registry.id', mode='foreignkey',
                relation_name='schema_parameters', onDelete='raise')

        tbl.column('status', dtype='A', size=':22', name_long='!![it]Status parametro')

        tbl.column('value', dtype='N', name_long='!![it]Valore', name_short='!![it]Val.')