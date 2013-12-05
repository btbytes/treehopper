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


    def earliest_commit_date(self):
        "return the earliest commit date for this repo"
        return self.cypher("""START myrepo=node({self})
MATCH(commit)
WITH commit
WHERE HAS(commit.date)
RETURN commit.date as date
ORDER BY commit.ctime
LIMIT 1
""")

    def last_commit_date(self):
        "return the last commit date for this repo"
        return self.cypher("""START myrepo=node({self})
MATCH(commit)
WITH commit
WHERE HAS(commit.date)
RETURN commit.date as date
ORDER BY commit.ctime DESC
LIMIT 1
""")

    def commits_on_day(self, dt):
        "return the total number of commits on a given date"
        return self.cypher("""START myrepo=node({self})
MATCH(timeline:Timeline), (y:Year)
WHERE y.year=2012
CREATE (timeline)-[r:YEAR]->(y)
return r;""")


    def commit_counts_by_day_for_year(self, year):
        print "commit_counts_by_day_for_year -- %s" % (year, )
        pattern = '%s-.*' % (year, )
        results = self.cypher("""START myrepo=node({self})
MATCH (c)
WITH c as c, '%s' as pat
WHERE c.date =~ pat
return c.date as date, count(c) as count""" % (pattern, ))
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
    date = IntegerProperty()

class File(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    belongs_to = RelationshipTo('Directory', 'BELONGS_TO')


class Directory(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    has_a = RelationshipTo(['Directory', 'File'], 'HAS_A')
