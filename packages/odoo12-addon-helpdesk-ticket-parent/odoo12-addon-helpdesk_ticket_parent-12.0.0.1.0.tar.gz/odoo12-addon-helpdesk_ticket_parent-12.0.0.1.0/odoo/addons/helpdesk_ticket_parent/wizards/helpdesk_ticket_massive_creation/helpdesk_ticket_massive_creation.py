from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class HelpdeskTicketMassiveCreation(models.TransientModel):
    _inherit = "helpdesk.ticket.massive.creation.wizard"
    is_parent = fields.Boolean("parent")

    @api.multi
    def button_create(self):
        if self.is_parent:
            ticket_params = {
                "name": self.name,
                "category_id": self.category_id.id,
                "team_id": self.team_id.id,
                "user_id": self.user_id.id,
                "tag_ids": [(6, 0, self.tag_ids.ids)],
                "priority": self.priority,
                "description": self.description,
            }

            parent_ticket = self.env["helpdesk.ticket"].create(ticket_params)

            _logger.debug(f" Parent ticket created {parent_ticket.id}")

            # In case there are contract_ids assigned instead of partner_ids
            partner_contract_dict = {}
            if self.contract_ids and not self.res_partner_ids:
                # For performance purposes the partner id is mapped with
                # their contract id so we are overcomming the ORM when
                # we ask what contract comes from which partner
                partner_contract_dict = dict(
                    map(
                        lambda contract: (contract.partner_id.id, contract.id),
                        self.contract_ids,
                    )
                )
                self.res_partner_ids = list(partner_contract_dict.keys())

            _logger.debug(f" Child tickets to be created: {self.res_partner_ids.ids}")
            # Creating the children with their own unique code numbering according to the specification
            # Firstly we update the original global number so that we insert
            # like follows: G-{ORIG_NUMB} while the children are: {ORIG_NUMB}-N
            common_number = str(parent_ticket.number)
            parent_ticket.number = "G-" + common_number
            for i, partner in enumerate(self.res_partner_ids, 1):

                params = ticket_params.copy()
                params.update(
                    {
                        "number":           common_number + "-" + str(i),
                        "partner_id":       partner.id,
                        "partner_name":     partner.name,
                        "partner_email":    partner.email,
                        "parent_ticket_id": parent_ticket.id,
                    }
                )
                if self.contract_ids:
                    params["contract_id"] = partner_contract_dict.get(partner.id)
                params.pop("message_follower_ids")  # User can not follow twice the same object
                _logger.debug(f" Creating child ticket...\n{str(params)}\n")

                hijo = self.env["helpdesk.ticket"].create(params)

                _logger.debug(f" Child ticket created {hijo.id}")
        else:
            super().button_create()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["is_parent"] = self.env.context.get("is_parent")
        return defaults
