from django.shortcuts import render
from app.models import Github,ContactMe
# Create your views here.
def index(request):
    d=Github.objects.all()
    if request.method=="POST":
        if request.POST.get('name')!="" and request.POST.get('email')!="" and request.POST.get('number')!="" and request.POST.get('message')!="": 
            cm=ContactMe(name=request.POST.get('name'),email=request.POST.get('email'),number=request.POST.get('number'),message=request.POST.get('message'))
            cm.save()
            data={"data":d}
            return render(request,"portfolio.html",data)
        else:
            data={"data":d}
            return render(request,"portfolio.html",data)

    else:
        data={"data":d}
        return render(request,"portfolio.html",data)
