import requests

def get_data():
    api_url= "http://localhost:8080"
    
    response = requests.get(api_url)
    print(response.text)

def post_sentence():
    url= "http://localhost:8080"
    inp= {"sentence": "Hello Mami Sheli"}
    response= requests.post(url, json= inp)

def main():
    post_sentence()

if __name__== "__main__":
    main()