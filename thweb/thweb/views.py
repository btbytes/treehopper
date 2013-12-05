from django.shortcuts import render
from models import Repository

def home(request):

    repositories = [{'name': 'requests'}]
    repos = Repository.category().instance.all()
    return render(request, "home.html",
        {'title': 'Home',
         'repositories': repos
     })


def repoview(request, repo_name):
    repo_obj = Repository.index.get(name=repo_name)
    last_n_commits = repo_obj.last_n_commits(10)
    print 'LAST N COMMITS ', last_n_commits
    return render(request, "repoview.html",
                  {'title': 'Repository view for %s' % (repo_name, ),
                   'repo_name': repo_name,
                   'last_n_commits': last_n_commits,
                   'ndays': range(1,32),
                   'nmonths': range(1,13),
                   'nhours': range(1,25) })

def user(request):
    ctx = {'title': "User",
        }
    return render(request, "user.html", ctx)
