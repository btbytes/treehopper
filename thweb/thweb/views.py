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
    return render(request, "repoview.html",
                  {'title': 'Repository view for %s' % (repo_name, ),
                   'repo_name': repo_name,
                   'ndays': range(1,32),
                   'nmonths': range(1,13),
                   'nhours': range(1,25) })

def user(request):
    ctx = {'title': "User",
        }
    return render(request, "user.html", ctx)
