# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo import models, fields, api, _


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    
    customer_po_ref = fields.Char(string='Customer PO Ref')
    
class ProcurementOrder(models.Model):
    _inherit = "procurement.order"
    
    customer_po_ref = fields.Char(string='Customer PO Ref')
    oplos_id= fields.Many2one('product.oplos', string='Oplos Code')
    
    def _get_stock_move_values(self):
        vals = super(ProcurementOrder, self)._get_stock_move_values()
        vals['customer_po_ref'] = self.customer_po_ref
        vals['oplos_id'] = self.oplos_id.id
        return vals
