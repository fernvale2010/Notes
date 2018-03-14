

class MyClass:
    def __init__(self, message):
        print('in __init__')
        self.message = message
        
    def __call__(self):
        print('in __call__', ':', self.message)




cls1 = MyClass("Hello ") # __init__
cls2 = MyClass("World")

cls1()  # __call__
cls2()







