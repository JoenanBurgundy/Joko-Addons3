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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
#     oplos = fields.Boolean(string='Oplos', readonly=True, states={'draft': [('readonly', False)]})
    oplos_product_id = fields.Many2one('product.product', string='Oplos Code')
    
    @api.onchange('product_id')
    def _onchange_product_id_oplos(self):
        if not self.product_id:
            self.oplos_product_id = False
            return {'domain': {'oplos_product_id': [False]}}
        return {
            'domain': {
                'oplos_product_id': [('id', 'in', [product.id for product in [oplos.oplos_product_id for oplos in self.product_id.oplos_ids]])]
        }}

    @api.onchange('oplos_product_id')
    def _onchange_oplos_product_id(self):
        if self.oplos_product_id:
            self.name = self.product_id.oplos_ids.filtered(lambda r: r.oplos_product_id == self.oplos_product_id)[0].oplos_desc
        return {}
        
#     @api.multi
#     def _prepare_order_line_procurement(self, group_id=False):
#         self.ensure_one()
#         res = super(SaleOrderLine, self)._prepare_order_line_procurement(group_id)
#         res['product_id'] = self.product_id.oplos_code.id if self.oplos and self.product_id.oplos_code \
#             else self.product_id.id
#         return res
#     
