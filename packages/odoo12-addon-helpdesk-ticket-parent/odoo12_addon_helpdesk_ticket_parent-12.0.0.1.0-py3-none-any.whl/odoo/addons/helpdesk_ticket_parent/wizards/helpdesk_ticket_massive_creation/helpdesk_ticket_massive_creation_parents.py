from odoo import api, models, _


class HelpdeskTicketMassiveCreation(models.TransientModel):
    _name = "helpdesk.ticket.massive.creation.parent.wizard"

    @api.multi
    def button_create_global_ticket(self):
        ctx = self.env.context.copy() or {}
        ctx['is_parent'] = True
        return {
            'name': _('Create tickets massively (Global ticket)'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': "helpdesk.ticket.massive.creation.wizard",
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def button_create_independent_ticket(self):
        ctx = self.env.context.copy() or {}
        ctx['is_parent'] = False
        return {
            'name': _('Create tickets massively (Independent tickets)'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': "helpdesk.ticket.massive.creation.wizard",
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }
