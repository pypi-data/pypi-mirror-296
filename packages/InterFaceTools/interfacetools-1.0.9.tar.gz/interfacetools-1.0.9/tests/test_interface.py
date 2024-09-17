
from Leviathan.interface import InterfaceInstancingError, Interface


class yolo:
    
    def yolo2(self):pass

@Interface
class MyClass():   
    def __init__(self, *args,**kwargs):
       pass  
   
    def method_1(self): 
            pass
@Interface    
class Myinter():
    
    def method_3(self):pass

class My2Class(MyClass, yolo):
    
    def __init__(self):
        super().__init__(self)
        pass
    
    def method_2(self):
        pass

class mulparam(MyClass):

    def __init__(self, x:int=0, y:int=0):
        pass



def test_interface_instance():
    try:
        foo = MyClass()  # Should raise an error
        assert False
    except InterfaceInstancingError as e:
        assert True
        print(f"interface instancing worked {e}")    
        

def test_instancing():
    
    try:
        fog = My2Class()  # Creating an instance should work fine
    except Exception as e:
       
        print(e)
        assert False
    assert True
    
def test_polymorphism():
    fog = My2Class()
    
    print(fog)
    print(isinstance(fog, MyClass))          # Should return True
    assert isinstance(fog, MyClass)          # Should return True
    
    print(isinstance(fog, My2Class))         # Should return True
    assert isinstance(fog, My2Class)         # Should return True
    
    print(isinstance(MyClass, My2Class))     # Should return False    
    assert not isinstance(MyClass, MyClass)  # Should return False => therefore assert true
    
    print(isinstance(fog,Myinter))           # should be false
    assert not isinstance(fog, Myinter)      # Should return false => therefore assert True
   

def test_multiparam():
    try:
        foo = mulparam(2,3)
        assert True
    except InterfaceInstancingError as e:
        print(e)
        assert False

def test_abc():
    
    from abc import ABCMeta, abstractmethod
    @Interface
    class MyClassIn(metaclass=ABCMeta):
        def __init__(self, *args,**kwargs):
            pass   
        @abstractmethod
        def method_1(self): 
                    pass

    class mulparam(MyClassIn):

        def __init__(self, x:int=0, y:int=0):
            super().__init__(self)
            self.x = x
            pass
        def method_1(self): 
             pass
    try:
        foo = mulparam(2,3)
        assert True
    except Exception as e:
        print(e)
        assert False
    
   