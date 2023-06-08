from odoo import http


class EstateControllers(http.Controller):

    @http.route('/estate', auth='public',  website=True)
    def index(self, **kw):
        estate_properties = http.request.env['estate.property']
        return http.request.render('estate.index', {
            'properties': estate_properties.search([])
        })

# Function For Front Page Of Website

    @http.route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def front_page(self, page=0, items_per_page=10, **kw):
        domain = [('state', 'in', ['new', 'offer_received'])]
        properties = http.request.env['estate.property'].search([])
        estate_property_count = properties.search_count(
            [('state', 'in', ['new', 'offer_received'])])
        date = kw.get('date')
        if date:
            domain.append(('date_availability', '>=', date))
        pager = http.request.website.pager(
            url="/properties",
            total=estate_property_count,
            page=page,
            step=items_per_page
        )
        response_property = properties.search(
            domain, limit=items_per_page, offset=pager['offset'])
        return http.request.render('estate.front_page', {
            'properties': response_property,
            'pager': pager,
            'selected_date': date,

        })

# Function For Click Property And Go To Next Page Of Property Detail

    @http.route('/properties/<int:id>', type='http', auth='public', website=True)
    def open_property_page(self, id):
        properties = http.request.env['estate.property'].sudo().browse(id)
        return http.request.render('estate.open_property_page', {
            'properties': properties,
        })
