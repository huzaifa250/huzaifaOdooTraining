# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
# import time
# import json
# import datetime
# import io
from odoo.exceptions import ValidationError, UserError
# from odoo.tools import date_utils
# from odoo.tools.misc import xlsxwriter


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

    # def get_print_xlsx_report(self, data, response):
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     sheet = workbook.add_worksheet()
    #     cell_format = workbook.add_format({'font_size': '12px'})
    #     head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
    #     txt = workbook.add_format({'font_size': '10px'})
    #     sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
    #     sheet.write('B6', 'From:', cell_format)
    #     sheet.merge_range('C6:D6', data['date'], txt)
    #     sheet.write('F6', 'To:', cell_format)
    #     sheet.merge_range('G6:H6', data['date'], txt)
    #     workbook.close()
    #     output.seek(0)
    #     response.stream.write(output.read())
    #     output.close()
    #     return {
    #         'type': 'ir_actions_xlsx_download',
    #         'data': {'model': 'create.show.wizard',
    #                  'options': json.dumps(data, default=date_utils.json_default),
    #                  'output_format': 'xlsx',
    #                  'report_name': 'Excel Report',
    #                  },
    #         'report_type': 'xlsx',
    #     }
