
# Sentiment Analysis and Emotion Detection on Aljazeera New Articles

Created a pipeline that collects (via web scraping) and analyzes news articles from Aljazeera.
Web scraped 10 articles and performed sentiment analysis and emotion detection on them. 


## Installation

1. Create a conda virtual environment

```bash
conda create --name testenv --file requirements.txt 

conda activate testenv

conda install -c plotly plotly 

conda install -c plotly plotly_express

pip install kaleido==0.1.0post1

```
    
## Usage/Examples

Web Scraping 

param: numarticles (default: 10)

output: json file
```bash
python minds_lab_webscraping.py --numarticles 10
```
Text Analysis

param: 

path- path of json file 

analysis- sentiment (default)/ emotion

```bash
python minds_lab_sentiment_analysis.py --path Recent_10_Articles.json --analysis emotion

python minds_lab_sentiment_analysis.py --path Recent_10_Articles.json --analysis sentiment
```
## Data Format

 Header      | Description
------------ | -------------
Link         | Link of the article
Heading      | Article Heading
Sub Heading  | Article Sub Heading
Date         | Publishing Date
Text         | Main Article Content

## Results

Sentiment Analysis

| Category  | Percentage |
| ----------| ---------- |
| Positive  |    20%     |
| Nagative  |    80%     |

Emotion Detection

| Category  | Percentage |
| ----------| ---------- |
| Fear      |    20%     |
| Sadness   |    20%     |
| Neutral   |    50%     |
| Disgust   |    0%      |
| Anger     |    10%     |
| Surprise  |    0%      |
| Joy       |    0%      |

Total operation time: 1 minutes 
## Screenshots

![App Screenshot](https://github.com/susano0/Sentiment-Analysis-and-Emotion-Detection-on-Aljazeera-New-Articles/blob/main/Figures/Emotion%20Detection%20on%20News%20Articles.png)

![App Screenshot](https://github.com/susano0/Sentiment-Analysis-and-Emotion-Detection-on-Aljazeera-New-Articles/blob/main/Figures/Sentiment%20Analysis%20on%20News%20Articles.png)
