from integrations_market.core import AbstractIntegrationAppConfig
from integrations_market.core import GetIntegrationStatusType
from integrations_market.core import get_integration_status


class BConfig3IntegrationMig24Config(AbstractIntegrationAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b3integration_mig24'

    get_integration_status_func: 'GetIntegrationStatusType' = get_integration_status
    is_integration = True
