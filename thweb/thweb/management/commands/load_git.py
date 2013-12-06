from django.core.management.base import BaseCommand, CommandError
from thweb.models import Repository, Commit, Actor, File, SourceType
from optparse import make_option
from git import Repo
from string import strip,lower, upper
import sys
import os
from datetime import datetime
from neomodel.exception import DoesNotExist
import logging

logging.basicConfig()

def dt(u): return datetime.utcfromtimestamp(u)

file_type = {
    '.py': 'Python',
    '.html': 'HTML',
    '.css': 'CSS',
    '.c': 'C/C++',
    '.cpp': 'C/C++',
    '.h': 'C/C++',
    '.hpp': 'C/C++',
    '.js': 'Javascript',
    '.js': 'Javascript',
    '.txt': 'Text',
    '.md': 'Text',
    '.rst': 'Text',
    '.rmd': 'Text',
    '.hs': 'Haskell',
    '.cabal': 'Cabal'
}


def get_sourcetype(fpath):
    basename = os.path.basename(fpath)
    ext = lower(os.path.splitext(fpath)[1])
    if ext in file_type.keys():
        return file_type[ext]
    else:
        if len(ext) > 1:
            return upper(ext.replace('.',''))
    return 'General'


class Command(BaseCommand):
    args = "<option>"
    help = "import a git repository into Treehopper"

    option_list = BaseCommand.option_list + (
        make_option('--url',
            action='store',
            dest='url',
            help='Repository URL.'),
        make_option('--name',
            action='store',
            dest='name',
            help='Repository name.'),
        )

    def handle(self, *args, **options):
        if not options['url']:
            self.stdout.write('load_git was not given a repo location')
            sys.exit(0)
        else:
            self.stdout.write('load_git called with repo location: %s' % (options['url'], ))
            repo = Repo(options['url'])
            if not options['name']:
                name = options['url'].split('/')[-1]
            else:
                name = options['name']

            self.stdout.write('load_git called with name: %s' % (name, ))
            #create the repository
            new_repo = Repository(name=name, url=options['url'])
            new_repo.save()
            heads = repo.heads
            commits = repo.iter_commits('master')
            count = 0

            # first pass

            prev_commit = None
            for commit in commits:
                date_ = dt(commit.committed_date).strftime("%Y-%m-%d")
                nc = Commit(hexsha=commit.hexsha,
                            message=unicode(strip(commit.message)),
                            summary=unicode(strip(commit.summary)),
                            ctime=dt(commit.committed_date),
                            date=date_,
                    )
                nc.save()
                nc.repo.connect(new_repo)
                nc.save()
                # associate with the committer
                try:
                    ccommitter_name = unicode(commit.committer.name).encode('ascii', 'ignore')
                    ccommitter_email = commit.committer.email
                    #print 'Querying committer: %s' % (ccommitter, )
                    committer = Actor.index.get(name=ccommitter_name)
                    nc.committer.connect(committer)
                    nc.save()
                except DoesNotExist, e:
                    #print '%s does not exist in db' %(ccommitter,)
                    committer = Actor(name=ccommitter_name, email=ccommitter_email)
                    committer.save()
                    committer.refresh()
                    nc.committer.connect(committer)
                    nc.save()

                # account for the files modified in this commit
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
                for cf in changed_files:
                    print '\t\t', cf
                    try:
                        
                        f = File.index.get(path=cf)
                        stname = get_sourcetype(cf)
                        f.save()
                        f.refresh()
                        try:
                            st = SourceType.index.get(name=stname)
                            f.sourcetype.connect(st)                            
                        except:
                            st = SourceType(name=stname)
                            st.save()
                            f.sourcetype.connect(st)
                        f.save()
                        f.commit.connect(nc)
                        f.save()
                    except DoesNotExist, e:
                        f = File(path=cf)
                        f.save()
                        f.refresh()
                        f.commit.connect(nc)
                        f.save()
                # one commit handled.    
                count += 1
            self.stdout.write('First pass - total commits: %d '  % (count, ))

            # second pass
            commits = repo.iter_commits('master')
            count = 0
            for commit in commits:
                nc = Commit.index.get(hexsha=commit.hexsha)
                for parent in commit.parents:
                    try:
                        pc = Commit.index.get(hexsha=parent.hexsha)
                        nc.parent.connect(pc)
                        nc.save()
                        count += 1
                    except:
                        self.stdout.write('Could not find parent(%s) of (%s)' % (parent.hexsha, commit.hexsha))
            self.stdout.write('Second pass - total commits: %d' % (count, ))
