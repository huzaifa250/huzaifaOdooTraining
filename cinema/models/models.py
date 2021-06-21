# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Cinema(models.Model):
    _name = 'cinema.show'
    _description = 'An Erp System for Cinema'
    _rec_name = 'movie_name'
    _check_company_auto = True  # ensure multi-company consistency

    movie_name = fields.Many2one('film.film', 'Movie Name')
    start = fields.Date('Start Date', default=lambda self: fields.Date.today())
    show_hall = fields.Char('Show Hall', copy=True, required=True)
    nums_sets = fields.Integer('Number of Sets', required=True)
    reserved_seat_no = fields.Integer('Reserved Seats Number')
    halls_supervisor = fields.Many2one('hr.employee', 'Supervisor', check_company=True)
    requester = fields.Char('Requester', required=True)
    reservation_ids = fields.One2many('cinema.show.reservation', 'reserve_id_inverse', string='Reservation Ids')
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)

    @api.constrains('requester', 'movie_name')
    def _check_request_movies(self):
        for rec in self:
            result = self.env['cinema.show'].search(
                [('requester', '=', rec.requester), ('movie_name', '=', rec.movie_name.id)])
            if len(result) > 1:
                raise ValidationError(_('Requester must not have more than request in same day.'))

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.show_hall + '/' + str(record.start)))

        return result


class Film(models.Model):
    _name = 'film.film'

    name = fields.Char('Name', required=True)
    movie_duration = fields.Float('Movie Duration', default=1.30)
    currency_id = fields.Many2one('res.currency', string='Currency')
    price = fields.Monetary('Price', required=True)
    movie_date = fields.Date('Movie Date', default=lambda self: fields.datetime.now())
    tickets_sold = fields.Boolean('Tickets are Sold out')
    description = fields.Text('Description')
    sequence = fields.Char(readonly=True, copy=False, default='New')

    @api.onchange('tickets_sold')
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
    m2m_real = fields.Many2many('res.partner', 'cinema_show_relation', string='Responsible Person')
    reserve_id_inverse = fields.Many2one('cinema.show', string='Reserve')


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('phone')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone and len(rec.phone) != 10:
                raise ValidationError(_('Phone number must be 10 digits !'))

    @api.constrains('name')
    def _check_unique_name(self):
        for rec in self:
            result = self.env['res.partner'].search([('name', '=', rec.name)])
            if len(result) > 1:
                raise ValidationError(_('Partner Name must be unique !'))
