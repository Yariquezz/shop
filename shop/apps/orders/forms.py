from django import forms
from django.core.exceptions import ValidationError
from .models import Order
import logging

logger = logging.getLogger(__name__)


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["shipping_address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_address'].required = True

    def clean_shipping_address(self):
        data = self.cleaned_data['shipping_address']
        if len(data) <= 10:
            raise ValidationError("Field too short")
        return data
