from vault import Vault
from flask.json import JSONEncoder
from decimal import Decimal
import numpy

class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, numpy.int64):
            return float(o)
        return super(DecimalEncoder,self).default(o)

class Config_Api:

    def __init__(self, tenant):
        vault = Vault(tenant)
        self.tenant_config = vault.get_tenant_data()

    def get_value_from_key(self, outer_key, inner_key):
        if inner_key.lower() == "":
            return self.tenant_config[outer_key]
        else:
            outer_key = outer_key
            inner_key = inner_key
            if outer_key in self.tenant_config:
                outer_arr = self.tenant_config[outer_key]
                for el in outer_arr:
                    for (k, v) in el.items():
                        if k == inner_key:
                            return v
            else:
                raise KeyError
