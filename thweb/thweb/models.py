from datetime import datetime
import pytz
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      DateTimeProperty,
                      RelationshipTo, RelationshipFrom)

class Repository(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    url = StringProperty()
    imported = DateTimeProperty(default=lambda: datetime.now(pytz.utc))

    def total_committers(self):
        "return the total number of commiters in this repository"
        committers, md = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[:COMMITTED_BY]-(commit)-[:BELONGS_TO]->myrepo
WITH commit, committer
WHERE HAS(commit.hexsha)
RETURN count(DISTINCT committer.name)
""")

        return committers[0][0]

    def total_commits(self):
        "return the total number of commits in the repo"
        commits, md = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[:COMMITTED_BY]-(commit)-[:BELONGS_TO]->myrepo
WITH commit
WHERE HAS(commit.hexsha)
RETURN count(commit) as total_commits
""")
        return commits[0][0]



    def last_n_commits(self, n=10):
        "return the last `n` commits in this repo"
        results = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[:COMMITTED_BY]-(commit)-[:BELONGS_TO]->(myrepo)
WITH commit, committer
RETURN commit.summary AS summary, commit.date as date, committer.name as committer
ORDER BY (commit.ctime) DESC
        LIMIT 10;""")
        return results


    def last_n_tags(self, n=5):
        "return the last `n` tags in this repo"
        results = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[:COMMITTED_BY]- (commit)<-[:BELONGS_TO]->myrepo
WHERE HAS(commit.tag)
with commit, committer
RETURN commit.tag as release, commit.date as date, committer.name as committer
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
        "Return commit_counts_by_day_for_year"
        pattern = '%s-.*' % (year, )
        results = self.cypher("""START myrepo=node({self})
MATCH (c)-[:BELONGS_TO]->(myrepo)
WITH c as c, '%s' as pat
WHERE c.date =~ pat
return c.date as date, count(c) as count""" % (pattern, ))
        return results

    def most_commits_by_n_users(self, n=5):
        "return the total commits by n most active users"
        results = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[COMMITTED_BY]-(commit)-[:BELONGS_TO]->myrepo
with commit, committer
WHERE HAS(committer.name)
RETURN DISTINCT committer.name, COUNT(commit)
ORDER BY COUNT(commit) DESC
LIMIT %d
""" % (n, ))
        return results[0]

    def oldest_committer(self):
        "return the name of the developer who has worked the longest"
        results = self.cypher("""START myrepo=node({self})
MATCH (committer)<-[COMMITTED_BY]-(commit)-[:BELONGS_TO]->myrepo
WITH committer, commit
RETURN committer.name, commit.date
ORDER BY commit.ctime
LIMIT 1
""")
        return results[0][0]

    def langpopularity(self):
        "return the number of files of all source file types"
        results = self.cypher("""START myrepo=node({self})
MATCH (a)-[:IS_A]->(b)
WITH a,b
WHERE HAS(a.path)
RETURN DISTINCT b.name, count(b)
ORDER BY count(b) DESC
""")
        return results[0]

class Actor(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    email =  StringProperty()


class Commit(StructuredNode):
    hexsha = StringProperty(unique_index=True, required=True)
    message = StringProperty()
    summary = StringProperty()
    ctime = DateTimeProperty()
    date = StringProperty()
    tag = StringProperty()
    parent = RelationshipTo('Commit', 'CHILD_OF')
    repo = RelationshipTo('Repository', 'BELONGS_TO')
    committer = RelationshipTo('Actor', 'COMMITTED_BY')


class SourceType(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class File(StructuredNode):
    path = StringProperty(unique_index=True, required=True)
    commit = RelationshipTo('Commit', 'MODIFIED_BY')
    sourcetype = RelationshipTo('SourceType', 'IS_A')

#class Directory(StructuredNode):
#    path = StringProperty(unique_index=True, required=True)
#    has_a = RelationshipTo(['Directory', 'File'], 'HAS_A')
