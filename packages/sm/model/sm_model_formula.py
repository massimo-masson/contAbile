#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Table(object):
    def config_db(self, pkg):
        '''sm: schema management, model formula'''
        tbl = pkg.table('sm_model_formula', pkey = 'id', 
                name_long = '!![it]Formula cella',
                name_plural = '!![it]Formule modello',
                caption_field = 'caption')

        self.sysFields(tbl)

        # foreign key to model
        fk_row = tbl.column('sm_model__id', dtype = 'A', size = '22',
                name_long = '!![it]Modello',
                validate_notnull = True)
        fk_row.relation('sm.sm_model.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'raise')

        # foreign key to schema row
        fk_row = tbl.column('sm_model_row__id', dtype = 'A', size = '22',
                name_long = '!![it]Riga modello',
                validate_notnull = True)
        fk_row.relation('sm.sm_model_row.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'cascade')

        # foreign key to schema column
        fk_col = tbl.column('sm_model_col__id', dtype = 'A', size = '22',
                name_long = '!![it]Colonna modello',
                validate_notnull = True)
        fk_col.relation('sm.sm_model_col.id', mode = 'foreignkey',
                relation_name = 'model_formula',
                onDelete = 'cascade')

        tbl.column('description', dtype = 'A', size = ':256', 
                name_long = '!![it]Descrizione formula')

        tbl.column('formula', dtype = 'A', size = ':2048', 
                name_long = '!![it]Formula', 
                validate_notnull = True)

        tbl.formulaColumn('caption', '@sm_model_row__id.code||","||@sm_model_col__id.code',
                name_long = '!![it]Cella di riferimento')

    def modelFormulaToBagFormula(self, model_formula, path_modifier=''):
        '''Translate the model's formula style to Bag formula components

        model formula: use [Rx.Cx] to refer a cell in the schema
                       where Rx is the row, and Cx is the column, dot separated.
                       Parameter starts with [ and ends with ]
        
        path_modifier: if given a path_modifier, it is pre-fixed to the cell reference.
                       Use the '../' modifier to reach cells in the upper level 
                       of the schema.

        returns:    a dictionary with 3 items
                    result['formula'] is the modified formula to pass to bagFormula
                    result['parameters'] are the parameters for the defineFormula (a list)
                    result['values'] are the parameters for the defineSymbol (a list)
        '''
        formula = model_formula
        result = dict()
        params = list()
        values = list()
        pn = 0 
        i = 0

        while i >= 0:
            pos_start = formula.find('[', i)
            pos_end = pos_start + 1
            if pos_start >= 0:
                pos_end = formula.find(']', i + 1)
                replacement = formula[pos_start:pos_end + 1]
                value = path_modifier + formula[pos_start + 1:pos_end]
                pn += 1
                parameter = f'p{pn}'
                params.append(parameter)
                values.append(value)        
                formula = formula.replace(replacement, '$' + parameter, 1)
                i = 0
            else:
                i = pos_start
        result['formula'] = formula
        result['parameters'] = params
        result['values'] = values
        return result
