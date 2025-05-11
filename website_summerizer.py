import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    print('api key found!!')

else:
    print('no api key found!!!')


openai = OpenAI()

class Website:

    url:str
    title:str
    text:str

    def __init__(self, url):

        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"

        for irrelevent in soup.body(['script', 'style', 'img', 'input']):
            irrelevent.decompose()

        self.text =  soup.body.get_text(separator="\n", strip=True)


web = Website("https://edwarddonner.com")

print(web.title)

print(web.text)


system_prompt = "You are an assistant that analyzes the contents of a website\
    and provides a short summery, ignoring test that might be navigation related\
    Respond in markdown."



def user_prompt_for(web):
    user_prompt = f"\nYou are looking at a website titled {web.title}"
    user_prompt += "The contents of this website is as follows:\
        please provide a short summary of this website in markdown.\
        If it include news or announcements, then summarize these too.\n\n"
    
    user_prompt +=web.text
    
    return user_prompt


# print(user_prompt_for(web))

#### message format for openai is list of dict having role and system/user


def messages_for(web):

    return[
        {'role':'system', 'content':system_prompt}
        {'role':'user', 'content':user_prompt_for(web)}
    ]