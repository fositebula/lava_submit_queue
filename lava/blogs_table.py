from django.utils.safestring import mark_safe
from django_tables2 import CheckBoxColumn
from django_tables2 import DateColumn
from django_tables2 import DateTimeColumn
from django_tables2 import FileColumn
from django_tables2 import SingleTableView
from django_tables2 import tables
from models import Blog, VerifyData
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

import django_tables2


# class BlogMixinView(SingleTableMixin, FilterView):


def pklink(record):
    return django_tables2.TemplateColumn(
        '''<a href="{{ record.url }}">%s</a>'''%(record.title)
    )


class BlogTitleColumn(django_tables2.Column):
    def render(self, record):
        return pklink(record)

class MyBoolean(django_tables2.columns.BooleanColumn):
    span = "123"

class BlogTable(tables.Table):
    # id = django_tables2.Column(orderable=True)
    # title = django_tables2.Column(attrs={'id':'1'})
    author_name  = django_tables2.TemplateColumn('''
    <a href="{{ record.url }}">{{record.author_name}}</a>
    ''')
    # my_boolean = CheckBoxColumn(checked=True)
    # publice_time = DateTimeColumn()
    # file = FileColumn(verify_exists=False)
    class Meta:
        model = Blog
    #     template_name = 'django_tables2/bootstrap.html'
    #     row_attrs = {'data-id':lambda record: record.pk}
    #     # exclude = ('id')
    #     # attrs = {'class':'fda'}
    #     empty_text = ['1','2']
    #     show_header = True
    #     fields = ('id', 'title', 'author_name',)
    #     # order_by = ('-id', 'title')
    #     squence = ('author_name', 'title')
    #     # orderable = False


    # def before_render(self, request):
    #         self.columns.hide('artcle')

    # def get_top_pinned_data(self):
    #     return [{
    #         'title': 'value for C column',
    #     }]
    # pinned_row_attrs = {
    #     'data-id': '1'
    # }

    # title = BlogTitleColumn()
