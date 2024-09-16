from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    parent_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Parent Ticket'
    )
    child_ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'parent_ticket_id',
        string='Children Tickets'
    )

    global_child_ticket_ids_count = fields.Integer(
        'Global Child Count', compute="_compute_global_child_ticket_ids_count", store=False)

    @api.multi
    def write(self, vals):
        res = super(HelpdeskTicket, self).write(vals)

        if "stage_id" in vals.keys():
            for record in self:
                # Propagate the stage_id change to all the children
                if record.global_child_ticket_ids_count:
                    records_to_change = record.child_ticket_ids.filtered(
                        # filter to get only the ones that are not further in sequence
                        lambda child: child.stage_id.sequence <= record.stage_id.sequence
                    )
                    records_to_change.write({'stage_id': record.stage_id.id})
        return res

    @api.multi
    @api.depends('child_ticket_ids')
    def _compute_global_child_ticket_ids_count(self):
        for ticket in self:
            ticket.global_child_ticket_ids_count = len(ticket.child_ticket_ids)

    def action_set_child_ticket(self, context):
        self.ensure_one()
        if not self.child_ticket_ids:
            raise UserError(
                "The ticket needs to be already a Global ticket in order to assign more child tickets.\n"
                "If you need to assign a group of tickets as childs to a common already created ticket first \n"
                "select them all in a list view and then select the action Set Global Parent searching for it."
                )
        return {
            "name": "Add Child Tickets",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "helpdesk.ticket.parent.set.child.ticket",
            "type": "ir.actions.act_window",
            'target': 'new',
            "context": context,
        }

    def get_view_helpdesk_global_parent_ticket(self, context):
        return {
            "name": self.name,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "helpdesk.ticket",
            "res_id": context.get("parent_ticket_id"),
            "type": "ir.actions.act_window",
            "context": context,
        }

    def server_action_open_send_email_wizard(self, context):
        if not context.get("default_global_ticket_id"):
            raise UserError(_("No Global Ticket found in context"))
        wizard = self.env['helpdesk.ticket.parent.send.global.email']
        vals = {
            "global_ticket_id": self.id,
            "ticket_language_ids": wizard.with_context(context).default_get(
                [
                    'global_ticket_id',
                    'ticket_language_ids'
                ]
                ).get('ticket_language_ids'),
        }
        wizard_to_return = wizard.create(vals)
        return {
            "name": _("Send global email to All"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": "helpdesk.ticket.parent.send.global.email",
            "res_id": wizard_to_return.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            "context": context,
        }
