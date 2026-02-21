def decorator(func):
    def wraps(*args,**kwargs):
        print('------------')
        func(*args,**kwargs)
        print('------------')
        return

    return wraps

@decorator
def my_print(name):
    print(f'Hello {name}!')

@decorator
def my_print1(name):
    print(f'Hello {name}!')

@decorator
def my_print2(name):
    print(f'Hello {name}!')

@decorator
def my_print3(name):
    print(f'Hello {name}!')


my_print('Marat')
my_print1('Alina')
my_print2('Sergey')
my_print3('Elena')