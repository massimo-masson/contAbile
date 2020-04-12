#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='sm package',sqlschema='sm',sqlprefix=True,
                    name_short='Sm', name_long='Sm', name_full='Sm')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
