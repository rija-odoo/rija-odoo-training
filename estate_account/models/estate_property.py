from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            "line_ids": [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 110
                }),
                Command.create({
                    'name': 'taxe',
                    'quantity': 1,
                    'price_unit': 60
                })
            ]
        })
        return super(EstateProperty, self).action_sold()
