from abc import ABC, abstractmethod

class GlobalOptionsBuilder(ABC):
    '''Abstract Component Class'''
    @abstractmethod
    def add_options(self):
        pass

class DefaultGlobalOptions(GlobalOptionsBuilder):
    '''Concrete Component Class'''
    def __init__(self,globalOptionsList):
        self.globalOptionsList=globalOptionsList
    def add_options(self):
        return self.globalOptionsList

class GlobalOptionsDecorator(GlobalOptionsBuilder,ABC):
    '''Abstract Decorator class for adding multiple global options'''

    def __init__(self,globalOptionsBuilder):
        self.globalOptionsBuilder = globalOptionsBuilder    

    @property
    def globalOptionsList(self):
        return self.globalOptionsList
    
    @globalOptionsList.setter
    def globalOptionsList(self,globalOptionsList):
        self.globalOptionsList=globalOptionsList

class ConcreteHideFlagOptionDecorator(GlobalOptionsDecorator):
    '''Concrete Decorator to add hide flag option'''
   
    def add_options(self):
        return self.globalOptionsBuilder.add_options()+ ["-hide-flag"]

class ConcreteOverwriteOutputFiles(GlobalOptionsDecorator):
    '''Concrete Decorator to to overwrite output files'''

    def add_options(self,overwrite='n'):
        return self.globalOptionsBuilder.add_options() + ['-'+overwrite]

class ConcreteProgressURL(GlobalOptionsDecorator):
    '''Concrete Decorator to tadd progress-url'''

    def add_options(self,url):
        return self.globalOptionsBuilder.add_options() + ['-progress '+url]