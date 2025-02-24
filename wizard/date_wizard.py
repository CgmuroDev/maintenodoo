from odoo import models, fields, api


class DateReportWizard(models.TransientModel):
    _name = 'maintenodoo.date.report.wizard'
    _description = 'Wizard para reporte de mantenimiento'

    start_date = fields.Date(string='Fecha de inicio', required=True)
    end_date = fields.Date(string='Fecha de fin', required=True)
    mantenimientos_ids = fields.Many2many('maintenodoo.mantenimiento', string='Mantenimientos')

    @api.onchange('start_date', 'end_date')
    def onchange_dates(self):
        print("Ejecutando onchange_dates")
        if self.start_date and self.end_date:
            mantenimientos = self.env['maintenodoo.mantenimiento'].search([
                ('programed_date', '>=', self.start_date),
                ('executed_date', '<=', self.end_date)
            ])
            print(f"Mantenimientos encontrados: {len(mantenimientos)}")
            self.mantenimientos_ids = [(6, 0, mantenimientos.ids)]

    def print_report(self):

        manteniemientos = self.env['maintenodoo.mantenimiento']

        domain = [
            ('programed_date', '>=', self.start_date),
            ('executed_date', '<=', self.end_date)
        ]
        if self.mantenimientos_ids:
            domain.append(('id', 'in', self.mantenimientos_ids.ids))

        manfields = ['name', 'programed_date', 'executed_date', 'equipment_id']

        manrecords = manteniemientos.search_read(domain, manfields)

        data = {
            'manrecords': manrecords,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

        return self.env.ref('maintenodoo.report_mantenimiento_fecha').report_action(self, data=data)


