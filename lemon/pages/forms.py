from django import forms
from django.contrib.sites.models import Site
from django.db.models import Count, Max
from django.utils.translation import ugettext_lazy as _

from lemon.pages.models import Page
from lemon.pages.widgets import SelectPageTemplate


class PageAdminForm(forms.ModelForm):

    slug = forms.RegexField(
        label = _(u'URL'),
        max_length = 255,
        regex = r'^/[\.\-/\w]*$',
        error_messages = {
            'invalid': _(u"Enter a valid 'slug' beginning with slash and "
                         u"consisting of letters, numbers, underscores, "
                         u"slashes or hyphens.")
        },
    )
    template = forms.CharField(
        label = _(u'Template'),
        max_length = 255,
        widget = SelectPageTemplate(),
        error_messages = {
            'required': _(u'Please create template for pages')
        },
    )

    def is_slug_unique(self):
        qs = Site.objects.all()
        qs = qs.filter(pk__in=self.cleaned_data['sites'],
                       page__slug=self.cleaned_data['slug'],
                       page__language=self.cleaned_data['language'])
        if self.instance and self.instance.pk:
            qs = qs.exclude(page__pk=self.instance.pk)
        qs = qs.annotate(page_count=Count('page'))
        result = qs.aggregate(page_count_max=Max('page_count'))
        return not result['page_count_max']

    def clean(self):
        cleaned_data = self.cleaned_data
        slug = cleaned_data.get('slug')
        sites = cleaned_data.get('sites')
        language = cleaned_data.get('language')
        if slug and sites and language and not self.is_slug_unique():
            msg = _(u'Page %s already exists for some of selected sites and language')
            raise forms.ValidationError(msg % cleaned_data['slug'])
        return cleaned_data

    class Meta:
        model = Page
