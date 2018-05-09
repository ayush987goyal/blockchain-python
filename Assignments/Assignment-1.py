name = input('Enter your name: ')
age = int(input('Enter your age: '))


def print_data():
    print(f'Name: {name} Age: {age}')


def print_arg_data(data1, data2):
    print(f'{data1} and {data2}')


def calc_decade(my_age):
    return my_age//10


print_data()
print_arg_data(name, age)
print(calc_decade(age))
