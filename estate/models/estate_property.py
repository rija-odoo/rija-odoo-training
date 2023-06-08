from odoo import api, fields, models, _, exceptions
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Plans"
    _order = "name"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price>=0)',
         'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price>=0)',
         'Selling price must be strictly positive'),
        ('name_uniq', 'unique(name)', 'The Title name already exists!')
    ]

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(
        readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedroom")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(String="Garden")
    garden_area = fields.Integer(
        compute="_compute_garden", readonly=False, string="Garden Area")
    date_availability = fields.Date(
        copy=False, default=lambda self: date.today()+relativedelta(months=+3))
    garden_orientation = fields.Selection(
        selection=[
            ('south', 'South'), ('north', 'North'), ("west", "West"), ("east", "East")],
        string='Type', compute="_compute_garden",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', ' Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=True, default='new',
        string='State',
    )
    image = fields.Binary(string="Image")
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    seller_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(
        string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Price", compute="_compute_best_price")


# Function For Compute Total Area


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

# Function For Compute Best Price   

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = [offer.price for offer in record.offer_ids if offer.price]
            record.best_price = max(prices) if prices else 0

# Function For Compute Graden

    @api.depends("garden")
    def _compute_garden(self):
        if self.garden:
            self.garden_area = "10"
            self.garden_orientation = "north"
        else:
            self.garden_orientation = False
            self.garden_area = False

# Function For Action Sold

    def action_sold(self):
        if self.state == "canceled":
            raise UserError("Cancled Properties can't be sold")
        else:
            self.state = "sold"
        return True

# Function For Action Canlcled

    def action_cancled(self):
        if self.state == "sold":
            raise UserError("sold properties can't be cancled")
        else:
            self.state = "canceled"
        return True

# Function For Check Selling Price

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and not float_is_zero(record.expected_price, precision_digits=2)
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1
            ):
                raise ValidationError(
                    "Selling price cannot be lower than 90% of the expected price.")

# Function For Deleting Record

    @api.ondelete(at_uninstall=False)
    def _deleting_record(self):
        if self.state in ['offer_received', 'sold', 'offer_accepted']:
            raise UserError("only new and canceled property can be deleted")
