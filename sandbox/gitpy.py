#!/usr/bin/env python
'''
gitpy.py -- program to test out some gitpython api.
'''

from git import *
repo = Repo("/Users/pradeep/src/requests")
heads = repo.heads

commits = repo.iter_commits('master')
for commit in commits:
    print commit.author, commit.message
