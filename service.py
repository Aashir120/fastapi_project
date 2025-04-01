from fastapi import HTTPException
import httpx
from openai import OpenAI
from langchain_xai import ChatXAI
import base64
import os
from groq import Groq
# XAI_API_KEY= os.getenv('XAI_API_KEY')
XAI_API_KEY= "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"
BASE_CONTENT_URL = "https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
BASE_METADATA_URL = "https://www.gutenberg.org/ebooks/{book_id}"

# client = OpenAI(
#     api_key=XAI_API_KEY,
#     base_url = "https://api.x.ai/v1"
# )

#2. GroQ query
client = Groq(api_key=XAI_API_KEY)


#1. get book content
async def getBookContent(book_id: int):
    url = BASE_CONTENT_URL.format(book_id=book_id)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Book content not found")
        return {"content": response.text}

#2. gett book metadata
async def getBookMetaData(book_id: int):
    url = BASE_METADATA_URL.format(book_id=book_id)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Book content not found")
        return {"meta_data": response.text}

#3. Book Analyzer LLM
def getGroqResponse(content:str):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
             {"role": "system", "content": "Analyze this book such as sentiment analysis, identify key characteristics, plot summary"},
            {"role": "user", "content": content[:2000]}
            ],
    )
    return completion.choices[0].message.content