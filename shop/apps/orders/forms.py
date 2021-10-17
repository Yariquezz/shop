from django import forms
from .models import Order
import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

NP_API_KEY = os.environ.get('NP_API_KEY', '')
URL = 'https://api.novaposhta.ua/v2.0/json/'
HEADERS = {
    "Content-Type": "aplications/json"
}


def get_branchets_list(city):
    branches = []
    try:
        body = {
            "apiKey": NP_API_KEY,
            "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": city,
                "Limit": 5
            }
        }
        r = requests.get(
            url=URL,
            headers=HEADERS,
            json=body,
        )
        content = json.loads(r.content)
        body = {
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "Language": "ua",
                "SettlementRef": content["data"][0]["Addresses"][0]["Ref"],
                "TypeOfWarehouseRef": "841339c7-591a-42e2-8233-7a0a00f0ed6f"
            },
            "apiKey": NP_API_KEY
        }
        for i in content["data"]:
            branches.append(i["Description"])
    except Exception as err:
        logger.error(err)
    return branches


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["shipping_address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_address'] = NpBracnhField()


class NpBracnhBoundField(forms.BoundField):
    @property
    def branch(self):
        """
        Return the country the coordinates lie in or None if it can't be
        determined.
        """
        city = self.value()
        if city:
            return get_branchets_list(city)
        else:
            return None


class NpBracnhField(forms.Field):
    def get_bound_field(self, form, field_name):
        return NpBracnhBoundField(form, self, field_name)
