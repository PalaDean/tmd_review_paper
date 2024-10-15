import requests
import csv
import re
import time
import pandas as pd

# Replace with your actual API key
API_KEY = "bd4c3ec6c4cf2707a2dc4735525e9156"
FULL_TEXT_URL = "https://api.elsevier.com/content/article/doi/{}?APIKey={}&httpAccept=application/xml"

# Rate limiting parameters
REQUEST_DELAY = 2  # Time to wait between requests (in seconds)
MAX_RETRIES = 3    # Number of retries for failed requests

# Keywords to search for
KEYWORDS = ["Energy Plus", "EnergyPlus"]

# Function to fetch full text for a given DOI
def fetch_full_text(doi):
    url = FULL_TEXT_URL.format(doi, API_KEY)
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # Return the XML content of the article
    else:
        print(f"Failed to retrieve article {doi}: {response.status_code}")
        return None

# Function to count occurrences of keywords in the full text
def count_keyword_occurrences(text, keywords):
    count_dict = {keyword: 0 for keyword in keywords}
    for keyword in keywords:
        count_dict[keyword] = len(re.findall(r'\b{}\b'.format(keyword), text, flags=re.IGNORECASE))
    return count_dict

# Read the CSV file containing DOIs
def process_papers(csv_filename):
    results = []
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            doi = row['DOI']
            title = row['Title']
            journal = row['Journal']
            print(f"Fetching full text for DOI: {doi} - Title: {title}")
            
            retries = 0
            full_text = None
            
            # Retry logic in case of failed requests
            while retries < MAX_RETRIES:
                full_text = fetch_full_text(doi)
                if full_text:
                    break
                retries += 1
                print(f"Retrying... Attempt {retries}")
                time.sleep(REQUEST_DELAY)  # Rate limiting and retry delay
            
            if full_text:
                # Count keyword occurrences in the full text
                keyword_counts = count_keyword_occurrences(full_text, KEYWORDS)
                
                # If any keyword is found, add the journal to the results
                if any(count > 0 for count in keyword_counts.values()):
                    results.append({
                        'Journal': journal,
                        'DOI': doi,
                        'Title': title,
                        'Occurrences of Energy Plus': keyword_counts["Energy Plus"],
                        'Occurrences of EnergyPlus': keyword_counts["EnergyPlus"]
                    })
                print(f"Keyword occurrences: {keyword_counts}\n")
            else:
                print(f"Failed to retrieve full text for {doi} after {MAX_RETRIES} attempts.\n")
            
            # Respect rate limit between requests
            time.sleep(REQUEST_DELAY)
    
    return results

# Function to aggregate results by journal and calculate occurrences
def aggregate_results(results):
    df = pd.DataFrame(results)
    
    # Aggregate by Journal and count the number of articles per journal where Energy Plus or EnergyPlus occurred
    aggregated_df = df.groupby('Journal').agg({
        'Occurrences of Energy Plus': 'sum',
        'Occurrences of EnergyPlus': 'sum',
        'DOI': 'count'  # Count how many articles per journal
    }).rename(columns={'DOI': 'Number of Articles'})
    
    # Total occurrences of keywords in all articles
    aggregated_df['Total Occurrences'] = aggregated_df['Occurrences of Energy Plus'] + aggregated_df['Occurrences of EnergyPlus']
    
    return aggregated_df

# Main execution
if __name__ == "__main__":
    # Step 1: Process papers and collect results
    csv_filename = 'papers.csv'  # Replace with your actual CSV file
    results = process_papers(csv_filename)
    
    # Step 2: Aggregate results by journal
    aggregated_results = aggregate_results(results)
    
    # Step 3: Show the aggregated results
    print("\nAggregated Results by Journal:")
    print(aggregated_results)
    
    # Optionally, save the aggregated results to a CSV file
    aggregated_results.to_csv('aggregated_results.csv')
    print("\nAggregated results saved to 'aggregated_results.csv'")
