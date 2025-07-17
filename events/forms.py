from django import forms
from events.models import Event,  Category


class StyledFormMixin:
    """Mixing to apply style to form field"""

    default_classes = "mt-3 border-1 border-gray-300 w-72 px-3 py-1 rounded-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": f"Enter {field.label.lower()}",
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": f"{self.default_classes} resize-none",
                        "placeholder": f"Enter {field.label.lower()}",
                        "rows": 5,
                    }
                )
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update(
                    {
                        "class": "mt-2 mb-3 border-1 border-gray-300 px-3 py-1 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                    }
                )
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update(
                    {
                        "class": "mt-2 mb-3 border-1 border-gray-300 px-3 py-2 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                    }
                )
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "type": "time",
                        "class": "mt-2 mb-2 border-1 border-gray-300 px-3 py-2 rounded-md shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"
                    }
                )
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({"class": "border-gray-300 border-b border-gray-300 mt-3 mb-4 space-y-2"})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({"class": "border-t border-gray-300 border-b border-gray-300 mt-3 mb-4 space-y-2 border-1 border-blue-400 px-2 py-1 rounded-sm focus:outline-none focus:border-green-400 focus:ring-green-400"})
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({
                        "class": "border-1 border-blue-400 px-2 py-1 mt-3 mb-3 rounded-sm focus:outline-none focus:border-green-400 focus:ring-green-400"
                    })  
            else:
                field.widget.attrs.update({"class": self.default_classes})


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category','participant', 'evn_img']
        widgets = {
            "date": forms.SelectDateWidget,
            "time": forms.TimeInput,
            "category": forms.RadioSelect,
            "participant": forms.CheckboxSelectMultiple
        }

    """ Widget using mixins """

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
            
