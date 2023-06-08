from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The Type name already exists!'),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_offer_count')

# Functions For Offer Count

    @api.depends('offer_ids')
    def _offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
