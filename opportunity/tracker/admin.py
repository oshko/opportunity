#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#
#       Copyright 2012 John Kern
#
'''
register to allow admin access to database.
'''
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
