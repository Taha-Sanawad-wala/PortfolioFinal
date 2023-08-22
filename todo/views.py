from django.http import HttpResponse
from django.shortcuts import render,redirect
from todo.models import TodoUser,TODO
from todo.forms import TODOForm
# Create your views here.
def home(request):
    if request.session.get('TodoUser'):
        id = request.session['id']
        form = TODOForm()
        todos = TODO.objects.filter(user=id)
        print(todos)
        return render(request , 'todo/index.html' , context={'form' : form , 'todos' : todos})
    else:
        return render(request,'todo/login.html')

def login(request):
    if request.method=='GET':
        request.session['TodoUser']=''
        return render(request,'todo/login.html')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if TodoUser.objects.filter(email=email,password=password):
            request.session['TodoUser']=list(TodoUser.objects.filter(email=email,password=password).values())[0]['name']
            request.session['id']=list(TodoUser.objects.filter(email=email,password=password).values())[0]['id']
            return redirect('home_todo')
        else:
            return render(request,'todo/login.html',{"error":"invalid Email or Password"})
    

def signup(request):
    if request.method=='GET':
        return render(request,'todo/signup.html')
    if request.method=='POST':
        name = request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if TodoUser.objects.filter(email=email):
            return render(request,'todo/signup.html',{"error":"email already exist try sign in using different mail.!!!"})
        else:
            user=TodoUser(name=name,email=email,password=password)
            user.save()
            return render(request,'todo/signup.html',{"success":"user registered try login!!!"})

def logout(request):
    request.session['TodoUser']=''
    return render(request,'todo/login.html')

def add_todo(request):
    if request.session.get('TodoUser'):
        name = request.session['TodoUser']
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            x=TodoUser.objects.get(name=name)
            data=form.cleaned_data
            todo = TODO(title=data['title'],status=data['status'],priority=data['priority'],user=x)
            todo.save()
            return redirect("home_todo")
        else: 
            return render(request , 'todo/index.html' , context={'form' : form})

def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home_todo')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home_todo')
