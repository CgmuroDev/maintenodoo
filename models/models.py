from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta
import logging



logger = logging.getLogger(__name__)


class Equipment(models.Model):
    _name = 'maintenodoo.equipment'
    _description = 'Equipo de Mantenimiento'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', default=lambda self: 'New', readonly=True, copy=False)
    category = fields.Selection(
        [('electronic', 'Electrónico'), ('mechanical', 'Mecánico'), ('hydraulic', 'Hidráulico')],
        string='Categoría', required=True
    )
    installation_date = fields.Date(string='Fecha Instalación', default=fields.Date.context_today, required=True)
    last_maintenance = fields.Date(string='Último Mantenimiento')
    state = fields.Selection(
        [('inactivo', 'Inactivo'), ('activo', 'Activo'), ('reparacion', 'Reparación')],
        string='Estado', default='inactivo'
    )
    indicator_result_behavior_graph = fields.Binary(string="Gráfico de Comportamiento",
                                                    compute='_compute_indicator_result_behavior', store=False)
    responsible_id = fields.Many2one('res.users', string='Responsable')
    maintenance_ids = fields.One2many(
        'maintenodoo.mantenimiento',
        'equipment_id',
        string='Mantenimientos',
        domain=[('programed_date', '>=', fields.Date.today())],
        ondelete='cascade'
    )

    @api.constrains('state')
    def _check_state(self):
        for record in self:
            if record.state == 'reparacion':
                raise ValidationError("No se puede modificar equipos en estado de reparación")

    def _compute_indicator_result_behavior(self):
        if not np or not plt:
            raise ValidationError('Por favor instale numpy y matplotlib para ver el gráfico')

        for record in self:
            data = self.env['maintenodoo.equipment'].read_group(
                domain=[],
                fields=['category'],
                groupby=['category'],
            )
            if data:
                categories = ['electronic', 'mechanical', 'hydraulic']
                counts = {d['category']: d['category_count'] for d in data}
                values = [counts.get(cat, 0) for cat in categories]

                fig, ax = plt.subplots()
                ax.bar(categories, values)
                ax.set_ylabel('Cantidad de Equipos')
                ax.set_title('Distribución de Equipos por Categoría')

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close(fig)
                record.indicator_result_behavior_graph = base64.b64encode(buffer.getvalue())
            else:
                record.indicator_result_behavior_graph = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('maintenodoo.equipo') or 'New'
        return super().create(vals_list)


class Mantenimiento(models.Model):
    _name = 'maintenodoo.mantenimiento'
    _description = 'Mantenimiento Preventivo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Referencia', default=lambda self: 'New', readonly=True, copy=False)
    equipment_id = fields.Many2one('maintenodoo.equipment', string='Equipo', required=True, ondelete='cascade')
    programed_date = fields.Date(string='Fecha Programada', required=True)
    executed_date = fields.Date(string='Fecha de Ejecución')
    technician_ids = fields.One2many('maintenodoo.tecnico', 'maintenance_id', string='Técnicos', ondelete='cascade', store=True)
    notes = fields.Text(string='Notas')
    validity = fields.Integer(
        string='Días restantes',
        compute='_compute_validity',
        inverse='_inverse_validity',
        default=0
    )

    costo_por_dia = fields.Float(string='Costo por Día en Pesos', default=50.0, readonly=True)
    costo_por_diario = fields.Monetary(string='Costo Total', readonly=True, compute='_calculate_costo',
                                       currency_field='currency_id')

    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id
    )

    programed_date_from = fields.Date(string='Fecha Programada Desde')
    programed_date_to = fields.Date(string='Fecha Programada Hasta')
    executed_date_from = fields.Date(string='Fecha de Ejecución Desde')
    executed_date_to = fields.Date(string='Fecha de Ejecución Hasta')

    @api.depends('programed_date', 'executed_date')
    def _compute_validity(self):
        for record in self:
            if record.programed_date and record.executed_date:
                record.validity = (record.executed_date - record.programed_date).days
            else:
                record.validity = 0

    @api.onchange('validity')
    def _inverse_validity(self):
        for record in self:
            if record.programed_date:
                record.executed_date = record.programed_date + timedelta(days=record.validity)

    @api.depends('costo_por_dia', 'validity', 'currency_id')
    def _calculate_costo(self):
        for record in self:
            if record.currency_id.name == 'USD':
                record.costo_por_diario = record.costo_por_dia * record.validity / 20
            else:
                record.costo_por_diario = record.costo_por_dia * record.validity

    @api.model
    def cron_notificar_mantenimientos(self):
        logger.info('Ejecutando Cron Job de Notificación de Mantenimientos')
        try:
            today = fields.Date.today()
            target_date = today + timedelta(days=1)
            mantenimientos = self.search([('programed_date', '=', target_date)])
            if mantenimientos:
                for mantenimiento in mantenimientos:
                    equipo = mantenimiento.equipment_id.name
                    for tecnico in mantenimiento.technician_ids:
                        if tecnico.user_id and tecnico.user_id.partner_id:
                            email_to = tecnico.user_id.partner_id.email
                            if email_to:
                                mail = self.env['mail.mail'].create({
                                    'subject': f'Mantenimiento programado para el {target_date}',
                                    'body_html': (
                                        f'<p>Estimado {tecnico.user_id.name},</p>'
                                        f'<p>Tienes un mantenimiento programado para el equipo <b>{equipo}</b> el día <b>{target_date}</b>.</p>'
                                        '<p>Por favor, prepara el equipo para su mantenimiento.</p>'
                                    ),
                                    'email_to': email_to,
                                    'email_cc': self.env.user.partner_id.email,
                                })
                                mail.send()
                                logger.info(
                                    f'Notificación enviada al técnico {tecnico.user_id.name} para el mantenimiento del equipo {equipo}.'
                                )
        except Exception as e:
            logger.error(f'Error en cron_notificar_mantenimientos: {e}')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('maintenodoo.mantenimiento') or 'New'
        return super().create(vals_list)

    @api.constrains('equipment_id')
    def _check_equipment_active(self):
        for record in self:
            if record.equipment_id.state == 'inactivo':
                raise ValidationError("No se puede crear mantenimiento para un equipo inactivo.")


class Tecnico(models.Model):
    _name = 'maintenodoo.tecnico'
    _description = 'Asignación de Técnicos'
    _rec_name = 'user_id'

    maintenance_id = fields.Many2one('maintenodoo.mantenimiento', string='Mantenimiento', ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Técnico', required=True)


class ResUserExtend(models.Model):
    _inherit = 'res.users'

    maintenance_ids = fields.Many2many(
        'maintenodoo.mantenimiento',
        string='Mantenimientos Asignados',
        relation='user_maintenance_rel',
        column1='user_id',
        column2='maintenance_id'
    )
