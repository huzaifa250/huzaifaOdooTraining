# -*- coding: utf-8 -*-


from odoo import models, fields


class Cinema(models.Model):
    _name = 'cinema.cinema'
    _description = 'An Erp System for Cinema'

    name = fields.Char('Name', required=True)
    set_no = fields.Integer('Sets')
    description = fields.Text('Description')


class Film(models.Model):
    _name = 'film.film'
    _description = 'Film and Display Information'

    f_name = fields.Char('Film Name', required=True, copy=True)
    type = fields.Selection([('A', 'Action'), ('An', 'Anime'), ('c', 'Comedy')])
    date = fields.Date('Film Time')
    info = fields.Text('More Info')
