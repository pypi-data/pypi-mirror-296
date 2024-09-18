from b3integrations.abstract_classes import AbstractIntegrationAppConfig


class BConfig3IntegrationMig24Config(AbstractIntegrationAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b3integration_mig24'

    is_integration = True
