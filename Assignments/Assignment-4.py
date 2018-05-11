def out_fun(fn, *args):
    for arg in args:
        print('Result: {:^20.2f}'.format(fn(arg)))


out_fun(lambda x: x**2, 1, 2, 3, 4)
