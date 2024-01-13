from GlobalOptions import *

if __name__ == "__main__":
    default_global_options = DefaultGlobalOptions([])
    print(ConcreteLogLevelOptionDecorator(ConcreteHideFlagOptionDecorator(default_global_options).add_option()).add_option(log_level='quiet').global_options_list)
