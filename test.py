import csv

# Read the CSV file containing DOIs
def process_papers(csv_filename):
    results = []
    
    # Open the CSV file
    with open(csv_filename, newline='', encoding='utf-8-sig') as csvfile:
        # Initialize the CSV DictReader
        reader = csv.DictReader(csvfile)
        
        # Print column headers for debugging purposes
        print(f"CSV Column Headers: {reader.fieldnames}")
        
        for row in reader:
            # Check if the row is empty (skip empty rows)
            if not row:
                continue
            
            # Print row contents to check data
            print(f"Processing row: {row}")
            
            # Ensure correct column names ('DOI', 'Title', 'Journal') exist
            if 'DOI' in row and 'Title' in row and 'Journal' in row:
                doi = row['DOI'].strip()      # Remove leading/trailing spaces
                title = row['Title'].strip()  # Remove leading/trailing spaces
                journal = row['Journal'].strip()  # Remove leading/trailing spaces
                print(f"Processing article with DOI: {doi}, Title: {title}, Journal: {journal}")
                
                # Add to results (you can process further or return this data)
                results.append({
                    'DOI': doi,
                    'Title': title,
                    'Journal': journal
                })
            else:
                print("Error: One or more required columns (DOI, Title, Journal) missing in the row")
    
    return results

# Main execution
if __name__ == "__main__":
    csv_filename = 'scopus_doi.csv'  # Replace with your CSV file
    processed_results = process_papers(csv_filename)
    
    print("\nProcessed Results:")
    for result in processed_results:
        print(result)
