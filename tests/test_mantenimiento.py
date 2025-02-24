from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install')
class TestEquipment(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Equipment = self.env['maintenodoo.equipment']
        self.user = self.env.ref('base.user_admin')


        self.equipment1 = self.Equipment.create({
            'name': 'Equipo Test 1',
            'category': 'electronic',
            'installation_date': date.today(),
            'state': 'activo'
        })

    def test_equipment_creation(self):

        self.assertEqual(self.equipment1.state, 'activo')
        self.assertEqual(self.equipment1.category, 'electronic')

    def test_state_constraint(self):

        with self.assertRaises(ValidationError):
            self.equipment1.write({'state': 'reparacion'})

    def test_compute_indicator_graph(self):

        self.equipment1._compute_indicator_result_behavior()
        self.assertTrue(self.equipment1.indicator_result_behavior_graph)


@tagged('post_install', '-at_install')
class TestMaintenance(TransactionCase):
    def setUp(self):
        super().setUp()

        self.Maintenance = self.env['maintenodoo.mantenimiento']
        self.Equipment = self.env['maintenodoo.equipment']
        self.user = self.env.ref('base.user_admin')


        self.equipment = self.Equipment.create({
            'name': 'Equipo Test',
            'category': 'mechanical',
            'installation_date': date.today(),
            'state': 'activo'
        })

    def test_maintenance_creation(self):

        maintenance = self.Maintenance.create({
            'equipment_id': self.equipment.id,
            'programed_date': date.today() + timedelta(days=1)
        })

        self.assertEqual(maintenance.validity, 0)
        self.assertTrue(maintenance.name != 'New')

    def test_validity_calculation(self):

        maintenance = self.Maintenance.create({
            'equipment_id': self.equipment.id,
            'programed_date': date(2024, 1, 1),
            'executed_date': date(2024, 1, 5)
        })

        self.assertEqual(maintenance.validity, 4)

    def test_cost_calculation(self):

        maintenance = self.Maintenance.create({
            'equipment_id': self.equipment.id,
            'programed_date': date.today(),
            'executed_date': date.today() + timedelta(days=5),
            'costo_por_dia': 100.0
        })

        self.assertEqual(maintenance.costo_por_diario, 500.0)

    def test_inactive_equipment_constraint(self):

        self.equipment.write({'state': 'inactivo'})

        with self.assertRaises(ValidationError):
            self.Maintenance.create({
                'equipment_id': self.equipment.id,
                'programed_date': date.today()
            })

    def test_cron_notification(self):

        maintenance = self.Maintenance.create({
            'equipment_id': self.equipment.id,
            'programed_date': date.today() + timedelta(days=1)
        })


        self.Maintenance.cron_notificar_mantenimientos()


        emails = self.env['mail.mail'].search([
            ('subject', 'ilike', 'Mantenimiento programado')
        ])

        self.assertTrue(len(emails) > 0)


@tagged('post_install', '-at_install')
class TestTechnician(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Technician = self.env['maintenodoo.tecnico']
        self.user = self.env.ref('base.user_demo')

    def test_technician_creation(self):

        technician = self.Technician.create({
            'user_id': self.user.id
        })

        self.assertEqual(technician.user_id, self.user)
