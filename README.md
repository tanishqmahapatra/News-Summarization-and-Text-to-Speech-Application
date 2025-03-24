# 📰 News Summarization & Text-to-Speech (TTS) Application

## 📌 Objective
This web-based application extracts key details from multiple news articles related to a given company, performs **sentiment analysis**, conducts **comparative analysis**, and generates **text-to-speech (TTS) output in Hindi**. Users can input a company name and receive a structured sentiment report with audio output.

---

## 🌟 Features
✅ **News Extraction:** Scrapes at least 10 unique news articles using `BeautifulSoup` (Only non-JavaScript web pages are considered).  
✅ **Sentiment Analysis:** Determines whether each article is **Positive, Negative, or Neutral**.  
✅ **Comparative Analysis:** Highlights sentiment differences across articles and extracts common vs. unique topics.  
✅ **Hindi Text-to-Speech:** Converts summarized news sentiment into Hindi speech using an open-source TTS model.  
✅ **Interactive UI:** Built with `Gradio/Streamlit` to accept company name input and display results.  
✅ **API-Based Architecture:** Frontend and backend communicate via API calls for efficient data processing.  
✅ **Deployment:** The application is hosted on Hugging Face Spaces for easy access and testing.

---

## 🎯 API Architecture
The application follows a **modular API-based design**, where the frontend makes API calls to fetch data and perform operations.

### 🔹 **Frontend API Calls**
- The frontend (`Gradio` or `Streamlit`) **sends requests** to fetch news articles, perform sentiment analysis, and generate TTS.
- Calls are made via **AJAX requests** or `requests` library.

### 🔹 **Backend API Calls**
- The backend is deployed on **Render** and exposes REST API endpoints.
- API calls handle **news scraping, sentiment analysis, and TTS conversion**.
- Base Backend URL: [`https://news-summarization-and-text-to-speech-cok7.onrender.com/`](https://news-summarization-and-text-to-speech-cok7.onrender.com/)

### 🔹 **Hugging Face Deployment**
- Frontend is deployed on Hugging Face Spaces - https://huggingface.co/spaces/tanishq0907/News_Summarization

---

## 📥 Input Format
User enters a **company name** (via dropdown or text input).

### Example Input:
```
Company Name: Tesla
```

---

## 📤 Expected Output
The application returns a **structured sentiment report** in JSON format and an **audio file** summarizing the news in Hindi.

### Example Output:
```json
{
    "Company": "Tesla",
    "Articles": [
        {
            "Title": "Tesla's New Model Breaks Sales Records",
            "Summary": "Tesla's latest EV sees record sales in Q3...",
            "Sentiment": "Positive",
            "Topics": ["Electric Vehicles", "Stock Market", "Innovation"]
        },
        {
            "Title": "Regulatory Scrutiny on Tesla's Self-Driving Tech",
            "Summary": "Regulators have raised concerns over Tesla’s self-driving software...",
            "Sentiment": "Negative",
            "Topics": ["Regulations", "Autonomous Vehicles"]
        }
    ],
    "Comparative Sentiment Score": {
        "Sentiment Distribution": {
            "Positive": 1,
            "Negative": 1,
            "Neutral": 0
        },
        "Coverage Differences": [
            {
                "Comparison": "Article 1 highlights Tesla's strong sales, while Article 2 discusses regulatory issues.",
                "Impact": "The first article boosts confidence in Tesla's market growth, while the second raises concerns about future regulatory hurdles."
            }
        ],
        "Topic Overlap": {
            "Common Topics": ["Electric Vehicles"],
            "Unique Topics in Article 1": ["Stock Market", "Innovation"],
            "Unique Topics in Article 2": ["Regulations", "Autonomous Vehicles"]
        }
    },
    "Final Sentiment Analysis": "Tesla’s latest news coverage is mostly positive. Potential stock growth expected.",
    "Audio": "[Play Hindi Speech]"
}
```

---

## 🛠️ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/news-summarization-tts.git
cd news-summarization-tts
```
### **2️⃣ Install Dependencies**
Using `pip`:
```bash
pip install -r requirements.txt
```
Using `conda`:
```bash
conda env create -f environment.yml
conda activate news-summarization
```
### **3️⃣ Run the Application**
```bash
python app.py
```
The application will be available at `http://localhost:8501`.

---

## 📡 API Development
### **Backend Endpoints:**
| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/fetch_news/<company>` | Fetches news articles related to the company |
| `POST` | `/analyze_sentiment` | Performs sentiment analysis on fetched news |
| `POST` | `/generate_tts` | Converts text summary into Hindi speech |

Use `Postman` or `cURL` to test API endpoints.

---

## 🔍 Assumptions & Limitations
### ✅ **Assumptions:**
- The news sources do not require JavaScript rendering (ensuring `BeautifulSoup` works correctly).
- Articles contain relevant content related to the company.
- Sentiment scores are based on pre-trained NLP models.
- Hindi TTS output may slightly vary in pronunciation accuracy.

### ❌ **Limitations:**
- **JavaScript-heavy websites cannot be scraped** (e.g., dynamically loaded content via React/Vue).
- **Sentiment analysis is not 100% accurate**, as it depends on context and dataset training.
- **Comparative analysis may be skewed** if articles focus on specific events disproportionately.
- **TTS model may have limitations** in handling technical terms and proper names in Hindi.
- **Limited language support:** Currently, sentiment analysis is in English, while TTS is in Hindi.

---

## 🚀 Deployment Links
✅ **Backend API:** [`https://news-summarization-and-text-to-speech-cok7.onrender.com/`](https://news-summarization-and-text-to-speech-cok7.onrender.com/)  
✅ **Frontend (Hugging Face Spaces):** (https://huggingface.co/spaces/tanishq0907/News_Summarization)

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🤝 Contributing
Feel free to **fork** the repository, submit PRs, or suggest improvements!

💡 **Suggestions & Feedback?** Open an issue or reach out! 🚀

