from django.db import DatabaseError, connections
from django.forms import ModelForm, Field, ValidationError, BooleanField
from django.forms.widgets import CheckboxInput, HiddenInput, Select

from explorer.models import Query, MSG_FAILED_BLACKLIST


class QueryForm(ModelForm):

    snapshot = BooleanField(widget=CheckboxInput, required=False)

    def __init__(self, *args, **kwargs):

        connection_choices = []
        for connection in connections.all():
            connection_choices.append((connection.alias, connection.alias))

        # if 'initial' in kwargs:
        #     kwargs['initial'].update({
        #         'connection': connection_choices[0][0]
        #     })
        # else:
        #     kwargs['initial'] = {
        #         'connection': connection_choices[0][0]
        #     }

        super(QueryForm, self).__init__(*args, **kwargs)

        if len(connection_choices) <= 1:
            self.fields['connection'].widget = HiddenInput()
        else:
            self.fields['connection'].widget = Select(
                attrs={
                    'class': 'form-control'
                },
                choices=connection_choices
            )

        self.connection_choices = connection_choices

    def clean(self):
        if self.instance and self.data.get('created_by_user', None):
            self.cleaned_data['created_by_user'] = self.instance.created_by_user
        return super(QueryForm, self).clean()

    def clean_sql(self):
        sql = self.cleaned_data.get('sql', '')
        connection = self.cleaned_data.get('connection', 'default')
        query = Query(sql=sql, connection=connection)

        passes_blacklist, failing_words = query.passes_blacklist()

        error = MSG_FAILED_BLACKLIST % ', '.join(
            failing_words) if not passes_blacklist else None

        if not error and not query.available_params():
            try:
                query.execute_query_only()
            except DatabaseError as e:
                error = str(e)

        if error:
            raise ValidationError(
                error,
                code="InvalidSql"
            )

        return sql

    @property
    def created_by_user_email(self):
        return self.instance.created_by_user.email if self.instance.created_by_user else '--'

    class Meta:
        model = Query
        fields = ['title', 'connection', 'sql', 'description', 'snapshot']
