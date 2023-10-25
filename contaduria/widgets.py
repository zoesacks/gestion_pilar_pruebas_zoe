import datetime
from django import forms
from django.utils.dates import MONTHS
from django.forms.utils import flatatt


class CustomMonthSelectWidget(forms.Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})
        context['widget']['optgroups'] = self.render_options([value])
        context['widget']['value'] = value.strftime('%Y-%m') if value else ''
        context['widget']['final_attrs'] = flatatt(final_attrs)
        return context

    def render_options(self, selected_choices):
        selected_value = selected_choices[0] if selected_choices else None
        selected_value = selected_value.strftime('%Y-%m') if selected_value else None

        options = []
        for month in range(1, 13):
            month_label = MONTHS.get(month)
            month_value = f'{selected_value[:4]}-{str(month).zfill(2)}'
            options.append((month_value, month_label))

        selected_values = {selected_value} if selected_value else set()
        return [
            {
                'value': option_value,
                'label': option_label,
                'selected': option_value in selected_values,
                'index': i,
                'attrs': {}
            }
            for i, (option_value, option_label) in enumerate(options)
        ]

    def value_from_datadict(self, data, files, name):
        year_month = data.get(name)
        if year_month:
            year, month = year_month.split('-')
            return datetime.date(year=int(year), month=int(month), day=1)
        return None

    def value_omitted_from_data(self, data, files, name):
        return False