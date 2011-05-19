# -*- coding: UTF-8 -*-

from datetime import datetime, date
from django.db import models
from common import validate_mobileno
import urllib

class Question(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.now)
    writer = models.CharField(max_length=100)
    email = models.EmailField()
    mobileno = models.CharField(max_length=11, validators=[validate_mobileno])
    content = models.CharField(max_length=10000)
    publicname = models.BooleanField(default=True)
    publicall = models.BooleanField(default=True)
    handled = models.BooleanField(help_text='whether the question was handled')
    tag = models.ManyToManyField('Tag', blank=True)
    university = models.ManyToManyField('University', blank=True)

    def writername(self):
        if self.publicall and self.publicname:
            return self.writer
        else:
            return '匿名'

    def __unicode__(self):
        return "[%d]%s" % (self.id, self.title)


class Answer(models.Model):
    time = models.DateTimeField(default=datetime.now)
    content = models.CharField(max_length=10000)
    senior = models.ForeignKey('Senior')
    selected = models.BooleanField()
    father = models.ForeignKey('Question')
    thank = models.IntegerField(default=0)

    def title(self):
        return self.father.title

    def writer(self):
        return self.senior.name

    # is an obsolete answer or not
    def past(self):
        if self.time.year < datetime.now().year:
            return True
        else:
            return False

    def __unicode__(self):
        return self.title()


class Additional(models.Model):
    time = models.DateTimeField(default=datetime.now)
    content = models.CharField(max_length=10000)
    writer = models.CharField(max_length=100)
    email = models.EmailField()
    publicname = models.BooleanField(default=True)
    handled = models.BooleanField()
    father = models.ForeignKey('Question')

    def title(self):
        return self.father.title

    def writername(self):
        if self.publicname:
            return self.writer
        else:
            return '匿名'

    def __unicode__(self):
        return self.father.title


class Senior(models.Model):
    SUBJECT_CHOICES = (
        ('A', 'Art'),
        ('S', 'Science'),
    )
    TYPE_CHOICES = (
        ('C', 'Core'),
        ('M', 'Maintainer'),
    )

    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=1, choices=SUBJECT_CHOICES)
    university = models.ForeignKey('University')
    gyear = models.IntegerField(verbose_name='Graduated')
    major = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=True)

    def avatar(self):
        return '%s-%s.jpg' % (self.id, self.name)

    def count(self):
        return self.answer_set.count() + self.comment_set.count()

    def __unicode__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pinyin = models.CharField(max_length=200)
    website = models.CharField(max_length=500, blank=True)
    zsbsite = models.CharField(max_length=500, blank=True)
    is211 = models.BooleanField(default=False)
    is985 = models.BooleanField(default=False)
    nstudent = models.IntegerField(blank=True)
    province = models.CharField(max_length=20)

    def qcount(self):
        return self.question_set.count()

    def scount(self):
        return self.senior_set.count()

    def ccount(self):
        return self.comment_set.count()

    def name_gbk(self):
        return urllib.quote(self.name.encode('gbk'))

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    desc = models.CharField(max_length=2000)

    def qcount(self):
        return self.question_set.count()

    def ccount(self):
        return self.comment_set.count()

    def __unicode__(self):
        return self.name

class Comment(models.Model):
    time = models.DateTimeField(default=datetime.now)
    summary = models.CharField(max_length=1000)
    content = models.CharField(max_length=10000, blank=True)
    senior = models.ForeignKey('Senior')
    tag = models.ForeignKey('Tag', blank=True, null=True)
    university = models.ForeignKey('University', blank=True, null=True)

    def writer(self):
        return self.senior.name

    def title(self):
        if self.tag:
            return self.tag.name
        if self.university:
            return self.university.name

    def __unicode__(self):
        return self.title()

class Shortcut(models.Model):
    content = models.CharField(max_length=100, unique=True)
    tag = models.ForeignKey('Tag', blank=True, null=True)
    university = models.ForeignKey('University', blank=True, null=True)

    def title(self):
        if self.tag:
            return self.tag.name
        if self.university:
            return self.university.name

    def __unicode__(self):
        return self.title()

class Searchlog(models.Model):
    ipaddr = models.IPAddressField()
    content = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.content
