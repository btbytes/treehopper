from datetime import datetime
import pytz
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty,
                      RelationshipTo, RelationshipFrom)

class Repository(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    url = StringProperty()
    imported = DateTimeProperty(default=lambda: datetime.now(pytz.utc))


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
