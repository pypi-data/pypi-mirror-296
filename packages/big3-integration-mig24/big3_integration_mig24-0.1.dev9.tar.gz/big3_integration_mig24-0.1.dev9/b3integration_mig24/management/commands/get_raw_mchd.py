import logging
import time

from b3platform.b3integrations.core import AbstractIntegrationCommand

from b3integration_mig24.apps import BConfig3IntegrationMig24Config


class Command(AbstractIntegrationCommand):

    @property
    def integration_name(self) -> "str":
        return BConfig3IntegrationMig24Config.name

    @property
    def process_name(self) -> "str":
        return "get_raw_mchd"

    def get_logger(self) -> "logging.Logger":
        return logging.getLogger("b3")

    def handle(self, *args, **options) -> None:
        log = self.get_logger()
        log.info("Начало работы программы.")
        time.sleep(30)
        log.info("Завершение работы программы.")
