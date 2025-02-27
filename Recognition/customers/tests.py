from django.test import TestCase
from customers.recognition import get_passport_data, get_text_data

text = 'IDKGZID3310280021402200000422<\n0002141M3304042KGZ<<<<<<<<<<<7\nAGDEEV<<ALEKSEI<<<<<<<<<<<<<<<'
print(get_text_data(text))
