
from abc import abstractmethod
from django.core.cache import cache

from afex_logger.util import LogUtil, ConfigProvider


class Repo:

    class Meta:
        abstract = True

    @abstractmethod
    def peck(self, n=15) -> list:
        raise NotImplementedError

    @abstractmethod
    def re_stack(self, elements: list):
        raise NotImplementedError

    @abstractmethod
    def aggregate(self, log_type, payload):
        raise NotImplementedError


class InMemoryRepo(Repo):

    def __init__(self):
        self.__data = []

    def peck(self, n=15) -> list:
        elements = self.__data[:n]
        del self.__data[:n]
        return elements

    def re_stack(self, elements: list):
        self.__data = elements + self.__data

    def aggregate(self, log_type, payload):
        self.__data.append({"logType": log_type, "payload": payload})


class RedisRepo(Repo):

    __cache_key = "extras:repo"

    def __get_data(self):
        cached_data = cache.get(self.__cache_key)
        if not cached_data:
            cached_data = []

            timeout = 60 * 60 * 24 * 7
            cache.set(self.__cache_key, cached_data, timeout=timeout)

        return cached_data

    def update_data(self):
        cached_data = cache.get(self.__cache_key)
        if not cached_data:
            cached_data = []

            timeout = 60 * 60 * 24 * 7
            cache.set(self.__cache_key, cached_data, timeout=timeout)

        return cached_data



    def peck(self, n=15) -> list:
        data = self.__get_data()
        elements = data[:n]
        del data[:n]
        return elements

    def re_stack(self, elements: list):
        self.__data = elements + self.__data

    def aggregate(self, log_type, payload):
        self.__data.append({"logType": log_type, "payload": payload})


class Repository:

    _instance = None
    _repo: Repo = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        config = LogUtil().get_config_provider()
        self.repo = InMemoryRepo() if config.is_test_mode() else RedisRepo(config)


repository = Repository()

