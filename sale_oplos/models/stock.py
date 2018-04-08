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
    
    oplos_id= fields.Many2one('product.oplos', string='Oplos Code', readonly=True, states={'draft': [('readonly', False)]})
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
    @api.onchange('product_id')
    def _onchange_product_id_oplos(self):
        if not self.product_id:
            self.oplos_id = False
            return {'domain': {'oplos_id': [False]}}
        return {
            'domain': {
                'oplos_id': [('product_id', '=', self.product_id.product_tmpl_id.id)]
        }}

    @api.onchange('oplos_id')
    def _onchange_oplos_id(self):
        if self.oplos_id:
            self.name = self.oplos_id.oplos_desc
        return {}
    
    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals['customer_po_ref'] = self.customer_po_ref
        return vals