import pandas as pd
import os

# Paths to processed files
BEHAVIORS_FILE = "data/processed/parsed_behaviors.csv"
NEWS_FILE = "data/processed/parsed_news.csv"
OUTPUT_FILE = "data/processed/session_data.csv"

def aggregate_user_sessions():
    # Load parsed behaviors and news
    behaviors = pd.read_csv(BEHAVIORS_FILE)
    news = pd.read_csv(NEWS_FILE)

    # Create a dictionary mapping News_ID to its features
    news_features = news.set_index('News_ID').to_dict(orient='index')

    session_rows = []

    # Iterate through each user session
    for _, row in behaviors.iterrows():
        user_id = row['User_ID']
        session_time = row['Time']
        clicked_articles = row['History']
        impressions = row['Impressions'].split(' ')

        # Compute user-specific features
        num_clicked = len(clicked_articles)
        diversity = len(set(clicked_articles))  # Number of unique articles clicked

        # Iterate through the impression articles for the session
        for impression in impressions:
            news_id, label = impression.split('-')  # Get article and click label (0 or 1)
            label = int(label)

            # Get features for the current article
            article_features = news_features.get(news_id, {})
            title_length = article_features.get('Title_Length', 0)
            category = article_features.get('Category', 'unknown')

            # Construct the feature row for this user-article interaction
            session_rows.append({
                'User_ID': user_id,
                'Session_Time': session_time,
                'Num_Clicked': num_clicked,
                'Diversity': diversity,
                'Article_ID': news_id,
                'Title_Length': title_length,
                'Category': category,
                'Label': label  # Whether the article was clicked or not
            })

    # Convert to DataFrame and save to CSV
    session_df = pd.DataFrame(session_rows)
    session_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Session-level data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    print("Aggregating session-level features...")
    aggregate_user_sessions()
    print("Aggregation completed.")

