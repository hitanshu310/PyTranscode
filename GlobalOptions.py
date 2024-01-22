from abc import ABC, abstractmethod
from typing import List

class GlobalOptionsBuilder(ABC):
    '''Abstract Component Class'''
    @abstractmethod
    def add_options(self):
        pass

class DefaultGlobalOptions(GlobalOptionsBuilder):
    '''Concrete Component Class'''
    _globalOptionsList:List=None

    @property
    def globalOptionsList(self):
        return self._globalOptionsList

    def __init__(self):
        '''Initializing the _globalOptionsList'''
        self._globalOptionsList=[]
    
    def add_options(self):
        return self.globalOptionsList

class GlobalOptionsDecorator(GlobalOptionsBuilder,ABC):
    '''Abstract Decorator class for adding multiple global options'''
    _baseGlobalOptions: GlobalOptionsBuilder = None

    def __init__(self,baseGlobalOptions):
        self._baseGlobalOptions = baseGlobalOptions    

    @property
    def baseGlobalOptions(self):
        return self._baseGlobalOptions
    
    def add_options(self):
        pass

class ConcreteHideFlagOptionDecorator(GlobalOptionsDecorator):
    '''Concrete Decorator to add hide flag option'''

    def __init__(self, baseGlobalOptions):
        super().__init__(baseGlobalOptions)

    def add_options(self):
        return self.baseGlobalOptions.add_options() + ["-hide-flag"]

class ConcreteOverwriteOutputFiles(GlobalOptionsDecorator):
    '''Concrete Decorator to to overwrite output files'''

    def __init__(self, baseGlobalOptions, overwrite):
        super().__init__(baseGlobalOptions)
        self._overwrite=overwrite
    
    def add_options(self,overwrite='n'):
        return self.baseGlobalOptions.add_options() + ['-'+self._overwrite]

class ConcreteProgressURL(GlobalOptionsDecorator):
    '''Concrete Decorator to tadd progress-url'''
 
    def __init__(self, baseGlobalOptions,url):
        super().__init__(baseGlobalOptions)
        self._url=url


    def add_options(self):
        return self.baseGlobalOptions.add_options() + ['-progress '+self._url]
    
if __name__=='__main__':

    globalOptions=DefaultGlobalOptions()
    globalOptions=ConcreteOverwriteOutputFiles(globalOptions,'y')
    globalOptions=ConcreteHideFlagOptionDecorator(globalOptions)
    
    # Checking intermediate result
    print(globalOptions.add_options())
    globalOptions=ConcreteProgressURL(globalOptions,'www.sample.com')
    
    # Calling add_options to get the final list
    fullGlobalOptionsList=globalOptions.add_options()
    print(fullGlobalOptionsList)