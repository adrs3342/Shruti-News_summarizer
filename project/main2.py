# import os.path
# import pandas as pd
# from bs4 import BeautifulSoup
# from newspaper import Article
# import requests
# from categorize_text import classify_text_domain


# visited_links = {}  # Dictionary to track visited links and their domains
# def categorize_articles(all_links):
   

#     for url in all_links:
#         response = requests.get(url)
#         web_page = response.text
#         soup = BeautifulSoup(web_page, 'html.parser')
#         for article_tag in soup.find_all('a', href=True):
#             link = article_tag['href']
#             # Check if the link starts with "https://timesofindia.indiatimes.com/" and contains "articleshow"
#             if (link.startswith("https://timesofindia.indiatimes.com/") and "articleshow" in link and any(domain in link for domain in ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"])):

#                 # Check if the link has been visited before
#                 if link not in visited_links:
#                     try:
#                         article = Article(link)
#                         article.download()
#                         article.parse()
#                         article.nlp()
#                         text = article.text
#                         domain = classify_text_domain(text)
                        
#                         # Store the link and its domain in the visited links dictionary
#                         visited_links[link] = domain
#                         print(link, " is ", domain) 
#                     except Exception as e:
#                         print(f"Error downloading article from {link}  : {e}\n")
#                         continue  # Continue with the next iteration of the loop

#     # Separate links based on their domains
#     domain_lists = {
#         'India': [],
#         'World': [],
#         'Business': [],
#         'Technology': [],
#         'Sports': []
#     }

#     for link, domain in visited_links.items():
#         domain_lists[domain].append(link)

    
#     return domain_lists





from newspaper import Article, build
from categorize_text import classify_text_domain

visited_links = {}  # Dictionary to track visited links and their domains

def categorize_articles(all_links):
    for url in all_links:
        try:
            # Build the source and extract all article links
            source = build(url, memoize_articles=False)  # Prevent caching issues
            
            for article in source.articles:
                link = article.url
                
                # Filter valid articles
                if ("articleshow" in link and 
                    any(domain in link for domain in ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"])):
                    
                    # Check if already processed
                    if link not in visited_links:
                        try:
                            article.download()
                            article.parse()
                            text = article.text

                            # Classify article
                            domain = classify_text_domain(text)
                            
                            # Store the classified article
                            visited_links[link] = domain
                            print(f"{link} → {domain}")
                            
                        except Exception as e:
                            print(f"Error processing article {link}: {e}")
                            continue  # Skip to the next article

        except Exception as e:
            print(f"Error accessing {url}: {e}")
            continue  # Skip to the next source

    # Organize links by category
    domain_lists = {category: [] for category in ['India', 'World', 'Business', 'Technology', 'Sports']}
    
    for link, domain in visited_links.items():
        domain_lists[domain].append(link)

    return domain_lists