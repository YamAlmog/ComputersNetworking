import requests
URL = "http://localhost:8080"

def get_data():
    response = requests.get(URL)
    print(response.text)

def post_sentence():
    inp= input("Please input data according to this format: {'sentence' : '___', 'font_size' : '___', 'color' : '___'} ---> \n")
    response= requests.post(URL, json = inp)
    print(response.text)

def main():
    get_data
    post_sentence()

if __name__== "__main__":
    main()
    