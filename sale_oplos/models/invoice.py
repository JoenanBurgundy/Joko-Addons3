from datetime import date
from datetime import datetime
# from datetime import timedelta
# from dateutil import relativedelta
# import time

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
# from odoo import http
from openerp.exceptions import UserError
# from openerp.tools.safe_eval import safe_eval as eval
# from openerp.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
