from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Financial advisor with Ollama"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Hello, Lets analyse your expenses"),
        ("user","Question:{question}")
    ]
)

import pandas as pd
df = pd.read_csv("transactions.csv")
# Get transactions in the Description column
transaction= df["Description"].unique()
#print(transaction)

def generate_response(question):
    llm=Ollama(model="gemma2")
    output_parser=CommaSeparatedListOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


user_input ="Can you categorize this expense in single word?"

#create new dictionary to add expense and category
category_dict = {
   "Kaiser" : "HealthCare"
}

if user_input :
   for i in range(len(transaction)):
        response=generate_response(user_input+" "+transaction[i])
        #to convert list response to a string
        delimiter = " " # Define a delimiter
        output_response = delimiter.join(response)
        category_dict.update({transaction[i] : output_response})

else:
    print("Something is wrong with the data")

#to print the dictionary
#for x, y in category_dict.items():
#  print(x, y)

#convert dictionary to pandas DataFrame
category_df = pd.DataFrame(list(category_dict.items()), columns = ['Description', 'Category'])


# applying merge with more parameters
df_merged = df.merge(category_df[['Description', 'Category']], on = 'Description', how = 'left')

df_merged.to_csv("transactions_categorized.csv", index=False)

