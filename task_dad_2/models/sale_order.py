from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    user_d = fields.Many2one(comodel_name="res.users", string="User only", required=False, compute='_compute_user_d')

    @api.depends()
    def _compute_user_d(self):
        for x in self:
            x.user_d = self.env.user


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('phone')
    def phone_validation(self):
        partners = self.search([])
        for partner in partners:
            if partner.phone and self.phone:
                if partner.phone == self.phone:
                    raise ValidationError('The Phone Number already Exist')

    @api.constrains('phone')
    def check_phone(self):
        for rec in self:
            if rec.phone and len(rec.phone) != 11:
                raise ValidationError('Phone . must be 11 character or number.')
