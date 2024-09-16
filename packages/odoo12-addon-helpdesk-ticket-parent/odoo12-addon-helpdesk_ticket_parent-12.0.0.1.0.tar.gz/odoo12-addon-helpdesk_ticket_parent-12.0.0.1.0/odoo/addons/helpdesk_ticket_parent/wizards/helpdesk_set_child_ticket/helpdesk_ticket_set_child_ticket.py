from odoo import api, fields, models
from odoo.exceptions import UserError


class HelpdeskTicketMassiveCreation(models.TransientModel):
    _name = "helpdesk.ticket.parent.set.child.ticket"

    global_ticket_id = fields.Many2one(
        "helpdesk.ticket",
        string="Global Ticket",
        required=True,
        domain="['!', ('global_child_ticket_ids_count', '=', 0)]"
    )

    global_name = fields.Char(
        string="Parent Ticket Name",
        related="global_ticket_id.name",
    )

    child_ticket_ids = fields.Many2many(
        "helpdesk.ticket",
        string="Selected Child Tickets",
        domain="[('parent_ticket_id', '=', False), ('child_ticket_ids', '=', False)]",  # Not child nor father
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["global_ticket_id"] = self.env.context.get("default_global_ticket_id")
        return defaults

    def button_done(self):
        self.ensure_one()
        if not len(self.child_ticket_ids):
            raise UserError("There are no tickets to assign!")
        self.child_ticket_ids.write({'parent_ticket_id': self.global_ticket_id.id})
