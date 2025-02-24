from django.test import TestCase
from customers.recognition import get_passport_data

file_name = 'Szepene Kiss Rozalia.jpeg'
file_path = rf'C:\Users\alesh\Pictures\Passports\{file_name}'
print(get_passport_data(file_path))
