names = ['Ayush', 'Kushal', 'Ank']

for name in names:
    if len(name) > 5:
        print(name)
    if 'n' in name.lower():
        print(name)

while len(names) > 0:
    names.pop()
