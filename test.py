import unittest
import uuid

import adhara_ecs

class TestECS(unittest.TestCase):

    def test_create_assemblage(self):
        assemblage = adhara_ecs.create_assemblage({'ktest':'vtest'})

        self.assertIsInstance(assemblage, type(uuid.uuid4()))
        self.assertIn(assemblage, adhara_ecs.db.get_neighbors(adhara_ecs.assemblages))

    def test_create_component(self):
        assemblage = adhara_ecs.create_assemblage({'ktest':'vtest'})
        component = adhara_ecs.create_component(assemblage)

        self.assertIsInstance(component, type(uuid.uuid4()))
        self.assertIn(component, adhara_ecs.db.get_neighbors(adhara_ecs.components))

    def test_create_entity(self):
        assemblage = adhara_ecs.create_assemblage({'ktest':'vtest'})
        component = adhara_ecs.create_component(assemblage)
        component2 = adhara_ecs.create_component(assemblage)
        entity = adhara_ecs.create_entity([component, component2])

        self.assertIsInstance(entity, type(uuid.uuid4()))
        self.assertIn(entity, adhara_ecs.db.get_neighbors(adhara_ecs.entities))

    def test_add_system(self):
        def dummy_system(**kwargs):
            pass
        system = adhara_ecs.add_system(callable=dummy_system)

        self.assertIsInstance(system, type(uuid.uuid4()))
        self.assertIn(system, adhara_ecs.db.get_neighbors(adhara_ecs.rt_systems))


class TestBaseSystem(unittest.TestCase):

    def test_base_system(self):
        assemblage = adhara_ecs.create_assemblage({'ktest':'vtest'})
        component = adhara_ecs.create_component(assemblage)
        system = adhara_ecs.add_system(callable=adhara_ecs.BaseSystem())
        for s in adhara_ecs.db.get_neighbors(adhara_ecs.rt_systems):
            func = adhara_ecs.db.get_attributes(s)['callable']
            func(component=component)

        self.assertIsInstance(system, type(uuid.uuid4()))
        self.assertIn(system, adhara_ecs.db.get_neighbors(adhara_ecs.rt_systems))
