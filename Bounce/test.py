import requests

url = 'https://api.exchangerate-api.com/v4/latest/USD'
r = requests.get(url)
print(r.json())