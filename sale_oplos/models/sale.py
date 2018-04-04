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

# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#     
#     comp_pricelist_id = fields.Many2one('product.pricelist', string='Compare Pricelist')

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
#     oplos = fields.Boolean(string='Oplos', readonly=True, states={'draft': [('readonly', False)]})
    oplos_product_id = fields.Many2one('product.product', string='Oplos Code')
    price_unit_public = fields.Float(string='Public Price', digits=dp.get_precision('Product Price'), default=0.0)
    
    @api.multi
    def _get_public_price(self, product):
#         # TO DO: move me in master/saas-16 on sale.order
#         if self.order_id.partner_id.property_product_pricelist.discount_policy == 'with_discount':
#             return product.with_context(pricelist=self.order_id.partner_id.property_product_pricelist.id).price
#         import ipdb;ipdb.set_trace()
#         final_price, rule_id = self.order_id.partner_id.property_product_pricelist.get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
#         context_partner = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order)
#         base_price, currency_id = self.with_context(context_partner)._get_real_price_currency(self.product_id, rule_id, self.product_uom_qty, self.product_uom, self.order_id.partner_id.property_product_pricelist.id)
#         if currency_id != self.order_id.partner_id.property_product_pricelist.currency_id.id:
#             base_price = self.env['res.currency'].browse(currency_id).with_context(context_partner).compute(base_price, self.order_id.partner_id.property_product_pricelist.currency_id)
#         # negative discounts (= surcharge) are included in the display price
#         return max(base_price, final_price)
        # TO DO: move me in master/saas-16 on sale.order
        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(pricelist=self.order_id.pricelist_id.id).price
        final_price, rule_id = self.order_id.pricelist_id.get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        context_partner = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order)
        base_price, currency_id = self.with_context(context_partner)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        if currency_id != self.order_id.pricelist_id.currency_id.id:
            base_price = self.env['res.currency'].browse(currency_id).with_context(context_partner).compute(base_price, self.order_id.pricelist_id.currency_id)
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)
    
    @api.onchange('product_id')
    def _onchange_product_id_oplos(self):
        if not self.product_id:
            self.oplos_product_id = False
            return {'domain': {'oplos_product_id': [False]}}
        # set public pricelist
#         product = self.product_id
#         import ipdb;ipdb.set_trace()
#         if self.order_id.partner_id.property_product_pricelist and self.order_id.partner_id:
#             self.price_unit_public = self.env['account.tax']._fix_tax_included_price_company(self.with_context(public_pricelist=True)._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
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
