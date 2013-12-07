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
    repo = Repository.index.get(name=repo_name)
    return render(request, "repoview.html",
                  {'title': 'Repository view for %s' % (repo_name, ),
                   'repo_name': repo_name,
                   'last_n_commits': repo.last_n_commits(10),
                   'total_commits': repo.total_commits(),
                   'total_committers': repo.total_committers(),
                   'oldest_committer': repo.oldest_committer,
                   })

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

def commitvol(request, repo_name):
    repo_obj = Repository.index.get(name=repo_name)
    data = repo_obj.most_commits_by_n_users(5)
    return render(request, "commitvol.html", 
            {'data_header': 'Developer,Commits',
            'data': data} )

def langpop(request, repo_name):
    repo_obj = Repository.index.get(name=repo_name)
    data = repo_obj.langpopularity()
    return render(request, "commitvol.html", 
            {'data_header': 'Developer,Commits',
            'data': data})

def langpopdata(request, repo_name):
    repo_obj = Repository.index.get(name=repo_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="commits.csv"'
    writer = csv.writer(response)
    writer.writerow(['Language','Files'])
    data, metadata = repo_obj.langpopularity()
    for d in data:
        writer.writerow([d[0], d[1]])
    return response
