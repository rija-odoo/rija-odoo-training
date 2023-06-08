from odoo import fields, models, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price"
    _sql_constraints = [('check_price', 'CHECK(price>0)',
                         'Offer price must be strictly positive'),]

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False, string="Status"
    )
    partner_id = fields.Many2one(
        "res.partner", required=True, string="Partner")
    property_id = fields.Many2one(
        "estate.property", required=True, string="Property")
    validity = fields.Integer(default="7", string="Validity")
    date_deadline = fields.Date(
        string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True)

# Functions For Inverse Date Deadline

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               datetime.date(record.create_date)).days

# Functions For Compute Date Deadline

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if (record.create_date):
                record.date_deadline = record.create_date + \
                    relativedelta(days=+record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=+record.validity)

# Functions For Action Accepted

    def action_accepted(self):
        for record in self:
            record.property_id.offer_ids.status = 'refused'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = self.partner_id
            record.property_id.state = 'offer_accepted'

# Functions For Action Refused

    def action_refused(self):
        for record in self:
            self.status = "refused"
            self.property_id.selling_price = 0
            self.property_id.buyer_id = ""

# Inheritance

    @api.model
    def create(self, vals):
        temp = self.env['estate.property'].browse(vals['property_id'])
        temp.state = "offer_received"
        if temp.best_price >= vals['price']:
            raise UserError(
                "offer price should be greater than existing offer %.2f" % temp.best_price)
        return super().create(vals)
