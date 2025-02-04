# import os.path
# import csv
# from bs4 import BeautifulSoup
# from newspaper import Article
# from gensum import text_summarizer
# from main2 import categorize_articles_new
# from pathlib import Path

# # Function to download and parse articles, and save data to CSV
# def download_and_save_articles(links_list, csv_file):
#     article_links = []
#     article_text = []
#     article_summary = []
#     article_titles = []
#     article_img = []
#     total = 0

#     for link in links_list:
#         try:
#             article = Article(link)
#             article.download()
#             article.parse()
#             article.nlp()
#             text = article.text
#             summary = text_summarizer(text) #from gensum.py

#             # Find img src
#             # img_src = None
#             # img_tags = BeautifulSoup(article.html, 'html.parser').find_all('img')
#             # for img_tag in img_tags:
#             #     src = img_tag.get('src', '')
#             #     alt = img_tag.get('alt', '')
#             #     fetchpriority = img_tag.get('fetchpriority', '')
#             #     if "static.toiimg." in src and alt != "TOI logo" and fetchpriority == "high":
#             #         img_src = src
#             #         break

#             img_src = article.top_image  # Extracts the top image


#             # Check if all fields are valid and not null
#             if all(article.title not in article_titles and field is not None and isinstance(field, str) and field.strip() for field in [link, text, summary, img_src]):
#                 article_img.append(img_src)
#                 article_links.append(link)
#                 article_text.append(text)
#                 article_titles.append(article.title)  # Domain name as title
#                 article_summary.append(summary)
#                 total += 1
#                 print(total)

#             if total >= 40:
#                 break

#         except Exception as e:
#             print(f"Error downloading article from {link}   : {e}")
#             continue  # Continue with the next iteration of the loop

#     # Save data to CSV
#     if article_titles:
#         if os.path.exists(csv_file):
#             file_size = os.path.getsize(csv_file)
#             if file_size == 0:
#                 with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(['Article Title', 'Article Link', 'Article Text', 'Article Summary', 'Article Image'])
#                     for i in range(len(article_titles)):
#                         writer.writerow([article_titles[i], article_links[i], article_text[i], article_summary[i], article_img[i]])
#                 print("Data has been saved to:", csv_file)



# csv_folder = Path(__file__).resolve().parent  # Get the directory of the script

# # Define CSV file paths
# info_files = {
#     0: csv_folder/'india.csv',
#     1: csv_folder/'world.csv',
#     2: csv_folder/'business.csv',
#     3: csv_folder/'tech.csv',
#     4: csv_folder/'sports.csv'
# }



import pandas as pd
from gensum import text_summarizer
from collect import categorize_articles
from pathlib import Path

# Function to process already-downloaded articles, generate summaries, and save to CSV.
def process_and_save_articles(articles_data, csv_file):
    article_links = []
    article_text = []
    article_summary = []
    article_titles = []
    article_img = []
    total = 0

    for article in articles_data:
        try:
            text = article["text"]
            # Generate summary using gensum's text_summarizer.
            summary = text_summarizer(text)
            
            # Validate fields (here you can add further validations if needed).
            if all([article["url"], text, summary, article["top_image"]]) and article["title"] not in article_titles:
                article_links.append(article["url"])
                article_text.append(text)
                article_titles.append(article["title"])
                article_img.append(article["top_image"])
                article_summary.append(summary)
                total += 1
                print(f"Collected {total}: {article['title']}")

            if total >= 20:  # Stop after collecting 20 articles per category.
                break

        except Exception as e:
            print(f"Error processing article {article['url']}: {e}")
            continue

    # Create a DataFrame and save the data to CSV.
    df = pd.DataFrame({
        'Article Title': article_titles,
        'Article Link': article_links,
        'Article Text': article_text,
        'Article Summary': article_summary,
        'Article Image': article_img
    })
    df.to_csv(csv_file, index=False, encoding='utf-8')
    print("Data has been saved to:", csv_file)


# Define CSV file paths relative to the current file.
csv_folder = Path(__file__).resolve().parent
info_files = {
    "India": csv_folder / 'data/india.csv',
    "World": csv_folder / 'data/world.csv',
    "Business": csv_folder / 'data/business.csv',
    "Technology": csv_folder / 'data/tech.csv',
    "Sports": csv_folder / 'data/sports.csv'
}

# List of URLs to scrape.
all_links = [
    "https://timesofindia.indiatimes.com/india",
    "https://timesofindia.indiatimes.com/world",
    "https://timesofindia.indiatimes.com/business",
    "https://timesofindia.indiatimes.com/technology",
    "https://timesofindia.indiatimes.com/sports"
]

def start_new():
    # Get the categorized articles (each article has already been processed once).
    domain_lists = categorize_articles(all_links)
    
    # For each category, process the articles and save to CSV.
    for category, filepath in info_files.items():
        if category in domain_lists:
            process_and_save_articles(domain_lists[category], filepath)

    print("\n\nApp ready for display")

# To run the process:
if __name__ == "__main__":
    start_new()
