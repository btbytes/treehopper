#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
gitpy.py -- program to test out some gitpython api.
'''

import sys

from git import Repo
from git.diff import Diff
from string import strip
from py2neo import neo4j, node, rel

#import codecs
# UTF8Writer = codecs.getwriter('utf8')
# sys.stdout = UTF8Writer(sys.stdout)

repo = Repo("/Users/pradeep/src/hakyll")


heads = repo.heads
commits = repo.iter_commits('master')
count = 0


for commit in commits:
    nc = {'hexsha': commit.hexsha,
          'message': unicode(strip(commit.message)),
          'committed_date': commit.committed_date,
          'message': unicode(commit.message)
      }
    #graph_db.create(nc)
    print 'commit: %s' % (commit.hexsha, )
    #for parent in commit.parents:
    #    print '\t%s' % (parent.hexsha, )
    print '\ttree: ', commit.tree
    for t in commit.tree.blobs:
        print '\t\t',t, t.mime_type, t.abspath, t.name, t.path, t.size
        #print dir(t)
        #diff = Diff(commit, t)
        #print '\t\t\t', diff
    #print 'Authored Tree: ', commit.authored_tree
    #print unicode(commit.author)
    count += 1

print 'Number of commits in the master: ', count
