# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _
from odoo.exceptions import UserError


class WizardMerge(models.TransientModel):
    _name = 'helpdesk_split_and_merge.wizard_merge'

    ticket_id = fields.Many2one(
        'helpdesk.ticket',
        default=lambda self: self.env.context.get('active_id'),
        required=True
    )
    merge_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        required=False
    )
    message = fields.Char(
        string="",
        default="This Ticket has been merged into ##",
        placeholder="This Ticket has been merged into ##",
        help="Leave the code ## where you want the ticket link to be"
    )
    message_main_ticket = fields.Char(
        string="",
        default="The Ticket ## was closed and has been merged into this Ticket",
        placeholder="The Ticket ## was closed and has been merged into this Ticket",
        help="Leave the code ## where you want the ticket link to be"
    )

    def action_merge_ticket(self):

        if not (self.ticket_id and self.merge_ticket_id):
            raise UserError(_("A Ticket to merge into has to be set."))

        if self.ticket_id.id == self.merge_ticket_id.id:
            raise UserError(_("You can not merge a ticket with itself."))

        if self.ticket_id.partner_id != self.merge_ticket_id.partner_id:
            raise UserError(
                _("Tickets to merge must belong to the same Partner."))

        # Actual act of setting the tickets as origin and merged respectively
        self.ticket_id.write({'merge_ticket_id': self.merge_ticket_id.id})

        # Close the ticket and move it to the specified stage
        merge_stage = self.env.user.company_id.merge_ticket_stage
        if not merge_stage:
            raise UserError(
                _("No stage found in settings for closing tickets."))

        self.ticket_id.write({'stage_id': merge_stage.id})

        if self.message:
            link = "<a href=# data-oe-model=helpdesk.ticket data-oe-id=%d>%s</a>" % (
                self.merge_ticket_id.id, self.merge_ticket_id.name)
            message = self.message.replace("##", link)
            self.ticket_id.message_post(body=message)
        if self.message_main_ticket:
            link = "<a href=# data-oe-model=helpdesk.ticket data-oe-id=%d>%s</a>" % (
                self.ticket_id.id, self.ticket_id.name)
            message = self.message_main_ticket.replace("##", link)
            self.merge_ticket_id.message_post(body=message)

        # Send email notification if configured
        if self.env.user.company_id.merge_email_template:
            template = self.env.user.company_id.merge_email_template
            template.send_mail(self.ticket_id.id, force_send=True)

        return True
