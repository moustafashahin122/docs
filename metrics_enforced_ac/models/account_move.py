from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    # gett all account move lines and check if all income and expense relateed lines having analytic account
    
    def validate_all_lines_have_analytic_account(self):
        for rec in self:
            for line in rec.line_ids:
                if line.account_id.user_type_id.internal_group in ['income','expense'] and not line.analytic_account_id:
                    raise ValidationError(_("Please add analytic account for all income and expense lines"))
        return True
    
    #override save method to check if all income and expense relateed lines having analytic account
    def action_post(self):
        self.validate_all_lines_have_analytic_account()
        return super(AccountMove, self).action_post()