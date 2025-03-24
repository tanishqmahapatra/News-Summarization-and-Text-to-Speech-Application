import gradio as gr
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API Configuration
API_URL = "http://127.0.0.1:8000/analyze"
AUDIO_URL = "http://127.0.0.1:8000/audio"

# Theme configuration
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="indigo",
    neutral_hue="slate"
)

def get_news_sentiment(company_name):
    if not company_name.strip():
        return (
            gr.update(visible=True, value="Please enter a company name"), 
            None, None, None, None, None, None
        )
    
    try:
        response = requests.get(API_URL, params={"company_name": company_name}, timeout=60)
        
        if response.status_code != 200:
            return (
                gr.update(visible=True, value=f"Error: API returned status code {response.status_code}"),
                None, None, None, None, None, None
            )
        
        data = response.json()
        
        # Error handling for empty data
        if not data.get("Articles"):
            return (
                gr.update(visible=True, value="No news articles found for this company."),
                None, None, None, None, None, None
            )
        
        # Format articles as markdown
        articles_md = ""
        for i, article in enumerate(data["Articles"]):
            sentiment_color = {
                "Positive": "🟢 ",
                "Negative": "🔴 ",
                "Neutral": "🔵 "
            }.get(article["Sentiment"], "")
            
            articles_md += f"### {i+1}. {sentiment_color}{article['Title']}\n\n"
            articles_md += f"**Summary:** {article['Summary']}\n\n"
            articles_md += f"**Sentiment:** {article['Sentiment']}\n\n"
            articles_md += f"**Topics:** {', '.join(article['Topics'])}\n\n"
            articles_md += "---\n\n"
        
        # Prepare sentiment distribution for visualization
        sentiment_dist = data["Comparative Sentiment Score"]["Sentiment Distribution"]
        sentiment_df = pd.DataFrame({
            'Sentiment': list(sentiment_dist.keys()),
            'Count': list(sentiment_dist.values())
        })
        
        # Create sentiment pie chart
        fig_pie = px.pie(
            sentiment_df, 
            values='Count', 
            names='Sentiment',
            color='Sentiment',
            color_discrete_map={
                'Positive': '#4CAF50',
                'Negative': '#F44336',
                'Neutral': '#2196F3'
            },
            hole=0.4,
            title="Sentiment Distribution"
        )
        fig_pie.update_layout(legend_title_text='', margin=dict(t=30, b=0, l=0, r=0))
        
        # Prepare topic data
        common_topics = data["Comparative Sentiment Score"]["Topic Overlap"].get("Common Topics", [])
        common_topics_str = ", ".join(common_topics) if common_topics else "No common topics found"
        
        # Get comparison insights
        comparisons = data["Comparative Sentiment Score"]["Coverage Differences"]
        comparison_text = "\n\n".join([f"* {comp['Comparison']}\n* {comp['Impact']}" for comp in comparisons]) if comparisons else "No comparative insights available"
        
        # Get timestamp
        timestamp = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        
        # Create summary card
        summary_html = f"""
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background-color: #f8f9fa;">
            <h3 style="margin-top: 0; color: #1a73e8;">Analysis Summary</h3>
            <p><strong>Company:</strong> {company_name}</p>
            <p><strong>Final Analysis:</strong> {data["Final Sentiment Analysis"]}</p>
            <p><strong>Articles Analyzed:</strong> {len(data["Articles"])}</p>
            <p><strong>Common Topics:</strong> {common_topics_str}</p>
            <p><strong>Generated on:</strong> {timestamp}</p>
        </div>
        """
        
        # Return all components
        return (
            gr.update(visible=False, value=""),
            articles_md,
            fig_pie,
            summary_html,
            comparison_text,
            data["Final Sentiment Analysis"],
            AUDIO_URL
        )
        
    except Exception as e:
        return (
            gr.update(visible=True, value=f"Error: {str(e)}"),
            None, None, None, None, None, None
        )

with gr.Blocks(theme=theme, title="Financial News Sentiment Analyzer") as demo:
    gr.Markdown(
        """
        # 📰 Financial News Sentiment Analyzer
        
        Analyze the sentiment of news articles for any company and get insights into market perception.
        The analysis includes sentiment distribution, topic analysis, and a Hindi audio summary.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=4):
            company_input = gr.Textbox(
                label="Enter Company Name",
                placeholder="Example: Apple, Microsoft, Tesla",
                info="Enter a publicly traded company name"
            )
        with gr.Column(scale=1):
            submit_button = gr.Button("Analyze", variant="primary")
    
    # Error display
    error_output = gr.Markdown(visible=False)
    
    with gr.Tabs():
        with gr.TabItem("News Articles"):
            articles_output = gr.Markdown(label="News Articles")
            
        with gr.TabItem("Sentiment Analysis"):
            with gr.Row():
                with gr.Column():
                    sentiment_chart = gr.Plot(label="Sentiment Distribution")
                with gr.Column():
                    summary_output = gr.HTML(label="Summary")
            
        with gr.TabItem("Comparative Insights"):
            comparison_output = gr.Markdown(label="Insights")
            
        with gr.TabItem("Audio Summary"):
            with gr.Row():
                with gr.Column():
                    sentiment_output = gr.Textbox(label="Overall Sentiment")
                with gr.Column():
                    audio_output = gr.Audio(label="Hindi Audio Summary")
    
    gr.Markdown(
        """
        ### How it works
        
        1. Enter a company name and click "Analyze"
        2. The system will fetch recent news articles about the company
        3. Each article is analyzed for sentiment (positive, negative, neutral)
        4. Topics are extracted from the articles
        5. A summary is generated with market implications
        6. A Hindi audio summary is provided for accessibility
        
        *Note: Analysis is based on recent news articles and should not be used as the sole basis for investment decisions.*
        """
    )
    
    submit_button.click(
        get_news_sentiment, 
        inputs=company_input, 
        outputs=[
            error_output,
            articles_output,
            sentiment_chart,
            summary_output,
            comparison_output,
            sentiment_output,
            audio_output
        ]
    )

if __name__ == "__main__":
    demo.launch()