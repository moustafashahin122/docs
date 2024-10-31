# my_module/controllers/my_controller.py
from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/my_module/get_contacts', type='json', auth='user', methods=['POST'])
    def get_contacts(self):
        # Query contacts (partners) from the database
        
        contacts = request.env['res.partner'].search([('is_company', '=', False)])
        
        # Convert the contacts to a dictionary format
        contact_data = [{
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
        } for contact in contacts]

        return {'contacts': contact_data}
