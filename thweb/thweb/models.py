from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom)

#class Country(StructuredNode):
#    code = StringProperty(unique_index=True, required=True)
#
#    # traverse incoming IS_FROM relation, inflate to Person objects
#    inhabitant = RelationshipFrom('Person', 'IS_FROM')


#class Person(StructuredNode):
#    name = StringProperty(unique_index=True)
#    age = IntegerProperty(index=True, default=0)
#
#    # traverse outgoing IS_FROM relations, inflate to Country objects
#   country = RelationshipTo('Country', 'IS_FROM')

class Repository(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    url = StringProperty()


class Developer(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    email =  StringProperty()


class Commit(StructuredNode):
    hexsha = StringProperty(unique_index=True, required=True)
    message = StringProperty()
    ctime = IntegerProperty()
    parent = RelationshipTo('Commit', 'CHILD_OF')
    repo = RelationshipTo('Repository', 'BELONGS_TO')


class File(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    belongs_to = RelationshipTo('Directory', 'BELONGS_TO')


class Directory(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    has_a = RelationshipTo(['Directory', 'File'], 'HAS_A')
