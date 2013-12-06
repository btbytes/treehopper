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
limit = 0
prev_commit = None
for commit in commits:
    limit +=1 
    nc = {'hexsha': commit.hexsha,
          'message': unicode(strip(commit.message)),
          'committed_date': commit.committed_date,
          'message': unicode(commit.message)
      }
    #graph_db.create(nc)
    print 'commit: %s' % (commit.hexsha, )
    changed_files = []
    for x in commit.diff(prev_commit):
        try:
            if x.a_blob.path not in changed_files:
                changed_files.append(x.a_blob.path)
        except:
            pass

        try:
            if x.b_blob is not None and x.b_blob.path not in changed_files:
                changed_files.append(x.b_blob.path)
        except:
            pass
    prev_commit = commit
    count += 1
    print '\t changed files: '
    for cf in changed_files:
        print '\t\t', cf

    if limit > 10:
        print 'done...'
        sys.exit(0)
print 'Number of commits in the master: ', count
