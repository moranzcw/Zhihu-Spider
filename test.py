import os
import csv

filename = os.path.join(os.path.abspath('./datafile'), 'data0002.csv')
# with open(filename, 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['user_data_json'].encode("utf-8").decode('unicode_escape'))


TABLEHEADER = ['user_url_token'.encode('utf-8'), 'user_data_json'.encode('utf-8')]
userinfo = {'user_url_token'.encode('utf-8'): "abcd".encode('utf-8'),
            'user_data_json'.encode('utf-8'): 'abcd\u4f60\u597dabcd'.encode('utf-8')
            }
# with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['死东风'])

with open(filename, 'a', newline='', encoding='utf-8') as file:
        file.write('abcd\u4f60\u597d')

with open(filename, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        print(line)
