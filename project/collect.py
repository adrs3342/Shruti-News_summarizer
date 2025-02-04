from newspaper import Article, build
from categorize_text import classify_text_domain

# Dictionary to hold processed articles.
# Key: article URL, Value: dict with article details.
visited_articles = {}

def categorize_articles(all_links):
    for url in all_links:
        try:
            # Build the source and extract all article links.
            source = build(url, memoize_articles=False)  # Prevent caching issues
            
            for article in source.articles:
                link = article.url
                
                # Filter valid articles using substring checks.
                if ("articleshow" in link and 
                    any(domain in link for domain in ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"])):
                    
                    # Process only if not already processed.
                    if link not in visited_articles:
                        try:
                            article.download()
                            article.parse()
                            text = article.text
                            
                            # Classify the article based on its text.
                            domain = classify_text_domain(text)
                            
                            # Store the processed article data.
                            visited_articles[link] = {
                                "url": link,
                                "domain": domain,
                                "text": text,
                                "title": article.title,
                                "top_image": article.top_image
                            }
                            
                            print(f"{link} → {domain}")
                            
                        except Exception as e:
                            print(f"Error processing article {link}: {e}")
                            continue  # Skip to the next article

        except Exception as e:
            print(f"Error accessing {url}: {e}")
            continue  # Skip to the next source

    # Organize articles by category.
    domain_lists = {category: [] for category in ['India', 'World', 'Business', 'Technology', 'Sports']}
    
    for article_data in visited_articles.values():
        # Only add articles whose domain matches one of the expected categories.
        domain = article_data["domain"]
        if domain in domain_lists:
            domain_lists[domain].append(article_data)

    return domain_lists
