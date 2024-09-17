import requests

class AbstractAPI:
    def __init__(self):
        self.vatURL: str = "https://vat.abstractapi.com/v1/"
        self.ipURL: str = "https://ipgeolocation.abstractapi.com/v1"
        self.ratesURL: str = "https://exchange-rates.abstractapi.com/v1/"

    def type_validation(self, type_, arg):
        if not isinstance(arg, type_):
            raise TypeError(f"Expected '{type_}' but got {type(arg).__name__}")



class VatAPI(AbstractAPI):
    def __init__(self, api_key):
        self.api_key: str = api_key
        super().__init__()
    
    def validate(self, vat_number: str) -> dict:
        self.type_validation(str, vat_number)
        params = {"api_key": self.api_key}
        params["vat_number"] = vat_number
        url = self.vatURL + "validate"
        response = requests.get(url, params=params)
        return response.text
    
    def calculate(self, amount: str, country_code: str, **kwargs) -> dict:
        params = {"api_key": self.api_key}
        self.type_validation(str, amount)
        self.type_validation(str, country_code)
        params["amount"] = amount
        params["country_code"] = country_code
        is_vat_incl = kwargs.get("is_vat_incl", None)
        vat_category = kwargs.get("vat_category", None)

        if is_vat_incl is not None:
            self.type_validation(bool, is_vat_incl)
            params["is_vat_incl"] = is_vat_incl
        if vat_category:
            self.type_validation(str, vat_category)
            params["vat_category"] = vat_category

        url = self.vatURL + "calculate"
        response = requests.request("GET", url, params=params)
        return response.text

    def categories(self, country_code: str):
        params = {"api_key": self.api_key}
        self.type_validation(str, country_code)
        params["country_code"] = country_code
        url = self.vatURL + "categories"
        response = requests.request("GET", url, params=params)
        return response.text


class IpAPI(AbstractAPI):
    def __init__(self, api_key):
        self.api_key: str = api_key
        super().__init__()

    def ip_info(self, **kwargs):
        params = {"api_key": self.api_key}
        ip_address = kwargs.get("ip_address", None)
        fields = kwargs.get("fields", None)

        if ip_address:
            self.type_validation(str, ip_address)
            params["ip_address"] = ip_address
        if fields:
            self.type_validation(str, fields)
            params["fields"] = fields
         
        response = requests.request("GET", self.ipURL, params=params)
        return response.text


class ExchangeRatesAPI(AbstractAPI):
    def __init__(self, api_key):
        self.api_key: str = api_key
        super().__init__()
    
    def live(self, base: str, **kwargs):
        params = {"api_key": self.api_key}
        self.type_validation(str, base)
        params["base"] = base
        target = kwargs.get("target", None)

        if target:
            self.type_validation(str, target)
            params["target"] = target

        url = self.ratesURL + "live"
        response = requests.request("GET", url, params=params)
        return response.text

    def convert(self, base: str, target: str, **kwargs):
        params = {"api_key": self.api_key}
        self.type_validation(str, base),
        self.type_validation(str, target)
        params["base"] = base,
        params["target"] = target
        date = kwargs.get("date", None)
        base_amount = kwargs.get("base_amount", None)

        if date:
            self.type_validation(str, date)
            params["date"] = date
        
        if base_amount:
            self.type_validation(str, base_amount)
            params["base_amount"] = base_amount

        url = self.ratesURL + "convert"
        response = requests.request("GET", url, params=params)
        return response.text



