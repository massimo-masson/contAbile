#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrbag import Bag
from simpleeval import simple_eval

class Table(object):
    def config_db(self, pkg):
        '''sm: single transofmration rule for ruleset'''
        tbl = pkg.table('sm_ruleset_entry', pkey = 'id',
                name_long = '!![it]Trasformazione cella modello',
                name_plural = '!![it]Trasformazione celle modello',
                caption_field = 'position_description')

        self.sysFields(tbl)

        tbl.column('position', dtype = 'N',
                name_long = '!![it]Posizione',
                name_short = '!![it]Pos')

        tbl.column('description', dtype = 'A', size = ':256',
                name_long = '!![it]Descrizione')

        # ruleset reference entry
        tbl_sm_ruleset__id=tbl.column('sm_ruleset__id', size = '22',
                unmodifiable = True,
                name_long = '!![it]Ruleset',
                validate_notnull = True
                )
        tbl_sm_ruleset__id.relation('sm.sm_ruleset.id', mode = 'foreignkey',
                relation_name = 'ruleset_entries',
                onDelete = 'raise'
                )

        # source row
        tbl_src_sm_model_row__id = tbl.column('src_sm_model_row__id', size = '22',
                name_long = '!![it]Riga sorgente',
                validate_notnull = True
                )
        tbl_src_sm_model_row__id.relation('sm.sm_model_row.id', mode = 'foreignkey',
                relation_name = 'ruleset_rows_src',
                onDelete = 'raise'
                )
        # and it's reference id model
        # tbl.aliasColumn('src_sm_model__id', name_long='!![it]src_sm_model__id',
        #         relation_path='@src_sm_model_row__id.@sm_model__id.id')

        # source col
        tbl_src_sm_model_col__id = tbl.column('src_sm_model_col__id', size = '22',
                name_long = '!![it]Colonna sorgente',
                validate_notnull = True
                )
        tbl_src_sm_model_col__id.relation('sm.sm_model_col.id', mode = 'foreignkey',
                relation_name = 'ruleset_cols_src',
                onDelete = 'raise'
                )

        # destination row
        tbl_dst_sm_model_row__id = tbl.column('dst_sm_model_row__id', size = '22',
                name_long = '!![it]Riga destinazione',
                validate_notnull = True
                )
        tbl_dst_sm_model_row__id.relation('sm.sm_model_row.id', mode = 'foreignkey',
                relation_name = 'ruleset_rows_dst',
                onDelete = 'raise'
                )
        # and it's reference id model
        # tbl.aliasColumn('dst_sm_model__id', name_long='!![it]dst_sm_model__id',
        #         relation_path='@dst_sm_model_row__id.@sm_model__id.id')

        # destination col
        tbl_dst_sm_model_col__id = tbl.column('dst_sm_model_col__id', size = '22',
                name_long = '!![it]Colonna destinazione',
                validate_notnull = True
                )
        tbl_dst_sm_model_col__id.relation('sm.sm_model_col.id', mode = 'foreignkey',
                relation_name = 'ruleset_cols_dst',
                onDelete = 'raise'
                )

        # recalc destination before apply
        # this could be useful in case the rule entry needs a calculated value
        # that needs to be updated with the previous values
        tbl.column('recalculate_before', dtype = 'B',
                default = False,
                name_long = '!![it]Ricalcola prima di applicare la regola',
                name_short = '!![it]Ricalcola')

        # operation set entry
        tbl.column('operation', dtype = 'A', size = ':22',
                name_long = '!![it]Operazione')

        # formula, used if operation equals to f
        tbl.column('formula', dtype = 'A', size = ':4096', 
                name_long = '!![it]Formula', name_short = '!![it]fn')

        # virtual columns
        tbl.formulaColumn('code_description',
                '"("||$position||") - "||$description',
                name_long = '!![it]Regole')

    def CONST_operation(self):
        '''Return the constant values for the "operation" field.
            In reference to the value of the destination cell:
                100: set value to 0
                110: set value equal to source_value
                120: set value equal to -source_value (source_value * -1)
                130: sum value to the existing
                140: subtract value from the existing
                f: formula
                p: python code
        '''
        CONST = '100:=0,110:=(+),120:=(-),130:+,140:-,f:formula,py:python'
        return CONST

    def parseFormula(self, formula, 
                    src_schema_id, src_bag, src_row, src_col, \
                    dst_schema_id, dst_bag, dst_row, dst_col):
        '''Parse the formula. Schema is mandatory, needed to dig parameters.

        src_schema_id, src_bag, src_row, src_col needed to get source values
        dst_schema_id, dst_bag, dst_row, dst_col needed to get destination values

        Formula parse works the following way:
        parse the result with simpleeval module, so normal operators are used.

        Parameters are replaced with values
        Parameters begin with [ and end with ]
        Special characters are used to identify parameter's meaning:
        $ refers to source context
        @ refers to destination context

        [$] the source schema row and column, as given in the ruleset
        [$Rx.Cy] source schema, row Rx and column Cy

        [@] the destination schema row and column, as given in the ruleset
        [@Rx.Cy] destination schema, row Rx and column Cy

        [#G#name] global parameter, code "name"

        [#C$name] category parameter, code "name", from source schema
        [#M$name] model parameter, code "name", from source schema
        [#S$name] schema parameter, code "name", from source schema

        [#C@name] category parameter, code "name", from destination schema
        [#M@name] model parameter, code "name", from destination schema
        [#S@name] schema parameter, code "name", from destination schema
        '''
        parsed_formula = formula
        
        # get references, from current schema to associated model and category
        # schema
        src_schema = self.db.table('sm.sd_data_registry').record(pkey = src_schema_id).output('bag')
        dst_schema = self.db.table('sm.sd_data_registry').record(pkey = dst_schema_id).output('bag')
        # model
        src_model_id = src_schema['sm_model__id']
        dst_model_id = dst_schema['sm_model__id']
        src_model = self.db.table('sm.sm_model').record(pkey = src_model_id).output('bag')
        dst_model = self.db.table('sm.sm_model').record(pkey = dst_model_id).output('bag')
        # category
        src_category_id = src_model['sm_category__id']
        dst_category_id = dst_model['sm_category__id']
        src_category = self.db.table('sm.sm_category').record(pkey = src_category_id).output('bag')
        dst_category = self.db.table('sm.sm_category').record(pkey = dst_category_id).output('bag')

        # let's start with simple task.
        # replace source [$] and destination [@] for ruleset_entry

        # parse [$]
        src_value = src_bag[src_row][src_col]
        parsed_formula = parsed_formula.replace('[$]', str(src_value))

        # parse [@]
        src_value = src_bag[src_row][src_col]
        parsed_formula = parsed_formula.replace('[@]', str(src_value))

        # now the longest part. search for [] pattern.
        # when found, process $, @, #
        # note that, from now on, [$] and [@] are not present, so we can
        # deal with the [$...], [@...], [#...] patterns

        i = 0
        while (i >= 0):
            pos_start = parsed_formula.find('[', i)
            i = pos_start
            pos_end = pos_start + 1
            if (pos_start >= 0):
                pos_end = parsed_formula.find(']', i + 1)
                found_token = parsed_formula[pos_start:pos_end + 1]
                i = pos_end     # note: if i >= 0 we've found a formula token
            
            # now, if i >= 0 we have a token, otherwise not, and exit while
            if (i >= 0):
                # found_token has the surrounding []
                # token_content is the found token without the surrounding []
                token_content = found_token[1:-1]
                operation_set = token_content[0]

                if operation_set == '#':
                    # PARAMETERS PATTERN
                    # token_content has now the form '#XYname'
                    # X = [G|C|M|S], Y = [#|$|@]
                    # first 3 char are pattern, the remaining is the name
                    parameter_category = token_content[1].upper()
                    parameter_name = token_content[3:]
                    if parameter_category == 'G':
                        # global parameter
                        param_value = self.getParameterGlobal(parameter_name)

                    elif parameter_category == 'C':
                        # category paremeter, could be $ source or @ destination.
                        # final pattern char is in 3rd position, so index = 2
                        #print('parameter category, token_content:', token_content)
                        if token_content[2] == '$':
                            param_value = self.getParameterCategory(src_category_id, parameter_name)
                        elif token_content[2] == '@':
                            param_value = self.getParameterCategory(dst_category_id, parameter_name)
                        else:
                            # bad pattern
                            pass
                    elif parameter_category == 'M':
                        # model paremeter, could be $ source or @ destination.
                        # final pattern char is in 3rd position, so index = 2
                        if token_content[2] == '$':
                            param_value = self.getParameterModel(src_model_id, parameter_name)
                        elif token_content[2] == '@':
                            param_value = self.getParameterModel(dst_model_id, parameter_name)
                        else:
                            # bad pattern
                            pass
                    elif parameter_category == 'S':
                        # schema paremeter, could be $ source or @ destination.
                        # final pattern char is in 3rd position, so index = 2
                        if token_content[2] == '$':
                            param_value = self.getParameterSchema(src_schema_id, parameter_name)
                        elif token_content[2] == '@':
                            param_value = self.getParameterSchema(dst_schema_id, parameter_name)
                        else:
                            # bad pattern
                            pass
                    else:
                        # unknown parameter pattern
                        pass

                elif operation_set == '$':
                    # SOURCE SCHEMA PATTERN
                    # token_content is in the form: $Rx.Cy
                    reference_token = token_content[1:]
                    param_value = str(src_bag[reference_token])

                elif operation_set == '@':
                    # DESTINATION SCHEMA PATTERN
                    reference_token = token_content[1:]
                    param_value = str(dst_bag[reference_token])

                else:
                    # unknown pattern...
                    pass
                
                # here, we've found a token, and got his value in param_value
                # now replace the parameter with it's value
                #print('****replacing ', found_token, ' with ', param_value)
                parsed_formula = parsed_formula.replace(found_token, param_value)

                # string containing formula in parsing has changed, lenght probably
                # was changed too, so we must restart scanning from the beginng
                i = 0

        value = simple_eval(parsed_formula)
        return value

    def getParameterGlobal(self, parameter):
        '''Get "parameter" from global parameters'''
        value = '0'
        try:
            record = self.db.table('sm.sd_parameter_global') \
                .record(code = parameter).output('bag')
            value = str(record['value'])
        except:
            pass
        return value

    def getParameterCategory(self, category_id, parameter):
        '''Get "parameter" from category parameters'''
        value = '0'
        try:
            record = self.db.table('sm.sd_parameter_category').record(
                    sm_category__id = category_id, 
                    code = parameter).output('bag')
            value = str(record['value'])
        except:
            pass
        return value

    def getParameterModel(self, model_id, parameter):
        '''Get "parameter" from model parameters'''
        value = '0'
        try:
            record = self.db.table('sm.sd_parameter_model').record(
                    sm_model__id = model_id, 
                    code = parameter).output('bag')
            value = str(record['value'])
        except:
            pass
        return value

    def getParameterSchema(self, schema_id, parameter):
        '''Get "parameter" from schema parameters'''
        value = '0'
        try:
            record = self.db.table('sm.sd_parameter_schema').record(
                    sd_data_registry__id = schema_id, 
                    code = parameter).output('bag')
            value = str(record['value'])
        except:
            pass
        return value
