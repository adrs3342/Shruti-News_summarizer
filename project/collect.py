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