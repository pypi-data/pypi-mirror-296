from odoo.tests.common import SavepointCase
from odoo.addons.component.tests.common import ComponentMixin


class ComponentTransactionCase(SavepointCase, ComponentMixin):

    @classmethod
    def setUpClass(cls):
        super(ComponentTransactionCase, cls).setUpClass()
        cls.setUpComponent()

    def setUp(self):
        # resolve an inheritance issue (SavepointCase does not call super)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)

