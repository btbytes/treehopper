from django.shortcuts import render

def home(request):
	return render(request, "home.html", 
		{'title': 'Home',
		 'ndays': range(1,32), 
		 'nmonths': range(1,13), 
		 'nhours': range(1,25) })

def user(request):
	ctx = {'title': "User",
		}
	return render(request, "user.html", ctx)
