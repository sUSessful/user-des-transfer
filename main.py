import json
from openai import OpenAI
from pymongo import MongoClient
import pandas as pd


def api_getting():
    client = MongoClient("mongodb+srv://datathon-2023:datathon-2023@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority")
    client.admin.command('ping')
    db = client["Api"]
    collection = db["api"]
    documents = collection.find()
    api_key = None
    for item in documents:
        if item['api'] == 'datathon-service':
            api_key = item['api-key']
            break
    client.close()
    return api_key

def read_embeddded():
    with open("er.json", "r") as f:
        er = json.load(f)
    f.close()
    return er

def make_embedded():
    with open("er.json", "r") as f:
        er = json.load(f)
    client = OpenAI(api_key = api_getting())
    df = pd.read_csv("nike_dataset.csv")
    for item in df["description"]:
        prompt_text = " ".join(["Labeling this", item])
        response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages =[
                        {"role": "system", "content" :"you are an NLP engineer, and your task is get all vocabulary belong to fields tagname: COLOR, CLOTHING, BRAND, MATERIAL, STYLE, ACTIVITY, AGE, FEATURE and return the list dict label to [{\"word\": str, \"tagname\": str}]"},
                        {"role": "system", "content": prompt_text}
                ]
            )
        er.append(response.choices[0].message.content)
    with open('er.json', 'w') as f:
        json.dump(er, f, indent=2)
    f.close()
    
if __name__ == "__main__":
    make_embedded()