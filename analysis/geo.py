import requests
response = requests.get('http://api.map.baidu.com/geocoder/v2/'
                        '?address=常德'
                        '&output=json'
                        '&ak=Pt15VZ8Msk0fjKO4SXLUD58CiwbOOZ0P')
print(response.text)

