from abc import ABC, abstractmethod

class GlobalOptionsBuilder(ABC):
    '''Abstract Component Class'''
    _globalOptionsList:list=[]
    
    @abstractmethod
    def add_options(self):
        pass

class DefaultGlobalOptions(GlobalOptionsBuilder):
    '''Concrete Component Class'''
    def __init__(self):
        '''Initializing the _globalOptionsList declared in the Parent Class GlobalOptionsBuilder'''
        self._globalOptionsList=[]
    def add_options(self):
        return self

class GlobalOptionsDecorator(GlobalOptionsBuilder,ABC):
    '''Abstract Decorator class for adding multiple global options'''
    _baseGlobalOptions: GlobalOptionsBuilder = None

    def __init__(self,baseGlobalOptions):
        self._baseGlobalOptions = baseGlobalOptions    

    @property
    def globalOptionsList(self):
        return self._baseGlobalOptions._globalOptionsList
    
    @globalOptionsList.setter
    def globalOptionsList(self,globalOptionsList):
        self._baseGlobalOptions._globalOptionsList=globalOptionsList

class ConcreteHideFlagOptionDecorator(GlobalOptionsDecorator):
    '''Concrete Decorator to add hide flag option'''
   
    def add_options(self):
        self.globalOptionsList=self.globalOptionsList+ ["-hide-flag"]
        return self._baseGlobalOptions

class ConcreteOverwriteOutputFiles(GlobalOptionsDecorator):
    '''Concrete Decorator to to overwrite output files'''

    def add_options(self,overwrite='n'):
        self.globalOptionsList=self.globalOptionsList + ['-'+overwrite]
        return self._baseGlobalOptions

class ConcreteProgressURL(GlobalOptionsDecorator):
    '''Concrete Decorator to tadd progress-url'''

    def add_options(self,url):
        self.globalOptionsList=self.globalOptionsList + ['-progress '+url]
        return self._baseGlobalOptions
    
if __name__=='__main__':
    globalOptions=DefaultGlobalOptions()
    # print(globalOptions._globalOptionsList)

    globalOptions=ConcreteOverwriteOutputFiles(globalOptions)
    globalOptions=globalOptions.add_options('y')
    # print(globalOptions._globalOptionsList)

    globalOptions=ConcreteHideFlagOptionDecorator(globalOptions)
    globalOptions=globalOptions.add_options()
    # print(globalOptions._globalOptionsList)

    globalOptions=ConcreteProgressURL(globalOptions)
    globalOptions=globalOptions.add_options('www.sample.com')
    print(globalOptions._globalOptionsList)