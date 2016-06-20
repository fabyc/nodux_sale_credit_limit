# This file is part of the sale_payment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .party import *
from .sale import *
from .account import *

def register():
    Pool.register(
        Configuration,
        Party,
        Sale,
        module='nodux_sale_credit_limit', type_='model')
