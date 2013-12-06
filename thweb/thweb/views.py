from django.shortcuts import render
from django.http import HttpResponse
from models import Repository
import csv
from datetime import datetime

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
    total_commits = repo_obj.total_commits()
    return render(request, "repoview.html",
                  {'title': 'Repository view for %s' % (repo_name, ),
                   'repo_name': repo_name,
                   'last_n_commits': last_n_commits,
                   'total_commits': total_commits}
                   )

def user(request):
    ctx = {'title': "User",
        }
    return render(request, "user.html", ctx)


def caldata(request, repo_name, year):
    repo_obj = Repository.index.get(name=repo_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="commits.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date','Commits'])
    data, metadata = repo_obj.commit_counts_by_day_for_year(year)
    for d in data:
        writer.writerow([d[0], d[1]])
    return response


def calview(request, repo_name):
    cur_year = datetime.now().year
    return render(request, "calview.html",
                  {"st_year": cur_year,
                   "end_year": cur_year+1,
                   "cur_year": cur_year,
                   "repo_name": repo_name
                   })
