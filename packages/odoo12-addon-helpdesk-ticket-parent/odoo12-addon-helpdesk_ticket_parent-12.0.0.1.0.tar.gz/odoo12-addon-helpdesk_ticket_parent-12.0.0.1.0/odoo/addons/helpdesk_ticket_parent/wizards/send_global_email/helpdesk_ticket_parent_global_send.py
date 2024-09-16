from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from lxml import etree
import logging

_logger = logging.getLogger(__name__)


class HelpdeskTicketParentSendGlobalEmail(models.TransientModel):
    _name = "helpdesk.ticket.parent.send.global.email"

    global_ticket_id = fields.Many2one(
        comodel_name="helpdesk.ticket",
        string="Global Ticket",
        domain="['!', ('child_ticket_ids', '=?', False)]",
        default=lambda self: self.env.context.get('active_id'),
        required=True
    )
    global_name = fields.Char(
        string="Parent Ticket Name",
        related="global_ticket_id.name",
    )
    ticket_language_ids = fields.One2many(
        "helpdesk.ticket.parent.send.global.translation",
        "bind_global_ticket_email_transient_id",
        string="Available Translations",
    )
    lang_cursor = fields.Many2one(
        comodel_name="helpdesk.ticket.parent.send.global.translation",
        string="Selected Language",
        domain="[('id', 'in', ticket_language_ids)]"
    )
    lang_cursor_text = fields.Html(
        string="Message translated to send",
        related="lang_cursor.translation_text",
        readonly=False
    )
    lang_cursor_subject = fields.Char(
        string="Subject of the email",
        related="lang_cursor.translation_subject",
        readonly=False
    )
    mail_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        related="lang_cursor.mail_template_id",
        readonly=False,
        domain="[('model_id', '=', 'helpdesk.ticket')]",
    )

    @api.one
    def button_send(self):
        # Logic for sending each mail to a queue.job
        any_mail_sent = False
        translation_model = self.env['helpdesk.ticket.parent.send.global.translation']
        all_sendable_partners = self.get_all_sendable_partners(self.global_ticket_id.id)
        all_sendable_partners_ids = all_sendable_partners.ids if all_sendable_partners else []
        for child_ticket in self.global_ticket_id.child_ticket_ids:
            template = self.env['mail.template'].browse(self.mail_template_id.id)
            # Send to each child
            followers = child_ticket.mapped('message_partner_ids').filtered(lambda f: f.id in all_sendable_partners_ids)
            for follower in followers:
                if not follower.email or not follower.lang:
                    continue
                translation = translation_model.search(
                    [
                        ('id', 'in', self.ticket_language_ids.ids),
                        ('ticket_language_id.code', '=', follower.lang),
                    ],
                    limit=1
                )
                if not translation:
                    raise UserError(
                        _("OPERATION ABORTED (Reason: Translation needed but not found: ") + follower.lang + ")"
                    )
                body_html = self.env['mail.template']._render_template(
                    translation.translation_text,
                    'helpdesk.ticket',
                    child_ticket.id,
                    post_process=True
                )
                subject = self.env['mail.template']._render_template(
                    translation.translation_subject,
                    'helpdesk.ticket',
                    child_ticket.id,
                    post_process=False
                )
                email_values = {
                    'email_to': follower.email,
                    'mail_server_id': template.mail_server_id.id,
                    'subject': subject,
                    'body_html': body_html,
                    'res_id': child_ticket.id,
                    'model': 'helpdesk.ticket',
                }
                # body: sanitize and create the mail object
                email_values['body'] = tools.html_sanitize(email_values['body_html'])
                mail_to_send = self.env['mail.mail'].create(email_values)
                if mail_to_send:
                    # Finally send them through queue_job utility
                    mail_to_send.with_delay().send()
                    any_mail_sent = True
            # Some notifications posts
            message_child_tickets = _(
                "This Ticket has sent a new mail to all the followers massively ordered from the Global Ticket <a href=# data-oe-model=helpdesk.ticket data-oe-id=%d>%s</a>"  # noqa: E501
            ) % (
                child_ticket.parent_ticket_id.id,
                child_ticket.parent_ticket_id.name
            )
            child_ticket.message_post(
                body=message_child_tickets,
                message_type='comment'
            )
        if any_mail_sent:
            message_parent_ticket = _(
                "An email has been massively sent to all the children ticket followers automatically."
            )
            self.global_ticket_id.message_post(
                body=message_parent_ticket,
                message_type='notification'
            )
        return True

    @api.multi
    def button_translation_save(self):
        self.ensure_one()
        translation_model = self.env['helpdesk.ticket.parent.send.global.translation']
        if self.lang_cursor:
            self.lang_cursor.translation_text = self.lang_cursor_text
            self.lang_cursor = translation_model.search(
                [('id', 'in', self.ticket_language_ids.ids)],
                order='is_translated desc',
                limit=1
            ).id

    @api.onchange('mail_template_id')
    def render_email_template(self):
        for record in self:
            if record.mail_template_id and self.lang_cursor:
                template = record.with_context({'lang': self.lang_cursor.ticket_language_id.code}).mail_template_id
                fields = ['subject', 'body_html', 'email_from', 'reply_to', 'mail_server_id']
                values = dict((field, getattr(template, field)) for field in fields if getattr(template, field))
                if values.get('body_html'):
                    for translation in record.ticket_language_ids:
                        translation.translation_text = values.get('body_html') or "" + "\n" + (
                            translation.translation_text or ""
                        )
                        translation.translation_subject = values.get('subject') or "" + "\n" + (
                            translation.translation_subject or ""
                        )

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(HelpdeskTicketParentSendGlobalEmail, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu
        )
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            button_confirm = doc.xpath("//button[@name='button_send']")
            all_sendable_partners = self.get_all_sendable_partners(self.env.context.get("default_global_ticket_id"))
            button_confirm[0].set("string", _("Send to %d partners") % len(all_sendable_partners))
            button_confirm[0].set(
                "confirm",
                _("Are you sure to send a massive mail to %d partners?") % len(all_sendable_partners)
            )
            result['arch'] = etree.tostring(doc, encoding='unicode')

        return result

    @api.model
    def get_all_sendable_partners(self, global_ticket_id: int):
        all_sendable_partners = []
        global_ticket = self.env['helpdesk.ticket'].browse(global_ticket_id)
        if global_ticket:
            assigned_parent_user_partner_id = 0
            if global_ticket.user_id:
                assigned_parent_user_partner_id = global_ticket.user_id.partner_id.id
            all_sendable_partners = global_ticket.child_ticket_ids.mapped('message_partner_ids').filtered(
                lambda f: f.id not in [
                    self.env.user.partner_id.id,
                    assigned_parent_user_partner_id,
                ] + global_ticket.child_ticket_ids.mapped('user_id.partner_id.id')
            )
        return all_sendable_partners

    @api.model
    def default_get(self, fields):
        result = super(HelpdeskTicketParentSendGlobalEmail, self).default_get(fields)
        if result.get("global_ticket_id"):
            global_ticket_id = self.env['helpdesk.ticket'].browse(result.get("global_ticket_id"))
            _logger.debug(f" Global Ticket: {global_ticket_id.name}")
            all_sendable_partners = self.get_all_sendable_partners(global_ticket_id.id)

            lang_list = list(set(all_sendable_partners.mapped('lang')))

            # for each language we create a translation entry
            translation_ids = []
            for lang in lang_list:
                translation_ids.append(
                    (
                        0,
                        0,
                        {
                            'ticket_language_id': self.env['res.lang'].search(
                                [('code', '=', lang)],
                                limit=1
                            ).id
                        }
                    )
                )
            result.update({
                "global_ticket_id": global_ticket_id.id,
                "ticket_language_ids": translation_ids
            })

        return result
