# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Cinema(models.Model):
    _name = 'cinema.show'

    _description = 'An Erp System for Cinema'
    start = fields.Date('Start Date')
    show_hall = fields.Char('Show Hall', copy=True)
    nums_sets = fields.Integer('Number of Sets')
    reserved_seat_no = fields.Integer('Reserved Seats Number')
    halls_supervisor = fields.Many2one('hr.employee', string='Supervisor')
    name = fields.Many2one('film.film', string='Movie Name', required=True)
    reservation_ids = fields.One2many('cinema.show.reservation', 'reserve_id_inverse', string='Reservation Ids')

    def smart_button(self):
        for rec in self:
            return {
                'name': _('Cinema'),
                'view_type': 'tree',
                'view_mode': 'tree,form',
                'res_model': 'cinema.show',
                'type': 'ir.action.act_window',
                'domain': [()],

            }


class Film(models.Model):
    _name = 'film.film'
    _rec_name = 'movie_name'

    movie_name = fields.Char('Movie Name')
    movie_duration = fields.Float('Movie Duration')
    currency_id = fields.Many2one('res.currency', string='Currency')
    price = fields.Monetary('Price', required=True)
    movie_date = fields.Date('Movie Date', default=lambda self: fields.datetime.now())
    tickets_sold = fields.Boolean('Tickets are Sold out')
    description = fields.Text('Description')
    sequence = fields.Char(readonly=True, copy=False, default='New')
    requester = fields.Char('Requester')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.movie_name + '/' + str(record.movie_date)))
            # show_hall in another model + there is no relation
        return result

    @api.constrains('requester', 'movie_name')
    def _check_request_movies(self):
        for rec in self:
            result = self.env['film.film'].search(
                [('requester', '=', rec.requester), ('movie_name', '=', rec.movie_name)
                 ])
        if len(result) > 1:
            raise ValidationError(_('Requester must not have more than request in same day.'))

    @api.onchange('tickets_sold', 'movie_name')
    def _onchange_ticket_sold(self):
        if self.tickets_sold:
            self.description = 'Tickets are sold out'
        if not self.tickets_sold:
            self.description = ''

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('film.film') or _('new')
            res = super(Film, self).create(vals)
            return res


class CinemaReservation(models.Model):
    _name = 'cinema.show.reservation'
    _rec_name = 'show'

    show = fields.Many2one('cinema.show', string='Show', required=True, ondelete='cascade')
    m2m_real = fields.Many2many('res.partner', 'cinema_show_relation', string='Many2Many')
    reserve_id_inverse = fields.Many2one('cinema.show', string='Reserve')


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone and len(rec.phone) < 10:
                raise ValidationError(_('Phone number must not be less than 10 !'))

    # sql constraints unique name
    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Name must be Unique per record !"),
    # ]
    # sql constraints unique email
    _sql_constraints = [('email_uniq', 'unique (email)', 'Email must be Unique for person!'), ]
