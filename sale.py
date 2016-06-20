#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.wizard import Wizard
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from decimal import Decimal
__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'
    
    lock_credit = fields.Boolean("Lock credit")
    
    advanced = fields.Function(fields.Numeric('Advanced',
            digits=(16, Eval('currency_digits', 2)),
            depends=['currency_digits']), 'get_advanced')
            
    credit_limit = fields.Function(fields.Numeric('Credit limit',
            digits=(16, Eval('currency_digits', 2)),
            depends=['currency_digits']), 'get_credit_limit')
            
    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._buttons.update({
                'wizard_add_term': {
                    'invisible': Eval('lock_credit', True),
                },
                })
                
        cls.payment_term.states['readonly'] |= Eval('lock_credit', True)

    @classmethod
    def default_lock_credit(cls):
        pool = Pool()
        Config = pool.get('party.party')
        w = Config(1).lock_credit
        return w
        
    @classmethod
    def get_advanced(cls, sales, names):
        pool = Pool()
        advanced={}
        credit = Decimal(0.0)
        debit = Decimal(0.0)
        MoveLine = pool.get('account.move.line')
        sales = cls.browse(sales)
        
        for sale in sales:
            party = sale.party.credit_amount
            advanced[sale.id] = party
        result = {
            'advanced': advanced,
            }
        return result
        
    @classmethod
    def get_credit_limit(cls, sales, names):
        pool = Pool()
        credit = Decimal(0.0)
        debit = Decimal(0.0)
        MoveLine = pool.get('account.move.line')
        sales = cls.browse(sales)
        credit_limit = {}
        
        for sale in sales:
            party = sale.party.credit_limit_amount 
            credit_limit[sale.id] = party
        
        result = {
            'credit_limit': credit_limit,
            }
        return result  
