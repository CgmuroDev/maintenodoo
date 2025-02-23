from odoo.tests.common import TransactionCase

class TestMantenimiento(TransactionCase):
    test_tags = ['standard', 'at_install', 'post_install']

    def setUp(self):
        super(TestMantenimiento, self).setUp()
        self.equipment_model = self.env['maintenodoo.equipment']
        self.mantenimiento_model = self.env['maintenodoo.mantenimiento']

    def test_create_equipment(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
            'installation_date': '2023-01-01',
            'state': 'activo',
        })
        self.assertEqual(equipment.name, 'Equipo de Prueba')
        self.assertEqual(equipment.category, 'electronic')
        self.assertEqual(equipment.state, 'activo')

    def test_create_mantenimiento(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
            'installation_date': '2023-01-01',
            'state': 'activo',
        })
        mantenimiento = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': '2023-02-01',
            'executed_date': '2023-02-02',
            'notes': 'Mantenimiento de prueba',
        })
        self.assertEqual(mantenimiento.equipment_id.id, equipment.id)
        self.assertEqual(mantenimiento.programed_date, '2023-02-01')
        self.assertEqual(mantenimiento.executed_date, '2023-02-02')
        self.assertEqual(mantenimiento.notes, 'Mantenimiento de prueba')

    def create_equipment_with_invalid_state_raises_error(self):
        with self.assertRaises(ValidationError):
            self.equipment_model.create({
                'name': 'Equipo de Prueba',
                'category': 'electronic',
                'state': 'reparacion',
            })

    def compute_indicator_result_behavior_graph_with_data(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        equipment._compute_indicator_result_behavior()
        self.assertTrue(equipment.indicator_result_behavior_graph)

    def compute_indicator_result_behavior_graph_without_data(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        self.env['maintenodoo.equipment'].search([]).unlink()
        equipment._compute_indicator_result_behavior()
        self.assertFalse(equipment.indicator_result_behavior_graph)

    def create_maintenance_with_default_name(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        maintenance = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': fields.Date.today(),
        })
        self.assertNotEqual(maintenance.name, 'New')

    def compute_validity(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        maintenance = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': fields.Date.today(),
            'executed_date': fields.Date.today() + timedelta(days=5),
        })
        self.assertEqual(maintenance.validity, 5)

    def inverse_validity(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        maintenance = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': fields.Date.today(),
        })
        maintenance.validity = 5
        self.assertEqual(maintenance.executed_date, fields.Date.today() + timedelta(days=5))

    def calculate_costo(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        maintenance = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': fields.Date.today(),
            'validity': 5,
        })
        self.assertEqual(maintenance.costo_por_diario, 250.0)

    def cron_notificar_mantenimientos(self):
        equipment = self.equipment_model.create({
            'name': 'Equipo de Prueba',
            'category': 'electronic',
        })
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'email': 'testuser@example.com',
        })
        maintenance = self.mantenimiento_model.create({
            'equipment_id': equipment.id,
            'programed_date': fields.Date.today() + timedelta(days=1),
        })
        self.env['maintenodoo.tecnico'].create({
            'maintenance_id': maintenance.id,
            'user_id': user.id,
        })
        self.mantenimiento_model.cron_notificar_mantenimientos()
        # Check logs or email sending logic here