## -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api,_
from odoo.exceptions import UserError, Warning

#mobileshop fields
class MobileServiceShop(models.Model):
    _name = 'mobile.service.shop'
    _description = 'All Types of Mobiles Service Here!!'
    _rec_name = 'customer_id'

    sequence = fields.Char(default='New', readonly=True, states={'draft': [('readonly', False)]})
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
    total = fields.Float(string = 'Total', compute='calculate_total', readonly=True)#, states={'draft': [('readonly', False)]}

    @api.depends('mobile_service_line_ids.subtotal')
    def calculate_total(self):
        for v in self:
            v.total = sum(s.subtotal for s in v.mobile_service_line_ids)

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('cancel', 'Cancelled')], string='State', default='draft')

    @api.constrains('mobile_service_line_ids.product_id')
    def action_confirm(self):
        self.state = 'confirm'          #'confirm_clicked' : True ----- or self.write({'state': 'confirm'})
        if not self.mobile_service_line_ids:
            raise Warning("No product selected! Please choose a product.")
        if self.sequence == 'New':
            self.sequence = self.env['ir.sequence'].next_by_code('mobile.shop.sequence') or _('New')
        
    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

        # if self.state == 'cancel':  for pafter cancel to---> delete the product in the table
        #     return super(MobileServiceShop, self).unlink()

    @api.model
    def create(self, vals):
        if 'mobile_service_line_ids' in vals and not vals['mobile_service_line_ids']: #or vals.get("fieldName")
            raise Warning("No product selected! Please choose a product.")
        return super(MobileServiceShop, self).create(vals)

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
    unit_price = fields.Float(string='UnitPrice',readonly='1')#related = 'product_id.lst_price'
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

    description = fields.Char(string='Description',required=True)

    #at a time change 2 field values..!
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name + ' - ' + (self.product_id.default_code or '') # for Update description on change the product
            self.unit_price = self.product_id.lst_price

class DamagedSpareParts(models.Model):
    _name = 'spare.parts'
    _description = 'mobile damaged parts'
    _rec_name = 'damaged_spare_parts_name'

    damaged_spare_parts_name = fields.Char(string = 'Damaged SpareParts')
