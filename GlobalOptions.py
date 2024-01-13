from abc import ABC, abstractmethod


class GlobalOptionBuilder(ABC):
    globalOptionsList = []

    @abstractmethod
    def add_option(self, **kwargs):
        pass


class DefaultGlobalOptions(GlobalOptionBuilder):

    global_options_list: list = []

    def __init__(self, global_options_list):
        self.global_options_list = global_options_list

    def add_option(self, **kwargs):
        return self.global_options_list


class GlobalOptionDecorator(GlobalOptionBuilder, ABC):

    _default_global_options: DefaultGlobalOptions = None

    def __init__(self, default_global_options: DefaultGlobalOptions):
        self._default_global_options = default_global_options

    @property
    def default_global_options(self):
        return self._default_global_options

    @default_global_options.setter
    def default_global_options(self, default_global_options):
        self._default_global_options = default_global_options

    @abstractmethod
    def add_option(self):
        pass


class ConcreteHideFlagOptionDecorator(GlobalOptionDecorator):

    def add_option(self):
        self.default_global_options.global_options_list = self.default_global_options.global_options_list + ["-hide-flag"]
        return self.default_global_options


class ConcreteLogLevelOptionDecorator(GlobalOptionDecorator):

    def add_option(self, **kwargs):
        self.default_global_options.global_options_list = self.default_global_options.global_options_list + ["-loglevel", kwargs.pop('log_level')]
        return self.default_global_options
