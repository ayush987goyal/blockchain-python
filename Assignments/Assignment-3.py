persons = [
    {'name': 'Ayush', 'age': 22, 'hobbies': ['cubing', 'coding']},
    {'name': 'Kushal', 'age': 17, 'hobbies': ['baski']}
]
print(persons)

names = [person['name'] for person in persons]
print(names)

older = all([person['age'] > 20 for person in persons])
print(older)

new_persons = [person.copy() for person in persons]
new_persons[0]['name'] = 'YoYo'
print(new_persons)
print(persons)

person1, person2 = persons
print(person1, person2)
