# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CreateShow(models.TransientModel):
    _name = 'create.show.wizard'

    _description = 'Wizard to show the dates after the selected date and their tickets not sold yet'

    date = fields.Date('Show Date')

    def get_date(self):
        result = []
        for rec in self:
            result = self.env['film.film'].search([('movie_date', '>', rec.date),
                                                   ('tickets_sold', '=', False)])
        return {
            'name': _('Show By Date'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'film.film',
            'domain': [('id', 'in', result.ids)],  # ex
        }
