import requests
import newspaper
from bs4 import BeautifulSoup
from Summarize_Function import summarize



def get_articles(query):

    url = 'https://newsapi.org/v2/everything'
    params = {'q': query, 'sortBy': 'relevancy', 'apiKey': '7189a40a8cc3490993d2073174f15610', 'pageSize': 5, 'excludeDomains': 'engadget.com'}
   
    response = requests.get(url, params=params)
    content = response.json()
    
    articles = content['articles']
    all_articles = []
    
    for article in articles:

        article_title = article['title']
        article_url = article['url']
        article_text = article.get('description', '')

        try:
            article_obj = newspaper.Article(article_url)
            article_obj.download()
            article_obj.parse()

            if "bbc.co.uk" in article_url:
                soup = BeautifulSoup(article_obj.html, 'html.parser')
                article_text = ""
                
                for text_block in soup.find_all('div', {'data-component': 'text-block'}):
                    article_text += text_block.get_text().strip() + "\n"
            
            else:
                article_text = article_obj.text
        
        except Exception as e:
            print(f"Error: {e}")
        article_summary = summarize(article_text)
        all_articles.append({'title': article_title, 'text': article_summary, 'url': article_url})
    
    return all_articles


