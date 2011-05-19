# -*- coding: UTF-8 -*-
import base64
from settings import MAIL_NOTIFICATION, BASE_URL
from django.contrib import admin
from django import forms
from zy.models import *
import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# deal with Chinese characters
reload(sys)
sys.setdefaultencoding('utf8')

class QuestionForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'writer', 'publicall', 'handled')
    list_filter = ('handled',)
    search_fields = ('title',)

    filter_horizontal = ('tag', 'university')

    form = QuestionForm


class AnswerForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'writer', 'content', 'selected', 'thank')
    list_filter = ('selected',)

    radio_fields = {'father': admin.VERTICAL, 'senior': admin.HORIZONTAL}

    form = AnswerForm

    def save_model(self, request, obj, form, change):
        if change is False:
            # new answer
            obj.father.handled = True
            obj.father.save()

            adds = obj.father.additional_set.all()
            mailto = {obj.father.email: obj.father.writer}
            for a in adds:
                a.handled = True
                a.save()
                if not mailto.has_key(a.email):
                    mailto[a.email] = a.writer
            if MAIL_NOTIFICATION:
                smtp = smtplib.SMTP()
                smtp.connect("smtp.gmail.com", "587")
                smtp.starttls()
                smtp.login('zhiyuan@hcc.im', '@ff4eHf2%2dJ9')
                length = 200
                for email, name in mailto.items():
                    msg = MIMEMultipart()
                    msg.set_charset('UTF-8')
                    msg['From'] = "Zhiyuan Support"
                    msg['Subject'] = u"你提的问题得到了 %s 的回答" % (obj.senior.name, )
                    msg['To'] = email
                    msg.add_header("X-Mailer", "Zhiyuan");
                    if len(obj.content) <= length:
                        content = obj.content
                    else:
                        content = obj.content[:length] + '...'
                    body = '''%(name)s，你好！<br /><br />

%(senior)s学长 回答了你提出的问题“%(title)s”：<br /><br />

%(answer)s <a href="%(baseurl)sview/%(id)s/" target="_blank">[更多]</a><br /><br />

点击链接查看问答内容：<a href="%(baseurl)sview/%(id)s/" target="_blank">%(baseurl)sview/%(id)s/</a><br /><br />

——志愿 • <a href="%(baseurl)s" target="_blank">%(baseurl)s</a>''' % {
                    'name': str(name),
                    'senior': str(obj.senior.name),
                    'title': str(obj.father.title),
                    'answer': "<br />".join(str(content).split("\n")),
                    'id': obj.father.id,
                    'baseurl': BASE_URL, }
                    txt = MIMEText(body, 'html', 'UTF-8')
                    msg.attach(txt)
                    smtp.sendmail('zhiyuan@hcc.im', msg['To'], msg.as_string())
                smtp.quit()

        super(AnswerAdmin, self).save_model(request, obj, form, change)


class AdditionalForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Additional

class AdditionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'writer', 'content', 'handled')

    radio_fields = {'father': admin.VERTICAL}

    form = AdditionalForm


class SeniorAdmin(admin.ModelAdmin):
    list_display = ('name', 'gyear', 'university', 'subject', 'major', 'notes', 'type')

    radio_fields = {'university': admin.VERTICAL}


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'qcount', 'scount', 'is211', 'is985')
    list_filter = ('is211', 'is985')


class TagForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'qcount')

    form = TagForm


class CommentForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('senior', 'title', 'summary', 'content')

    form = CommentForm

    radio_fields = {
        'senior': admin.HORIZONTAL,
        'tag': admin.HORIZONTAL,
        'university': admin.HORIZONTAL,
    }

class ShortcutAdmin(admin.ModelAdmin):
    list_display = ('content', 'title')

    radio_fields = {
        'tag': admin.HORIZONTAL,
        'university': admin.HORIZONTAL,
    }

class SearchlogAdmin(admin.ModelAdmin):
    list_display = ('content', 'time', 'ipaddr')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Additional, AdditionalAdmin)
admin.site.register(Senior, SeniorAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Shortcut, ShortcutAdmin)
admin.site.register(Searchlog, SearchlogAdmin)
