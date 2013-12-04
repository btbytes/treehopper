'''
embd.py

use Neo4J's embedded database interface
needs JPype - https://github.com/originell/jpype/releases
'''
from neo4j import GraphDatabase, INCOMING, Evaluation


class Treehopper(object):
    def __init__(self, dblocn="/Users/pradeep/tmp/gdb"):
        self.db = GraphDatabase(dblocn)
        # Create a database
        db = GraphDatabase("/Users/pradeep/tmp/gdb")


        def _create_domain_objects(self):
            "Create Domain Objects only once in the lifecycle of a repository"
            repositories = db.node()
            commits = db.node()
            developers = db.node()
            files = db.node()
            directories = db.node()
            tags = db.node()

        def _create_indexes(self):
            "Create indexes only once in the lifecycle of a repository."
            repositories_idx = create_index('repositories')
            commits_idx = create_index('commits')
            developers_idx = create_index('developers')
            files_idx = create_index('files')
            directories_idx = create_index('directories')
            tags_idx = create_index('tags')


        def create_index(self, dobj_name):
            return db.node.indexes.create(dobj_name)

        def create_domain_object(self, domain_object, name):
            with db.transaction:
                obj = db.node(name=name)
                obj.INSTANCE_OF(domain_object)
                #index the object by name attr
                #repositories_idx =  create_index('repositories')

        def get_object(self, obj):
            #return obj_idx['name'][name].single
            pass

        def get_some_query(self, param1, param2):
            # return query results
            # example...
            return db.query('''
            START customer=node({customer_id})
            MATCH invoice-[:SENT_TO]->customer
            WHERE has(invoice.amount) and invoice.amount >= {min_sum}
            RETURN invoice''',
            customer_id = customer.id, min_sum = min_sum)['invoice']

        def shutdown():
            db.shutdown()

def main():
    th = Treehopper()
    #run once
    th._create_domain_objects()
    th._create_indexes()
    #~run once
    th.shutdown()
