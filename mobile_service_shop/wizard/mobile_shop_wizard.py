from odoo import models, fields, api

class RejectWizard(models.TransientModel):
    _name = 'reject.wizard'
    _description = "Reject Wizard"

    reason = fields.Text(string='Reason')

    def action_confirm_reject(self):
        active_id = self.env.context.get('active_id')
        if active_id and self.reason: 
            service_record = self.env['mobile.service.shop'].browse(active_id)
            service_record.write({
                'reason': self.reason
                # 'state': 'reject'
            })
        return {'type': 'ir.actions.act_window_close'}
