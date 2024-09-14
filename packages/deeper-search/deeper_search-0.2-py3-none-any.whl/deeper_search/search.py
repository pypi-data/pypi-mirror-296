import os
import requests
import json
from pydantic import BaseModel, Field, ValidationError
from firecrawl import FirecrawlApp
from openai import OpenAI

# Environment variables setup

# OpenAI client setup


class SearchQuery(BaseModel):
    query: str = Field(..., title="Search query", description="Search query for Google Custom Search API")
    max_results: int = Field(7, title="Maximum number of results", description="Maximum number of results to return")

class GoogleCustomSearch:
    def __init__(self, query: SearchQuery, headers=None):
        self.query = query.query
        self.max_results = query.max_results
        self.headers = headers or {}
        self.api_key = self.headers.get("google_api_key") or self.get_api_key()
        self.cx_key = self.headers.get("google_cx_key") or self.get_cx_key()

    def get_api_key(self):
        return os.environ.get("GOOGLE_API_KEY") or raise_exception("Google API key not found.")

    def get_cx_key(self):
        return os.environ.get("GOOGLE_CX_KEY") or raise_exception("Google CX key not found.")

    def search(self):
        print(f"Searching with query: {self.query}...")
        url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.cx_key}&q={self.query}&num={self.max_results}"
        resp = requests.get(url)
        
        if not resp.ok:
            print(f"Error: {resp.status_code} - {resp.text}")
            return []

        try:
            search_results = resp.json()
        except json.JSONDecodeError:
            print("Error parsing JSON response.")
            return []

        items = search_results.get("items", [])
        results = []

        for item in items:
            if "youtube.com" not in item["link"]:
                results.append({
                    "title": item["title"],
                    "link": item["link"],
                    "snippet": item["snippet"],
                })

        return results

def raise_exception(message):
    raise Exception(message)

def summarize_text(question, text):
    prompt = f"""based on the question: {question} 
                Summarize and extract key information from the text below,
                Summary and important detail should not be longer than 100 Words:
                TEXT: {text}"""
    client = OpenAI(base_url=os.environ["base_url"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def search_and_summarize(user_question, max_results=5):
    try:
        query_input = SearchQuery(query=user_question, max_results=max_results)
        search_service = GoogleCustomSearch(query_input)
        results = search_service.search()
        
        app = FirecrawlApp(api_key=os.environ["FIRE_CRAWLER"])
        
        all_results = []
        for res in results:
            try:
                link = res["link"]
                title = res["title"]
                scrape_result = app.scrape_url(link, params={'formats': ['markdown']})
                summary = summarize_text(user_question, scrape_result["markdown"])
                all_results.append({"title": title, "Search_result": summary})
            except Exception as e:
                print(f"Error processing link: {link}. Error: {str(e)}")
        
        return all_results
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return []

# if __name__ == "__main__":
#     user_question = "What are the top universities in Pakistan"
#     results = search_and_summarize(user_question)
#     print(results)
