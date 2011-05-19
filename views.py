# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django import conf
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.db.models import Q
from django import forms
import datetime
from common import validate_mobileno
from zy.models import *
from settings import TEST_HOST

def index(request):
    host = request.get_host()
    settings = conf.settings
    section = 'index'
    page_title = '首页'
    jsfiles = ['box', 'jquery.cookie', 'index']
    anss = Answer.objects.filter(father__publicall=1, selected=True).order_by('-time')[:6]
    ss = Senior.objects.filter(type='C').order_by('-gyear', '?')
    return render_to_response('index.html', locals())

def special(request):
    settings = conf.settings
    section = 'special'
    page_title = '专题'
    jsfiles = ['box', 'jquery.sort', 'special']

    ss = Senior.objects.filter(type='C').order_by('-gyear', '?')

    us = list(University.objects.all())
    us = filter(lambda x: x.qcount() + x.ccount() > 0, us)
    us.sort(key=(lambda x: x.pinyin))
    for index, u in enumerate(us):
        u.order_name = index
    us.sort(key=(lambda x: x.qcount() + x.ccount()), reverse=True)
    for index, u in enumerate(us):
        u.order_count = index
    for u in us[7:]:
        u.other = True

    ts = list(Tag.objects.all())
    ts.sort(key=(lambda x: x.qcount() + x.ccount()), reverse=True)
    for t in ts[12:]:
        t.other = True

    return render_to_response('special.html', locals())

def senior(request):
    settings = conf.settings
    section = 'senior'
    page_title = '学长们'
    jsfiles = ['senior']
    fss = Senior.objects.filter(type='C').order_by('-gyear', '?')
    oss = list(Senior.objects.filter(gyear=2010).exclude(type='C'))
    oss.sort(key=(lambda x: x.count()), reverse=True)
    pss = list(Senior.objects.exclude(gyear=0).exclude(gyear=2010).exclude(type='C'))
    pss.sort(key=(lambda x: x.count()), reverse=True)
    ms = Senior.objects.filter(type='M').order_by('?')
    return render_to_response('senior.html', locals())

def about(request):
    settings = conf.settings
    section = 'about'
    page_title = '关于我们'
    return render_to_response('about.html', locals())

class MobilenoField(forms.CharField):
    max_length = 11
    default_error_messages = {
        'invalid': u'输入一个有效的手机号码。',
    }
    default_validators = [validate_mobileno]

class QuestionForm(forms.Form):
    writer = forms.CharField(max_length=100, required=True)
    privatename = forms.BooleanField(required=False)
    email = forms.EmailField(required=True)
    mobileno = MobilenoField(max_length=11, required=True)
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(max_length=10000, widget=forms.Textarea, required=True)
    privateall = forms.BooleanField(required=False)

def q_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question(
                writer = form.cleaned_data['writer'],
                publicname = not form.cleaned_data['privatename'],
                email = form.cleaned_data['email'],
                mobileno = form.cleaned_data['mobileno'],
                time = datetime.today(),
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                publicall = not form.cleaned_data['privateall']
            )
            q.save()

            return HttpResponseRedirect('/q/success/' + str(q.id))
    else:
        form = QuestionForm()

    settings = conf.settings
    section = 'qna'
    page_title = '提问'
    jsfiles = ['q_form', 'box']
    las = Answer.objects.filter(father__publicall=1).order_by('-time')[:4]
    ss = Senior.objects.filter(type='C').order_by('-gyear', '?')
    return render_to_response('q_form.html', locals())

def q_success(request, id):
    settings = conf.settings
    section = 'qna'
    page_title = '提问成功'
    jsfiles = ['box']
    las = Answer.objects.filter(father__publicall=1).order_by('-time')[:4]
    return render_to_response('q_success.html', locals())

def qna_index(request):
    settings = conf.settings
    section = 'qna'
    page_title = '问答'
    jsfiles = ['box']
    sas = Answer.objects.filter(father__publicall=1, selected=True).order_by('-id')
    las = Answer.objects.filter(father__publicall=1).order_by('-time')[:6]
    lqs = Question.objects.filter(publicall=1).order_by('-id')[:10]
    return render_to_response('qna_index.html', locals())

def qna_list(request):
    settings = conf.settings
    section = 'qna'
    page_title = '所有问答'
    jsfiles = ['box', 'qna_list']
    qs = Question.objects.all().order_by('-id')
    for q in qs:
        q.anss = q.answer_set.all()
        sas = q.answer_set.filter(selected=True)
        if sas.count():
            q.selected = True

    return render_to_response('qna_list.html', locals())

class AdditionalForm(forms.Form):
    writer = forms.CharField(max_length=100, required=True)
    privatename = forms.BooleanField(required=False)
    email = forms.EmailField(required=True)
    content = forms.CharField(max_length=10000, widget=forms.Textarea, required=True)

def qna_view(request, id):
    #~ starttime = datetime.now()
    if request.method == 'POST':
        form = AdditionalForm(request.POST)
        if form.is_valid():
            a = Additional(
                writer = form.cleaned_data['writer'],
                publicname = not form.cleaned_data['privatename'],
                email = form.cleaned_data['email'],
                time = datetime.today(),
                content = form.cleaned_data['content'],
                father = Question.objects.get(pk=id),
            )
            a.save()

            return HttpResponseRedirect('/q/success/' + id)
    else:
        form = AdditionalForm()

    settings = conf.settings
    section = 'qna'
    jsfiles = ['box', 'qna_view']

    try:
        q = Question.objects.get(pk=id)
    except:
        return error(request, u'抱歉，没有这个问题。')

    if not q.publicall and not request.session.get('authed_' + id):
        return HttpResponseRedirect('/view/auth/' + id)

    anss = q.answer_set.all()
    adds = q.additional_set.all()
    anss_adds = []
    for a in anss:
        a.type = 'ANS'
        anss_adds.append(a)
    for a in adds:
        a.type = 'ADD'
        anss_adds.append(a)
    anss_adds.sort(key=(lambda x: x.time))

    ts = q.tag.all()
    us = q.university.all()
    las = Answer.objects.filter(father__publicall=1).order_by('-time')[:6]

    qunivs = q.university.all()
    qtags = q.tag.all()
    rqs = list(Question.objects.
        filter(publicall=1).
        filter(Q(tag__in=qtags) | Q(university__in=qunivs)).
        exclude(id=q.id).distinct())
    for rq in rqs:
        rq.related = 0
        rqunivs = rq.university.all()
        for u in qunivs:
            if u in rqunivs:
                rq.related += 1
        rqtags = rq.tag.all()
        for t in qtags:
            if t in rqtags:
                rq.related += 1
    rqs.sort(key=(lambda x: x.related), reverse=True)
    rqs = rqs[:12]
    #~ exectime = datetime.now() - starttime

    page_title = q.title
    return render_to_response('qna_view.html', locals())

class AuthForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    mobileno = MobilenoField(max_length=11, required=True)

def qna_auth(request, id):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            q = Question.objects.get(pk=id)
            if (q.writer == form.cleaned_data['name'] and q.mobileno == form.cleaned_data['mobileno']):
                request.session['authed_' + id] = True
                return HttpResponseRedirect('/view/' + id)
            auth_failed = True
    else:
        form = AuthForm()

    settings = conf.settings
    section = 'qna'
    page_title = '查看非公开问答'
    return render_to_response('qna_auth.html', locals())

def search(request, kw):
    settings = conf.settings
    section = 'qna'
    page_title = kw + u' ‹ 搜索结果'
    jsfiles = ['box', 'search']

    try:
        short = Shortcut.objects.get(content=kw)
        if short.university:
            return HttpResponseRedirect('/university/' + short.university.name + '/')
        else:
            # short.tag
            return HttpResponseRedirect('/tag/' + short.tag.name + '/')
    except:
        if request.get_host() != TEST_HOST:
            log = Searchlog(
                content = kw,
                time = datetime.today(),
                ipaddr = request.META['REMOTE_ADDR']
            )
            log.save()

        qs = Question.objects.filter(publicall=1).order_by('-time')
        qs = qs.filter(Q(content__contains=kw) | Q(title__contains=kw))
        qs = list(qs)
        anss = Answer.objects.filter(father__publicall=1).filter(Q(content__contains=kw)).order_by('-time')
        for a in anss:
            if not a.father in qs:
                qs.append(a.father)
            try:
                qs[qs.index(a.father)].anss.append(a)
            except:
                qs[qs.index(a.father)].anss = [a]

        rcount = len(qs) + len(anss)

        return render_to_response('search.html', locals())

def tag_list(request):
    settings = conf.settings
    section = 'special'
    ts = list(Tag.objects.all())
    ts.sort(key=(lambda x: x.qcount() + x.ccount()), reverse=True)
    page_title = '标签'
    return render_to_response('tag_list.html', locals())

def tag_view(request, name):
    settings = conf.settings
    section = 'special'
    try:
        t = Tag.objects.get(name=name)
    except:
        return tag_list(request)

    page_title = t.name
    jsfiles = ['box']

    qs = t.question_set.all().order_by('-time')
    for q in qs:
        if q.answer_set.count() > 0:
            q.a = q.answer_set.all().order_by('-selected', '-time')[0]
    cs = t.comment_set.all()
    ts = list(Tag.objects.all())
    ts.sort(key=(lambda x: x.qcount() + x.ccount()), reverse=True)
    for ti in ts[12:]:
        ti.other = True

    if t.comment_set.count() > 0:
        return render_to_response('tag_view.html', locals())
    else:
        return render_to_response('tag_view_lite.html', locals())

def university_list(request):
    settings = conf.settings
    section = 'special'
    jsfiles = ['jquery.sort', 'university_list']

    order = request.GET.get('order', 'count')
    us = list(University.objects.all())
    if order == 'count':
        us.sort(key=(lambda x: x.qcount() + x.ccount()), reverse=True)
    elif order == 'name':
        us.sort(key=(lambda x: x.pinyin))
    #~ us = filter(lambda x: x.qcount() > 0, us)
    page_title = '高校'
    return render_to_response('university_list.html', locals())

def university_view(request, name):
    settings = conf.settings
    section = 'special'

    try:
        u = University.objects.get(name=name)
    except:
        return university_list(request)

    jsfiles = ['box']

    qs = u.question_set.all().order_by('-time')
    for q in qs:
        if q.answer_set.count() > 0:
            q.a = q.answer_set.all().order_by('-selected', '-time')[0]
    cs = u.comment_set.all()
    page_title = u.name
    return render_to_response('university_view.html', locals())

def comment_view(request, id):
    settings = conf.settings
    section = 'special'
    jsfiles = ['box']
    c = Comment.objects.get(id=id)
    if c.university:
        page_title = u'学长感悟 ‹ ' + c.university.name
    else:
        # c.tag
        page_title = u'学长感悟 ‹ ' + c.tag.name
    return render_to_response('comment_view.html', locals())

def answer_thank(request, id):
    a = Answer.objects.get(id=id)
    a.thank += 1
    a.save()
    return HttpResponse('Done.')

def error(request, text):
    return render_to_response('error.html', locals())
