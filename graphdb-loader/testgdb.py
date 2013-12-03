'''
testgdb.py

Script to test out various operations on a
Neo4J graph database.

'''

import sys

from string import strip
from py2neo import neo4j, node, rel
from py2neo.calendar import GregorianCalendar


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    time_index = graph_db.get_or_create_index(neo4j.Node, "TIME")
    calendar = GregorianCalendar(time_index)
    graph_db.create(
            {"name": "Alice"},
            (0, "BORN", calendar.day(1800, 1, 1)),
            (0, "DIED", calendar.day(1900, 12, 31)),
    )

if __name__ == '__main__':
    main()
