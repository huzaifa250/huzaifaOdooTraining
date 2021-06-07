# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CreateShow(models.TransientModel):
    _name = 'create.show.wizard'

    _description = ''

    date = fields.Date('Show Date')
    tickets_sold = fields.Boolean('Tickets are Sold out', default=False)

    def get_date(self):
        result = []
        for rec in self:
            result = self.env['create.show.wizard'].search([('date', '=', rec.date)])
        return {
            'name': _('Show By Date'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'create.show.wizard',
            'domain': [('id', 'in', result.ids)],
        }
