import requests
while True:
    city = input("Enter city: ")
    if city.lower() == "exit":
        break
    url = f"https://wttr.in/{city}?format=3"

    response = requests.get(url)

    print(response.text)