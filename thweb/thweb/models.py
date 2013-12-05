from datetime import datetime
import pytz
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty,
                      RelationshipTo, RelationshipFrom)

class Repository(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    url = StringProperty()
    imported = DateTimeProperty(default=lambda: datetime.now(pytz.utc))

    def last_n_commits(self, n):
        "return the last `n` commits in this repo"
        results = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[:COMMITTED_BY]-(commit)-[:BELONGS_TO]->(myrepo)
WITH commit, committer
RETURN commit.summary AS summary, commit.ctime as ctime, committer.name as committer
ORDER BY (commit.ctime) DESC
        LIMIT 10;""")
        return results


class Actor(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    email =  StringProperty()


class Commit(StructuredNode):
    hexsha = StringProperty(unique_index=True, required=True)
    message = StringProperty()
    summary = StringProperty()
    ctime = DateTimeProperty()
    parent = RelationshipTo('Commit', 'CHILD_OF')
    repo = RelationshipTo('Repository', 'BELONGS_TO')
    committer = RelationshipTo('Actor', 'COMMITTED_BY')


class File(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    belongs_to = RelationshipTo('Directory', 'BELONGS_TO')


class Directory(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    has_a = RelationshipTo(['Directory', 'File'], 'HAS_A')
