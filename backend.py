from fastapi import FastAPI
import json
import os
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import re
from keybert import KeyBERT
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil

app = FastAPI(title="News Sentiment Analysis API")

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

def extract_bing_news(company_name):
    search_query = company_name.replace(" ", "+")
    url = f"https://www.bing.com/news/search?q={search_query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        news_articles = []
        seen_articles = set()

        for news_item in soup.find_all('div', class_=re.compile(r'news-card|newsitem')):
            try:
                title_element = news_item.find('a', class_='title')
                summary_element = news_item.find('div', class_='snippet')
                url = title_element['href'] if title_element else None

                if title_element and summary_element and url:
                    title = title_element.text.strip()
                    summary = summary_element.text.strip()

                    # Avoid duplicates based on title and summary
                    unique_key = (title, summary)
                    if unique_key not in seen_articles:
                        seen_articles.add(unique_key)
                        news_articles.append({
                            'title': title,
                            'summary': summary,
                            'url': url
                        })

            except Exception as e:
                print(f"Error processing news item: {e}")
                continue

        return news_articles[:10]  # Limit to top 10

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Bing News: {e}")
        return []

@app.get("/analyze")
def analyze_news(company_name: str):
    news_articles = extract_bing_news(company_name)

    if not news_articles:
        return {
            "Company": company_name,
            "Articles": [],
            "Comparative Sentiment Score": {},
            "Final Sentiment Analysis": "No news articles found.",
            "Audio": ""
        }

    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
    kw_model = KeyBERT()

    report = {
        "Company": company_name,
        "Articles": [],
        "Comparative Sentiment Score": {
            "Sentiment Distribution": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "Coverage Differences": [],
            "Topic Overlap": {}
        },
        "Final Sentiment Analysis": "",
        "Audio": ""
    }

    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    all_topics = []

    for article in news_articles:
        sentiment_result = sentiment_pipeline(article['summary'])
        sentiment_label = sentiment_result[0]['label'].upper()

        # Normalize sentiment to "Positive", "Negative", or "Neutral"
        if sentiment_label == "POSITIVE":
            sentiment_label = "Positive"
        elif sentiment_label == "NEGATIVE":
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        sentiment_distribution[sentiment_label] += 1

        # Smart summary length handling
        input_length = len(article['summary'].split())
        summary_length = max(20, min(60, input_length // 2))
        summary = summarization_pipeline(article['summary'], max_length=summary_length, min_length=20, do_sample=False)[0]['summary_text']

        # Extracting top 3 topics
        topics = kw_model.extract_keywords(article['summary'], keyphrase_ngram_range=(1, 2), stop_words='english')
        topics = [t[0] for t in topics[:3]]  # Get meaningful topics
        all_topics.append(set(topics))

        report["Articles"].append({
            "Title": article['title'],
            "Summary": summary,
            "Sentiment": sentiment_label,
            "Topics": topics
        })

    report["Comparative Sentiment Score"]["Sentiment Distribution"] = sentiment_distribution

    # Generate comparative insights
    positive_articles = [a for a in report["Articles"] if a["Sentiment"] == "Positive"]
    negative_articles = [a for a in report["Articles"] if a["Sentiment"] == "Negative"]

    for pos_article in positive_articles[:1]:  # Limit to 1 comparison for brevity
        for neg_article in negative_articles[:1]:
            comparison = {
                "Comparison": f"'{pos_article['Title']}' highlights a positive outlook, whereas '{neg_article['Title']}' raises concerns.",
                "Impact": "The contrasting narratives reflect both growth potential and risks for the company."
            }
            report["Comparative Sentiment Score"]["Coverage Differences"].append(comparison)

    # Identify topic overlap
    if all_topics:
        common_topics = set.intersection(*all_topics) if len(all_topics) > 1 else list(all_topics[0])
        unique_topics = [list(topics - common_topics) for topics in all_topics]

        report["Comparative Sentiment Score"]["Topic Overlap"] = {
            "Common Topics": list(common_topics),
            "Unique Topics in Article 1": unique_topics[0] if len(unique_topics) > 0 else [],
            "Unique Topics in Article 2": unique_topics[1] if len(unique_topics) > 1 else []
        }

    # Final Sentiment Conclusion
    positive, negative, neutral = sentiment_distribution.values()

    if positive > negative:
        final_sentiment = f"{company_name}'s latest news coverage is mostly positive. Potential stock growth expected."
    elif negative > positive:
        final_sentiment = f"{company_name}'s latest news coverage is mostly negative. Potential stock decline expected."
    else:
        final_sentiment = f"{company_name}'s latest news coverage is mostly neutral. Stock outlook remains uncertain."

    report["Final Sentiment Analysis"] = final_sentiment

    # Generate Hindi Audio Summary using deep_translator
    translator = GoogleTranslator(source='auto', target='hi')
    hindi_summary = translator.translate(final_sentiment)
    tts = gTTS(text=hindi_summary, lang='hi')
    audio_filename = "static/hindi_summary.mp3"
    os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
    tts.save(audio_filename)
    report["Audio"] = "/audio"

    return report

@app.get("/audio")
def get_audio():
    return FileResponse("static/hindi_summary.mp3", media_type="audio/mpeg")

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Sentiment Analysis API", 
            "endpoints": {
                "GET /analyze?company_name=Apple": "Analyze news for a company",
                "GET /audio": "Get the latest Hindi audio summary"
            }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)