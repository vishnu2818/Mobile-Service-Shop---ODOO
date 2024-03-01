## -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api,_
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import datetime 

#mobileshop fields
class MobileServiceShop(models.Model):
    _name = 'mobile.service.shop'
    _description = 'All Types of Mobiles Service Here!!'
    _rec_name = 'customer_id'

    sequence = fields.Char(default='New', readonly=True)
    #Many2one end wid _id
    customer_id = fields.Many2one('res.partner', readonly=True, states={'draft': [('readonly', False)]}) #comodel_name='res.partner', help = "Shop Customer field"
    customer_phone = fields.Char(related='customer_id.phone', readonly=True)
    mobile_os_type = fields.Selection([('android', 'Android'), ('basic', 'Basic'), ('os', 'Os')], readonly=True, states={'draft': [('readonly', False)]})
    # Many2one Field.....
    company_id = fields.Many2one('res.company', readonly=True, states={'draft': [('readonly', False)]})
    mobile_complaint_description = fields.Text(readonly=True, states={'draft': [('readonly', False)]})
    # one@many Field......
    mobile_service_line_ids= fields.One2many('mobile.service.line','service_id',string = 'Service Product', readonly=True, states={'draft': [('readonly', False)]}) 
    # many@many Field......
    damaged_spare_parts_ids = fields.Many2many('spare.parts', readonly=True, states={'draft': [('readonly', False)]})
    total = fields.Float(string = 'Total', compute='calculate_total', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('waiting_for_approvel', 'Waiting For Approvel'), ('approve', 'Approved'), ('reject', 'Rejected'), ('done', 'Done'),('cancel', 'Cancelled')], string='State', default='draft')
    current_user = fields.Char(string = 'Current User',readonly=True)
    reason = fields.Char(string = "Reason", readonly = True)

    @api.depends('mobile_service_line_ids.subtotal')
    def calculate_total(self):
        for v in self:
            v.total = sum(s.subtotal for s in v.mobile_service_line_ids)

    def action_wfa(self):
        self.state = 'waiting_for_approvel'          #'waiting_for_approvel_clicked' : True ----- or self.write({'state': 'waiting_for_approvel'})
        if not self.mobile_service_line_ids:
            raise Warning("No product selected! Please choose a product.")
        if self.sequence == 'New':
            self.sequence = self.env['ir.sequence'].next_by_code('mobile.shop.sequence') or _('New')

    def action_confirm(self):
        self.state = 'done'
        
    def action_draft(self):
        self.state = 'draft'

    def action_approved(self):
        self.state = 'approve'

    def action_rejected(self):
        self.state = 'reject'
        return {
            'name': ('Reject Service'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'reject.wizard',
            'target': 'new',
            'context': {'active_id': self.id}
        }

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'
        # if self.state == 'cancel':  for pafter cancel to---> delete the product in the table
        #     return super(MobileServiceShop, self).unlink()

    @api.model
    def create(self, vals):
        if 'mobile_service_line_ids' in vals and not vals['mobile_service_line_ids']: #or vals.get("fieldName")
            raise Warning("No product selected! Please choose a product.")
        return super(MobileServiceShop, self).create(vals)

    @api.onchange('customer_id')
    def get_current_user(self):
        # user_id = self.env.uid
        self.current_user = self.env['res.users'].browse(self.env.uid).name
        # current_user_group = self.env['res.groups'].search([('name', '=', 'MobileShop / Manager')])
        # if 'MobileShop / User' in self.env.user.groups_id.mapped('name'):
        #     self.current_user = "MobileShop / User"


        # if self.env.user.name in current_user_group:
        #     self.current_user = self.env.user.name
        # else:
        #     self.current_user="other Group"

    # @api.model
    # def unlink(self):
    #     # for service in self:
    #     if self.state != 'draft':
    #         raise UserError("You can only delete Record in draft state.")
    #     return super(MobileService, self).unlink()

class MobileServiceLine(models.Model):
    _name = 'mobile.service.line'
    _description = 'Mobile Service Line'
    _rec_name = 'service_id'

    @api.depends('qty', 'unit_price')
    def calculate_subtotal(self):
        for l in self:
            l.subtotal = l.qty * l.unit_price

    service_id = fields.Many2one('mobile.service.shop', string='Customer Name', ondelete='cascade') # required=True

    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity', default=1)
    unit_price = fields.Float(string='UnitPrice')#related = 'product_id.lst_price'
    subtotal = fields.Float( string='SubTotal', compute='calculate_subtotal')


    @api.constrains('product_id')
    def _check_product_selection(self):
        for record in self:
            if not record.product_id:
                raise Warning("No product selected! Please choose a product.")

    # @api.onchange('product_id')
    # def onchange_price(self):
    #     if self.product_id:
    #         self.unit_price = self.product_id.lst_price

    description = fields.Char(string='Description',default='')

    #at a time change 2 field values..!
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name + ' - ' + (self.product_id.default_code or '') # for Update description on change the product
            self.unit_price = self.product_id.lst_price

class DamagedSpareParts(models.Model):
    _name = 'spare.parts'
    _description = 'mobile damaged parts'
    _rec_name = 'damaged_spare_parts_name' #for appear the name

    damaged_spare_parts_name = fields.Char(string = 'Damaged SpareParts')

class SaleOrder(models.Model):
    _inherit = "sale.order"

    vat = fields.Char(string ='Vat', related = 'partner_id.vat')
    global_discount = fields.Float(string="Global Discount")

    def global_discount_btn(self):
        self.order_line.update_discount(self.global_discount)
        
    @api.constrains('amount_total')
    def action_confirm(self):
        if self.amount_total > 10000:
            raise ValidationError("Total Amount is Greater then 10,000$")
        return super(SaleOrder, self).action_confirm()

    @api.constrains('validity_date')
    def date_validation(self):
        current_date = datetime.now().date() #get a current date
        if self.validity_date:
            if self.validity_date < current_date:
                raise ValidationError("Expiration Date in Past...! ")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount = fields.Float(string = 'Discount') #, related = 'order_id.global_discount'

    def update_discount(self, discount):
        self.write({'discount': discount})

# class RejectWizard(models.TransientModel):
#     _name = 'reject.wizard'
#     _description = "Reject Wizard"

#     reason = fields.Text(string='Reason')

#     def action_confirm_reject(self):
#         active_id = self.env.context.get('active_id')
#         if active_id:
#             service_record = self.env['mobile.service.shop'].browse(active_id)
#             service_record.action_rejected(self.reason)
#         return {'type': 'ir.actions.act_window_close'}

# class ReportMobileServiceOrder(models.AbstractModel):
#     _name = 'mobile.service.shop.document'
#     _description = 'Mobile Service Shop Report'

#     def _get_report_values(self, docids, data=None):
#         docs = self.env['mobile.service.shop'].browse(docids)
#         return {
#             'doc_ids': docids,
#             'doc_model': 'mobile.service.shop',
#             'docs': docs,
#         }

# class MobileServiceOrderController(models.AbstractModel):
#     _name = 'mobile.service.shop.report'
#     # _inherit = 'report.report_custom'

#     def _get_report_values(self, docids, data=None):
#         docids = docids or self.env.context.get('active_ids')
#         return {
#             'doc_ids': docids,
#             'doc_model': 'mobile.service.shop',
#             'docs': self.env['mobile.service.shop'].browse(docids),
#         }
