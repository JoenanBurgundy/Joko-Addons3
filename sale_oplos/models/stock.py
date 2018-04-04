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


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    oplos_product_id = fields.Many2one('product.product', string='Oplos Code')
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
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
    
    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals['customer_po_ref'] = self.customer_po_ref
        return vals