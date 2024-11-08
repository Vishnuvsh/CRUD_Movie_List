from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import MovieInfo
from .forms import MovieForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def create(request):
    if request.POST:
        frm=MovieForm(request.POST)
        if frm.is_valid():
            frm.save()
    else:
        frm=MovieForm()
    return render(request,'create.html',{'frm':frm})

def list(request):
    recent_visits=request.session.get('recent_visits',[])
    count=request.session.get('count',0)
    count=int(count)
    count=count+1
    request.session['count']=count
    recent_movie_set=MovieInfo.objects.filter(pk__in=recent_visits)
    movie=MovieInfo.objects.all()
    print(movie)
    response=render(request,'list.html',{'movies':movie, 'visits':count, 'recent_movies':recent_movie_set})
    return response


def edit(request,pk):
    instanceedit=MovieInfo.objects.get(pk=pk)
    if request.POST:
        frm=MovieForm(request.POST,instance=instanceedit)
        if frm.is_valid():
            instanceedit.save()
    else:
        recent_visits=request.session.get('recent_visits',[])
        recent_visits.insert(0,pk)
        request.session['recent_visits']=recent_visits
        
        frm=MovieForm(instance=instanceedit)
    return render(request,'create.html',{'frm':frm})

def delete(request,pk):
    instance=MovieInfo.objects.get(pk=pk)
    instance.delete()
    movie=MovieInfo.objects.all()
    return redirect('list')