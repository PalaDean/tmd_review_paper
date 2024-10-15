import requests
import csv
import re
import time
import pandas as pd
import os
from keyword_groups import KEYWORD_GROUPS  # Import the keyword groups from the separate file


# Retrieve the API key from environment variables
API_KEY = os.getenv("SCOPUS_API_KEY")
FULL_TEXT_URL = "https://api.elsevier.com/content/article/doi/{}?APIKey={}&httpAccept=application/xml"

if API_KEY is None:
    raise ValueError("No API key found! Please set the SCOPUS_API_KEY environment variable.")


# Rate limiting parameters
REQUEST_DELAY = 2  # Time to wait between requests (in seconds)
MAX_RETRIES = 3    # Number of retries for failed requests

# Function to fetch full text for a given DOI
def fetch_full_text(doi):
    url = FULL_TEXT_URL.format(doi, API_KEY)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # Return the XML content of the article
    else:
        print(f"Failed to retrieve article {doi}: {response.status_code}")
        return None

# Function to check if any keyword variation occurs at least once in the full text
def check_keyword_occurrences(text, keyword_groups):
    flag_dict = {keyword: 0 for keyword in keyword_groups}  # Initialize to 0 (no occurrence)

    # Iterate over each keyword and its variations
    for keyword, variations in keyword_groups.items():
        # Create a regex pattern that matches any variation of the keyword
        pattern = "|".join(re.escape(variation) for variation in variations)
        
        # If any variation is found in the text, set the flag to 1 (occurs at least once)
        if re.search(pattern, text, flags=re.IGNORECASE):
            flag_dict[keyword] = 1
    
    return flag_dict

# Read the CSV file containing DOIs
def process_papers(csv_filename):
    results = []
    with open(csv_filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        print(f"CSV Column Headers: {reader.fieldnames}")
        
        for row in reader:
            if not row:
                continue
            
            doi = row['DOI'].strip()      # Strip spaces to clean up DOIs
            title = row['Title'].strip()  # Strip spaces to clean up Titles
            journal = row['Journal'].strip()  # Strip spaces to clean up Journals
            print(f"Fetching full text for DOI: {doi} - Title: {title}")
            
            retries = 0
            full_text = None
            
            while retries < MAX_RETRIES:
                full_text = fetch_full_text(doi)
                if full_text:
                    break
                retries += 1
                print(f"Retrying... Attempt {retries}")
                time.sleep(REQUEST_DELAY)  # Rate limiting and retry delay
            
            if full_text:
                # Check keyword occurrences in the full text (flag at least one occurrence)
                keyword_flags = check_keyword_occurrences(full_text, KEYWORD_GROUPS)
                
                # If any keyword occurs at least once, add the journal to the results
                if any(flag == 1 for flag in keyword_flags.values()):
                    results.append({
                        'DOI': doi,
                        'Title': title,
                        'Journal': journal,
                        **keyword_flags  # Add keyword flags to the result dictionary
                    })
                print(f"Keyword flags: {keyword_flags}\n")
            else:
                print(f"Failed to retrieve full text for {doi} after {MAX_RETRIES} attempts.\n")
            
            time.sleep(REQUEST_DELAY)
    
    return results

# Function to aggregate results by keyword across journals
def aggregate_results(results):
    df = pd.DataFrame(results)
    
    # Aggregate by counting the number of journals that mention each keyword at least once
    keyword_columns = list(KEYWORD_GROUPS.keys())
    
    # Calculate the number of unique journals where each keyword was mentioned
    aggregated_df = df.groupby('Journal').agg({**{keyword: 'max' for keyword in keyword_columns}, 'DOI': 'count'}).rename(columns={'DOI': 'Number of Articles'})
    
    # Count how many journals mentioned each keyword at least once
    keyword_journal_counts = {keyword: aggregated_df[keyword].sum() for keyword in keyword_columns}
    
    # Create a DataFrame with the count of journals mentioning each keyword
    keyword_summary_df = pd.DataFrame(keyword_journal_counts.items(), columns=['Keyword', 'Number of Journals Mentioned'])
    
    return keyword_summary_df

# Main execution
if __name__ == "__main__":
    # Step 1: Process papers and collect results
    csv_filename = 'papers.csv'  # Replace with your actual CSV file
    results = process_papers(csv_filename)
    
    # Step 2: Aggregate results by keyword
    aggregated_results = aggregate_results(results)
    
    # Step 3: Show the aggregated results
    print("\nAggregated Results by Keyword:")
    print(aggregated_results)
    
    # Optionally, save the aggregated results to a CSV file
    aggregated_results.to_csv('aggregated_results_by_keyword.csv')
    print("\nAggregated results saved to 'aggregated_results_by_keyword.csv'")