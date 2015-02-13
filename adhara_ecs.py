from adhara_db import Graph

db = Graph()
assemblages = db.add_node() #all assemblages link to this
components = db.add_node() #all components link to this
entities = db.add_node() #all entities link to this
rt_systems = db.add_node() #all real time systems link to this

def create_assemblage(attributes=None):
    '''
    A function to create an assemblage, or blueprint for componenets
    attributes is a dict of attributes for the assemblage
    '''
    if not attributes:
        attributes = {}

    node = db.add_node(attributes)
    db.add_edge(node, assemblages)

    return node


def create_component(assemblage):
    '''
    A function to create a component from an assemblage
    assemblage is a node (typically an assemblage or a component)
    that acts as a blueprint for this component
    component attributes start as a shallow copy of the assemblages attributes
    '''
    node = db.add_node()
    db.add_edge(node, components)
    attributes = db.get_attributes(assemblage).copy()
    db.add_attributes(node, **attributes)
    try:
        for s in attributes['systems']:
            db.add_edge(node, s)

    except KeyError:
        pass

    return node


def create_entity(assemblages=None, components=None):
    '''
    A function to create and entity from a list of components or assemblages
    components is an optional list of components
    assemblages is an optional list of assemblages,
    from which components will be constructed
    '''

    if not components:
        components = []


    node = db.add_node()
    db.add_edge(node, entities)

    if assemblages:
        for a in assemblages:
            components.append(create_component(a))

    for c in components:
        db.add_edge(node, c)

    return node


def add_system(callable, sys_type=rt_systems, **kwargs):
    '''
    A function to add a system to the ECS
    callable is the default called when the system should be ran
    callable should accept arbitrary kwargs (**kwargs) as a paremeter,
    so that the system call interface can change in the future
    sys_type is the uuid of the system type, default is rt_system
    kwargs are attributes of the system
    '''
    kwargs['callable'] = callable
    node = db.add_node(kwargs)
    db.add_edge(node, sys_type)

    return node


class BaseSystem():
    '''
    A base class that implements the basic methods of a class based system
    '''

    def __call__(self, **kwargs):
        '''
        When the system is called, we do call self.run_system for every component
        that is attached to this system
        '''
        self.run_system(kwargs['component'])

    def run_system(self, component):
        '''
        This function should do somthing for/with the component passed to it
        '''
        pass
