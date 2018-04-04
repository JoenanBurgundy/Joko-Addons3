from datetime import date
from datetime import datetime
# from datetime import timedelta
# from dateutil import relativedelta
# import time

from odoo import models, fields, api, _
# from odoo import http
from openerp.exceptions import UserError
import odoo.addons.decimal_precision as dp
# from openerp.tools.safe_eval import safe_eval as eval
# from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    oplos_ids = fields.One2many('product.oplos', 'product_id', string='Oplos Code')
#     oplos_desc = fields.Char(string='Oplos Description')
#     oplos_sale_price = fields.Float(string='Oplos Sale Price', digits=dp.get_precision('Product Price'))


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.multi
    def name_get(self):
#         if self._context.get('code_only'):
        result = []
        for product in self:
            result.append((product.id, "%s" % (product.default_code or product.name)))
        return result
#         else:
#             return super(ProductProduct, self).name_get()

class ProductOplos(models.Model):
    _name = 'product.oplos'

    product_id = fields.Many2one('product.product', string='Product')
    oplos_product_id = fields.Many2one('product.product', string='Oplos Code', required=True)
    oplos_desc = fields.Char(string='Oplos Description', required=True)
    
    @api.onchange('oplos_product_id')
    def _onchange_oplos_product_id(self):
        self.oplos_desc = self.oplos_product_id.name if self.oplos_product_id else False
        return
        