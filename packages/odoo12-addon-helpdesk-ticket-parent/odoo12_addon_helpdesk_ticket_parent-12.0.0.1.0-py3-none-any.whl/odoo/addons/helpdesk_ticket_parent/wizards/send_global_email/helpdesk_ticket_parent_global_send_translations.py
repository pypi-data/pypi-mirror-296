from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class HelpdeskTicketParentSendGlobalTranslation(models.TransientModel):
    _name = "helpdesk.ticket.parent.send.global.translation"
    _rec_name = "display_ticket_language_name"
    _order = "is_translated desc"

    bind_global_ticket_email_transient_id = fields.Many2one(
        comodel_name="helpdesk.ticket.parent.send.global.email",
        string="Global Ticket Wizard",
        required=True,
        index=True
    )
    ticket_language_id = fields.Many2one(
        "res.lang",
        string="Language",
        domain="[('active', '=', True)]",
        required=True
    )
    ticket_language_name = fields.Char(
        related="ticket_language_id.name",
        string="Language Name"
    )
    display_ticket_language_name = fields.Char(
        compute="compute_display_ticket_language_name",
        reaonly=True,
        store=False
    )
    translation_text = fields.Html(
        string="Translated Text",
        default=False
    )
    translation_subject = fields.Char(
        string="Subject of the email",
        default=False
    )
    mail_template_id = fields.Many2one(
        "mail.template",
        ondelete='set null',
        string="Email Template",
        domain="[('model_id', '=', 'helpdesk.ticket')]",
    )
    is_translated = fields.Boolean(
        compute="compute_is_translated",
    )

    @api.onchange('translation_text')
    def compute_is_translated(self):
        for record in self:
            record.is_translated = bool(len(record.translation_text or ""))

    @api.onchange('is_translated')
    def compute_display_ticket_language_name(self):
        for record in self:
            display_name = record.ticket_language_name + (" ☑" if record.is_translated else "")
            record.display_ticket_language_name = display_name
