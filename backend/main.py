from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "message": "Page Pulse Backend is Running!"
    }

@app.post("/audit")
def audit(request: URLRequest):

    try:
        start_time = time.time()

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            request.url,
            headers=headers,
            timeout=10
        )

        end_time = time.time()

        # Check if response is HTML
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            raise HTTPException(
                status_code=400,
                detail="URL does not point to an HTML webpage."
            )

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"

        meta_tag = soup.find("meta", attrs={"name": "description"})

        meta_description = (
            meta_tag.get("content").strip()
            if meta_tag and meta_tag.get("content")
            else "No Meta Description"
        )

        h1_count = len(soup.find_all("h1"))

        images = soup.find_all("img")

        missing_alt_images = sum(
            1
            for image in images
            if not image.get("alt")
        )

        text = soup.get_text(separator=" ", strip=True)

        word_count = len(text.split())

        return {
            "status": response.status_code,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "title": title,
            "meta_description": meta_description,
            "h1_count": h1_count,
            "missing_alt_images": missing_alt_images,
            "word_count": word_count
        }

    except requests.exceptions.MissingSchema:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL. Include http:// or https://"
        )

    except requests.exceptions.InvalidURL:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail="Website took too long to respond."
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )