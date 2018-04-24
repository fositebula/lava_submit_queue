import django_tables2 as tables
from django.utils.safestring import mark_safe
from models import VerifyDataTmp

def pklink(value):
    return mark_safe('<a href="{value}" title={value}>{name}</a>'.format(value=value, name=str(value).split('/')[-1]))

class VerifyTables(tables.Table):
    class Meta:
        model = VerifyDataTmp
        template_name = 'django_tables2/bootstrap.html'

    def render_submitting_log(self, value):
        return pklink(value)
