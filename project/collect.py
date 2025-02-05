# from newspaper import Article, build
# from categorize_text import classify_text_domain

# # Dictionary to hold processed articles.
# # Key: article URL, Value: dict with article details.
# visited_articles = {}

# def categorize_articles(all_links):
#     print("collect was called")
#     for url in all_links:
#         try:
#             # print("collect was called and links were processed ")
#             # Build the source and extract all article links.
#             source = build(url, memoize_articles=False)  # Prevent caching issues
            
#             for article in source.articles:
#                 link = article.url
#                 # print(link)
#                 # Filter valid articles using substring checks.
#                 if ("articleshow" in link):
#                     print(link)
#                     #  and 
#                     # any(domain in link for domain in ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"])):
                    
#                     # Process only if not already processed.
#                     if link not in visited_articles:
#                         try:
#                             print("collect was called and links were processed ")

#                             article.download()
#                             article.parse()
#                             text = article.text
                            
#                             # Classify the article based on its text.
#                             domain = classify_text_domain(text)
                            
#                             # Store the processed article data.
#                             visited_articles[link] = {
#                                 "url": link,
#                                 "domain": domain,
#                                 "text": text,
#                                 "title": article.title,
#                                 "top_image": article.top_image
#                             }
                            
#                             print(f"{link} → {domain}")
                            
#                         except Exception as e:
#                             print(f"Error processing article {link}: {e}")
#                             continue  # Skip to the next article

#         except Exception as e:
#             print(f"Error accessing {url}: {e}")
#             continue  # Skip to the next source

#     # Organize articles by category.
#     domain_lists = {category: [] for category in ['India', 'World', 'Business', 'Technology', 'Sports']}
    
#     for article_data in visited_articles.values():
#         # Only add articles whose domain matches one of the expected categories.
#         domain = article_data["domain"]
#         if domain in domain_lists:
#             domain_lists[domain].append(article_data)

#     return domain_lists

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
#                         # visited_links[link] = domain


#                         #                             # Store the processed article data.
#                         visited_links[link] = {
#                             "url": link,
#                             "domain": domain,
#                             "text": text,
#                             "title": article.title,
#                             "top_image": article.top_image
#                         }
                        
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

#     # for link, domain in visited_links.items():
#     #     domain_lists[domain].append(link)

#     for article_data in visited_links.values():
#         # Only add articles whose domain matches one of the expected categories.
#         domain = article_data["domain"]
#         if domain in domain_lists:
#             domain_lists[domain].append(article_data)
    
#     return domain_lists



import requests
from bs4 import BeautifulSoup
from newspaper import Article
from categorize_text import classify_text_domain

visited_links = {}

def categorize_articles(all_links):
    
    session = requests.Session()

    #Define domain keywords for filtering once
    domain_keywords = ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"]

    for url in all_links:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue

        # Parse the fetched HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Iterate through all anchor tags with an href attribute
        for article_tag in soup.find_all('a', href=True):
            link = article_tag['href']
            # Filter: Link must be from Times of India, include "articleshow", and contain one of the domain keywords
            if (link.startswith("https://timesofindia.indiatimes.com/") and 
                "articleshow" in link and 
                any(keyword in link for keyword in domain_keywords)):
                
                # Process the link only if not already visited
                if link not in visited_links:
                    try:
                        article = Article(link)
                        article.download()
                        article.parse()
                        text = article.text
                        
                        # Classify the article based on its text    
                        domain = classify_text_domain(text)
                        
                        # Save the article details in the visited_links dictionary
                        visited_links[link] = {
                            "url": link,
                            "domain": domain,
                            "text": text,
                            "title": article.title,
                            "top_image": article.top_image
                        }
                        
                        print(f"{link} → {domain}")
                    
                    except Exception as e:
                        print(f"Error processing article from {link}: {e}")
                        continue  # Move to the next article

    # 4. Use dictionary comprehension to initialize the domain lists
    domain_lists = {category: [] for category in ['India', 'World', 'Business', 'Technology', 'Sports']}
    
    # Organize the articles based on their classified domain
    for article_data in visited_links.values():
        domain = article_data["domain"]
        if domain in domain_lists:
            domain_lists[domain].append(article_data)
    
    return domain_lists
