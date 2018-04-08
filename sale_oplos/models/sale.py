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
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'
     
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
    def _prepare_procurement_group(self):
        res = super(SaleOrder, self)._prepare_procurement_group()
        res.update({'customer_po_ref': self.customer_po_ref})
        return res
    
    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['customer_po_ref'] = self.customer_po_ref
        return invoice_vals

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    oplos_id= fields.Many2one('product.oplos', string='Oplos Code', readonly=True, states={'draft': [('readonly', False)]})
#     oplos_product_id = fields.Many2one('product.product', string='Oplos Code')
    price_unit_public = fields.Float(string='Public Price', digits=dp.get_precision('Product Price'),
        related='product_id.list_price', readonly=True)
    
    @api.onchange('product_id')
    def _onchange_product_id_oplos(self):
        self.oplos_id = False
        if not self.product_id:
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
        
    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_order_line_procurement(group_id)
        res['customer_po_ref'] = self.order_id.customer_po_ref
        res['oplos_id'] = self.oplos_id.id
        return res
#     
