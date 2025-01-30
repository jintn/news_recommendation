import pandas as pd
import os 

BEHAVIORS_FILE = "data/raw/behaviors.tsv"
NEWS_FILE = "data/raw/news.tsv"
PROCESSED_PATH = "data/processed/"

os.makedirs(PROCESSED_PATH, exist_ok=True)

def parse_behaviors():

    behaviors = pd.read_csv(BEHAVIORS_FILE, sep='\t', header=None,
                            names=['Impression_ID', 'User_ID', 'Time', 'History', 'Impressions'])

    # Convert time to datetime format
    behaviors['Time'] = pd.to_datetime(behaviors['Time'])

    # Split history into lists of clicked articles
    behaviors['History'] = behaviors['History'].apply(lambda x: x.split() if isinstance(x, str) else [])

    # Save the parsed behaviors
    behaviors.to_csv(os.path.join(PROCESSED_PATH, 'parsed_behaviors.csv'), index=False)
    print("Behaviors file parsed and saved.")
    return behaviors

def parse_news():
    # Read news file with tab separator
    news = pd.read_csv(NEWS_FILE, sep='\t', header=None,
                       names=['News_ID', 'Category', 'SubCategory', 'Title', 'Abstract', 'URL', 'Title_Entities', 'Abstract_Entities'])

    # Optionally, process text features (e.g., tokenization, embeddings)
    news['Title_Length'] = news['Title'].apply(lambda x: len(str(x).split()))

    # Save parsed news data
    news.to_csv(os.path.join(PROCESSED_PATH, 'parsed_news.csv'), index=False)
    print("News file parsed and saved.")
    return news


if __name__ == "__main__":
    print("Starting preprocessing...")
    behaviors = parse_behaviors()
    news = parse_news()
    print("Preprocessing completed.")