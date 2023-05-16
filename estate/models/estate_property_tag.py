from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The Tag name already exists!'),
    ]

    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="Colour")
