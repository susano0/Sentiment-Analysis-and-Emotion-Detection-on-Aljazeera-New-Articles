import json
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import numpy as np
from scipy.special import softmax
import re
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import argparse

MODEL = ""
data = []

'''
1. Processing data - tokenizing and creating BERT embeddings
2. Preditioins using pretrained BERT models

Input: Model Name
Output: probability of each category for all input data
'''


def text_Analysis():
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    scores = []
    for d in tqdm(range(len(data))):
        text = data[d]["Text"]
        encoded_input = tokenizer(
            text,
            return_tensors='pt',
            max_length=512,
            truncation=True)
        output = model(**encoded_input)
        score = output[0][0].detach().numpy()
        score = softmax(score)
        scores.append(score)
    return scores


'''
1. Printing probability of each article

Input: Model and prediction array
'''


def print_results(scores):
   # Print labels and scores
    config = AutoConfig.from_pretrained(MODEL)
    for d, score in enumerate(scores):
        ranking = np.argsort(score)
        ranking = ranking[::-1]
        print(data[d]["Heading"])
        for i in range(score.shape[0]):
            l = config.id2label[ranking[i]]
            s = score[ranking[i]]
            print(f"{i+1}) {l} {np.round(float(s), 4)}")


'''
1. Plotting pie chart and saving the figure
'''


def plot_pie(scores, title, rows=5, cols=2, height=2000, width=1300):
    # Sanity Check
    if rows * cols < len(data):
        rows = len(data) // cols
        if len(data) % cols:
            rows += 1

    config = AutoConfig.from_pretrained(MODEL)
    fig = make_subplots(rows=rows,
                        cols=cols,
                        subplot_titles=[d["Heading"] for d in data],
                        specs=[[{"type": "pie"}] * cols for _ in range(rows)])

    for i in tqdm(range(len(scores))):
        fig.add_trace(
            go.Pie(values=scores[i], labels=list(config.id2label.values())),
            row= i // cols + 1, col = i % cols + 1)
    fig.update_layout(height=height, width=width,
                      title_text=title)

    fig.write_image(f"{title}.png")

    plotly.offline.plot(fig, filename=f"{title}.html")

    fig.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default="Recent_10_Articles.json")
    parser.add_argument('--analysis', type=str, default="sentiment")
    args = parser.parse_args()
    global data
    global MODEL
    # Reading Data
    with open(args.path) as f:
        data = json.load(f)

    # Bert Models for sentiment and emotion detection
    if args.analysis == "emotion":
        MODEL = "j-hartmann/emotion-english-distilroberta-base"  # Emotion Detection
        title = "Emotion Detection on News Articles"
    else:
        MODEL = "distilbert-base-uncased-finetuned-sst-2-english"  # Sentiment analysis
        title = "Sentiment Analysis on News Articles"

    scores = text_Analysis()  # Predictions

    print_results(scores)  # Printing results

    plot_pie(scores, title=title)


if __name__ == "__main__":
    main()
