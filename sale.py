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

    @fields.depends('shop', 'party')
    def on_change_party(self):
        res = super(Sale, self).on_change_party()
        pool = Pool()
        ListAdvanced = pool.get('sale.list_advanced')
        total_advanced = Decimal(0.0)
        
        all_list_advanced = ListAdvanced.search([('party', '=', self.party)])
        if all_list_advanced:
            for list_advanced in all_list_advanced:
                for line in list_advanced.lines:
                    total_advanced += line.balance

        res['advanced'] = total_advanced

        if self.shop:
            if not res.get('price_list') and res.get('invoice_address'):
                res['price_list'] = self.shop.price_list.id
                res['price_list.rec_name'] = self.shop.price_list.rec_name
            if not res.get('payment_term') and res.get('invoice_address'):
                res['payment_term'] = self.shop.payment_term.id
                res['payment_term.rec_name'] = self.shop.payment_term.rec_name
        return res

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
        ListAdvanced = pool.get('sale.list_advanced')
        sales = cls.browse(sales)
        total_advanced = Decimal(0.0)
        for sale in sales:
            total_advanced = Decimal(0.0)
            all_list_advanced = ListAdvanced.search([('party', '=', sale.party)])
            if all_list_advanced:
                for list_advanced in all_list_advanced:
                    for line in list_advanced.lines:
                        total_advanced += line.balance

            advanced[sale.id] = total_advanced
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
