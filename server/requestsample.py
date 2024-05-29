import requests

url = "https://traffic-data.onrender.com/find?"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for obj in data:
        print(obj)
else:
    print("Error fetching data :(")

