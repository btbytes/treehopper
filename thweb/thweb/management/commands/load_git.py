from django.core.management.base import BaseCommand, CommandError
from thweb.models import Repository, Commit, Developer, File, Directory
from optparse import make_option
from git import Repo
from string import strip
import sys

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


            for commit in commits:
                nc = Commit(hexsha=commit.hexsha,
                    message=unicode(strip(commit.message)),
                    ctime=commit.committed_date,                    
                    )
                nc.save()
                nc.repo.connect(new_repo)
                nc.save()                
                count += 1
            self.stdout.write('total commits: %d '  % (count, ))