from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class DateReportWizard(models.TransientModel):
    _name = 'maintenodoo.date.report.wizard'
    _description = 'Date Report Wizard'

    start_date = fields.Date(string='Fecha Inicial', required=True)
    end_date = fields.Date(string='Fecha Final', required=True)
    mantenimientos_ids = fields.Many2many('maintenodoo.mantenimiento', string='Mantenimientos')


    def print_report(self):

        _logger.info('Imprimiendo Reporte de Mantenimientos')
        return True