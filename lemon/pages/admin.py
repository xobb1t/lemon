from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.publications.admin import PublicationAdmin
from lemon.pages.models import Page
from lemon.pages.forms import PageAdminForm


class PageAdmin(PublicationAdmin):

    form = PageAdminForm
    date_hierarchy = None
    search_fields = ['title', 'content']
    fieldsets = (
        (None, {
            'fields': ('slug', 'site', 'title', 'content', 'template')
        }),
    ) + PublicationAdmin.fieldsets
    list_display = ('slug', 'title', 'site', 'author_name', 'enabled')
    list_display_links = ('title',)
    list_filter = ('enabled', 'site')
    string_overrides = {
        'add_title': _(u'Add page'),
        'change_title': _(u'Change page'),
        'changelist_title': _(u'Choose page to change'),
        'changelist_popup_title': _(u'Choose page'),
        'changelist_addlink_title': _(u'Add page'),
        'changelist_paginator_description': lambda n: \
            ungettext(u'%(count)d page', u'%(count)d pages', n)
    }
    tabs = True


extradmin.site.register(Page, PageAdmin)