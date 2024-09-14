from octopus_common.enums.ErrorCode import ErrorCode

from octopus_common.model.BizException import CrawlerException


class ResultDetail:
    classType = None

    def __init__(self, class_type=None):
        if class_type is not None:
            self.classType = class_type


class ArrayListResultDetail:

    def __init__(self):
        self.__list = ["com.ctrip.fx.octopus.model.ResultArrayList"]

    def add(self, item):
        self.__list.append(item)

    def add_all(self, items):
        for item in items:
            self.add(item)

    def get(self, index):
        return self.__list[index]

    def remove(self, index):
        self.__list.pop(index)

    def size(self):
        return len(self.__list)

    def is_empty(self):
        return len(self.__list) == 0

    def clear(self):
        self.__list.clear()

    @property
    def __dict__(self):
        return self.__list


class DefaultDBPersistenceResultDetail(ResultDetail):
    def __init__(self, ds_type: str, replace: bool, result: list):
        if ds_type is None or result is None:
            raise CrawlerException(ErrorCode.DEFAULT_DB_PERSISTENCE_RESULT_DETAIL_ERROR.code,
                                   ErrorCode.DEFAULT_DB_PERSISTENCE_RESULT_DETAIL_ERROR.message)
        super().__init__("com.ctrip.fx.octopus.model.DefaultDBPersistenceResultDetail")
        self.dsType = ds_type
        self.replace = replace
        self.result = result
