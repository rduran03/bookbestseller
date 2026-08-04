import os
import pandas as pd

DATA_PATH = os.path.join("data", "bestsellers.csv")

def load_data(filepath: str) -> pd.DataFrame:
    """Loads CSV data into a Pandas DataFrame with initial sanity checks."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Dataset loaded successfully. Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Inspects nulls, drops duplicates, and ensures correct data types."""
    # Standardize column names 
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Drop duplicates if any
    initial_count = len(df)
    df = df.drop_duplicates()
    dedup_count = len(df)
    if initial_count != dedup_count:
        print(f"Removed {initial_count - dedup_count} duplicate rows.")

    # Fill or inspect missing values
    if df.isnull().sum().sum() > 0:
        print("Missing values detected per column:")
        print(df.isnull().sum())
        df = df.dropna()
    
    return df

def analyze_bestsellers(df: pd.DataFrame):
    """Runs core analytical queries on the cleaned dataset."""
    print("=" * 50)
    print(" AMAZON BESTSELLERS ANALYSIS ")
    print("=" * 50)

    # Displays Top 5 Most Reviewed Books
    print("\n--- Top 5 Most Reviewed Books ---")
    most_reviewed = df[['name', 'author', 'reviews', 'user_rating']].sort_values(
        by='reviews', ascending=False
    ).drop_duplicates(subset=['name']).head(5)
    print(most_reviewed.to_string(index=False))

    # Average Price, Rating, and Review Count
    print("\n--- Summary Statistics by Genre ---")
    genre_summary = df.groupby('genre').agg(
        total_books=('name', 'count'),
        avg_price=('price', 'mean'),
        avg_rating=('user_rating', 'mean'),
        avg_reviews=('reviews', 'mean')
    ).round(2)
    print(genre_summary)

    # Top 5 Authors with the Most Bestselling Appearances
    print("\n--- Top 5 Authors by Total Bestseller Appearances ---")
    top_authors = df['author'].value_counts().head(5)
    print(top_authors.to_string())

    # Price Extremes
    print("\n--- Price Highlights ---")
    most_expensive = df.loc[df['price'].idxmax()]
    print(f"Most Expensive Book: '{most_expensive['name']}' by {most_expensive['author']} (${most_expensive['price']:.2f})")
    
    zero_price_count = (df['price'] == 0).sum()
    print(f"Number of Free ($0) Bestsellers: {zero_price_count}")

# Report Generation
def export_summary(df: pd.DataFrame, output_path: str = "genre_summary.csv"):
    """Exports grouped analytical insights to a new CSV file."""
    summary = df.groupby(['genre', 'year']).agg(
        avg_price=('price', 'mean'),
        avg_rating=('user_rating', 'mean')
    ).reset_index()
    
    summary.to_csv(output_path, index=False)
    print(f"\nYearly genre summary successfully saved to '{output_path}'.")

# Main Execution Flow
if __name__ == "__main__":
    try:
        raw_df = load_data(DATA_PATH)
        cleaned_df = clean_data(raw_df)
        analyze_bestsellers(cleaned_df)
        export_summary(cleaned_df)
    except Exception as e:
        print(f"An error occurred during execution: {e}")