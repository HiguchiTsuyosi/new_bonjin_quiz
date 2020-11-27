from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import Question,Question_normal,Question_hard,User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import urlencode

from .forms import QuestionForm,DeleteForm
from django.views.decorators.http import require_GET,require_POST

from django.db.models import Max

# Create your views here.

def top(request):
    return render(request,'top.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username_data']
        email=request.POST['email_data']
        password=request.POST['password_data']
        #バリデーションチェックはここで行う
        try:
            User.objects.create_user(username,email,password)
        except IntegrityError:
            return render(request,'signup.html',{'error':'このユーザー名は既に登録されています。'})
    else:
        return render(request,'signup.html',{})

    return redirect('signup_success')

def signup_success(request):
    return render(request,'signup_success.html')


def loginview(request):
    if request.method=='GET':
        if request.GET.get('error'):
            return render(request,'login.html',{'error':'このユーザーは登録されていません。'})
    if request.method=='POST':
        username=request.POST['username_data']
        password=request.POST['password_data']
        print(username)
        print(password)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            redirect_url=reverse('loginview')
            parameter=urlencode({'error':'1'})
            url=f'{redirect_url}?{parameter}'
            #return render(request,'login.html',{'error':'このユーザーは登録されていません。'})
            return redirect(url)
    return render(request,'login.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('top')
    if 'ques_num' in request.session:
        request.session['ques_num']=0

    if 'ans_num' in request.session:
        request.session['ans_num']=0

    print(request.user)
    return render(request,'home.html')


def quiz_start(request,level):
    if level==1:
        request.session['level']=1
    elif level==2:
        request.session['level']=2
    elif level==3:
        request.session['level']=3
    else:
        return redirect('home')
    return render(request,'quiz_start.html')  



def level_choice(request):
    userdata=User.objects.get(username=request.user)
    return render(request,'level_choice.html',{'userdata':userdata})


def question(request):
    if not request.user.is_authenticated:
        return redirect('top')
    #現在の出題数
    if 'ques_num' in request.session:
        request.session['ques_num']+=1
    else:
        request.session['ques_num']=1
    #正解数
    if not 'ans_num' in request.session:
        request.session['ans_num']=0
    
    print(request.session['ques_num'])
    print(request.session['ans_num'])
    ans_num=request.session['ans_num']

    if request.session['level']==1:
        question=Question.objects.get(pk=request.session['ques_num'])
    elif request.session['level']==2:
        question=Question_normal.objects.get(pk=request.session['ques_num'])
    elif request.session['level']==3:
        question=Question_hard.objects.get(pk=request.session['ques_num'])
    else:
        redirect('home')


    return render(request,'question.html',{'question':question,'ans_num':ans_num})

def answer(request,ans):
    #ログインしていなかったらトップ画面へ
    if not request.user.is_authenticated:
        return redirect('top')
    #現在の問題
    if request.session['level']==1:
        answer=Question.objects.get(pk=request.session['ques_num'])
    elif request.session['level']==2:
        answer=Question_normal.objects.get(pk=request.session['ques_num'])
    elif request.session['level']==3:
        answer=Question_hard.objects.get(pk=request.session['ques_num'])
    else:
        redirect('home')

    #現在の正解数
    if answer.answer==ans:
        request.session['ans_num']+=1
    ans_num=request.session['ans_num']

    #レコード数を格納 
    if request.session['level']==1:
        record_num=Question.objects.all().count()
    elif request.session['level']==2:
        record_num=Question_normal.objects.all().count()
    elif request.session['level']==3:
        record_num=Question_hard.objects.all().count()
    else:
        redirect('home')

    #最終問題かチェック
    if request.session['ques_num']==record_num:
        return render(request,'answer.html',{'answer':answer,'ans_num':ans_num,'flg':1})

    return render(request,'answer.html',{'answer':answer,'ans_num':ans_num,'flg':0})

def result(request):
    ans_num=request.session['ans_num']
    
    userdata=User.objects.get(username=request.user)
    #最高記録更新なら正解数をDBに保存
    if request.session['level']==1:
        if userdata.easy_point < ans_num:
            userdata.easy_point=ans_num
            userdata.save()
            request.session['ans_num']=0
            request.session['ques_num']=0
            return render(request,'result.html',{'ans_num':ans_num,'flg':1})
    elif request.session['level']==2:
        if userdata.normal_point < ans_num:
            userdata.normal_point=ans_num
            userdata.save()
            request.session['ans_num']=0
            request.session['ques_num']=0
            return render(request,'result.html',{'ans_num':ans_num,'flg':1})
    elif request.session['level']==3:
        if userdata.hard_point < ans_num:
            userdata.hard_point=ans_num
            userdata.save()
            request.session['ans_num']=0
            request.session['ques_num']=0
            return render(request,'result.html',{'ans_num':ans_num,'flg':1})
    else:
        redirect('home')
    
    request.session['ans_num']=0
    request.session['ques_num']=0
    return render(request,'result.html',{'ans_num':ans_num,'flg':0})

def logoutview(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request,'logout_success.html')



def user_data(request):
    userdata=User.objects.get(username=request.user)
    return render(request,'userdata.html',{'userdata':userdata})

def ranking(request):
    alluser_easy=User.objects.all().order_by('-easy_point')
    alluser_normal=User.objects.all().order_by('-normal_point')
    alluser_hard=User.objects.all().order_by('-hard_point')
    print(alluser_easy)
    return render(request,'ranking.html',{'alluser_easy':alluser_easy,'alluser_normal':alluser_normal,'alluser_hard':alluser_hard})


def dbms(request):
    return render(request,'dbms.html')

def question_form(request):
    questions=Question.objects.all().order_by('id')
    form=QuestionForm()
    print(form)
    return render(request,'question_form.html',{'form':form,'questions':questions})

#POSTでのみ実行される関数
@require_POST
def question_form_success(request):
    #POSTデータを紐づけ
    form=QuestionForm(request.POST)
    print(form)
    #入力値を検証
    if form.is_valid():
        #newQuestion=Question()
        #print(newQuestion)
        print(form.cleaned_data)
        question_add=Question(
            id=form.cleaned_data['id'],
            question=form.cleaned_data['question'],
            answer=form.cleaned_data['answer'],
            comment=form.cleaned_data['comment'])
        print(question_add)
        question_add.save()
        return render(request,'form_success.html',{'form':form})
    else:
        questions=Question.objects.all().order_by('id')
        form=QuestionForm()
        return render(request,'question_form.html',{'form':form,'questions':questions,'error':1})

def question_delete_form(request):
    questions=Question.objects.all().order_by('id')
    form=DeleteForm()
    return render(request,'question_delete_form.html',{'form':form,'questions':questions})

@require_POST
def delete_success(request):
    #POSTデータを紐づけ
    form=DeleteForm(request.POST)
    #入力値を検証
    if form.is_valid():
        key=form.cleaned_data['id']
        print(key)
        delete_question=Question.objects.get(pk=key)
        question=Question.objects.get(pk=key)
        question.delete()
        return render(request,'delete_success.html',{'delete_question':delete_question})
    else:
        questions=Question.objects.all().order_by('id')
        form=DeleteForm()
        return render(request,'question_delete_form.html',{'form':form,'questions':questions,'error':1})


def user_delete_form(request):
    users=User.objects.all().order_by('id')
    form=DeleteForm()
    return render(request,'user_delete_form.html',{'form':form,'users':users})

@require_POST
def user_delete_success(request):
    #POSTデータを紐づけ
    form=DeleteForm(request.POST)
    #入力値を検証
    if form.is_valid():
        key=form.cleaned_data['id']
        delete_user=User.objects.get(pk=key)
        users=User.objects.get(pk=key)
        users.delete()
        return render(request,'user_delete_success.html',{'delete_user':delete_user})
    else:
        users=User.objects.all().order_by('id')
        form=DeleteForm()
        return render(request,'user_delete_form.html',{'form':form,'users':users,'error':1})

