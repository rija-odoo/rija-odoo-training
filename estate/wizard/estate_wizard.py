from odoo import models, fields


class EstateWizard(models.TransientModel):
    _name = "estate.wizard"
    _description = "Estate Wizard"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, string="Price"
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)

# Function For Wizard Offer

    def wizard_offer(self):
        selected_ids = self.env.context.get('active_ids')
        for record in selected_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'status': self.status,
                'partner_id': self.partner_id.id,
                'property_id': record,
            })
        return True
