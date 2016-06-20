#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.model import ModelView, fields, ModelSQL, Workflow

__all__ = ['Party']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    lock_credit = fields.Boolean("Lock credit")
    rate = fields.Float("Porcentaje de incremento de credito")
    
    @classmethod
    def default_rate(cls):
        pool = Pool()
        Config = pool.get('account.configuration')
        w = Config(1).rate
        return w
        
        
    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()
