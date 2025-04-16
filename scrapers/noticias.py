import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(url: str) -> BeautifulSoup:
    """Faz requisição HTTP e retorna objeto BeautifulSoup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Adiciona um timeout para evitar requisições muito longas
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Levanta exceção para status codes de erro
        return BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        logger.error(f"Erro ao acessar {url}: {str(e)}")
        return None

def create_dataframe(articles: List[Dict]) -> pd.DataFrame:
    """Cria DataFrame a partir da lista de artigos."""
    if not articles:
        # Retorna DataFrame vazio com as colunas corretas
        return pd.DataFrame(columns=['title', 'link', 'source', 'category'])
    return pd.DataFrame(articles)

def fetch_technology() -> pd.DataFrame:
    """Busca notícias de tecnologia do Olhar Digital e Canaltech."""
    articles = []
    
    # Olhar Digital
    try:
        logger.info("Buscando notícias do Olhar Digital...")
        soup = make_request('https://olhardigital.com.br/ultimas/')
        if soup:
            news_items = soup.select('.mat-box')
            for item in news_items[:10]:
                title_elem = item.select_one('.mat-box-title')
                if title_elem and title_elem.a:
                    articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'Olhar Digital',
                        'category': 'Technology'
                    })
            logger.info(f"Encontradas {len(articles)} notícias do Olhar Digital")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Olhar Digital: {str(e)}")

    # Canaltech
    try:
        logger.info("Buscando notícias do Canaltech...")
        soup = make_request('https://canaltech.com.br/ultimas/')
        if soup:
            news_items = soup.select('article.timeline__item')
            canaltech_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('h3.title')
                if title_elem and title_elem.a:
                    canaltech_articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': f"https://canaltech.com.br{title_elem.a['href']}",
                        'source': 'Canaltech',
                        'category': 'Technology'
                    })
            articles.extend(canaltech_articles)
            logger.info(f"Encontradas {len(canaltech_articles)} notícias do Canaltech")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Canaltech: {str(e)}")

    return create_dataframe(articles)

def fetch_business() -> pd.DataFrame:
    """Busca notícias de negócios da Exame e CNN Brazil."""
    articles = []
    
    # Exame
    try:
        logger.info("Buscando notícias da Exame (Negócios)...")
        soup = make_request('https://exame.com/negocios/')
        if soup:
            news_items = soup.select('article.article-card')
            for item in news_items[:10]:
                title_elem = item.select_one('h2.article-card__title')
                if title_elem and title_elem.a:
                    articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'Exame',
                        'category': 'Business'
                    })
            logger.info(f"Encontradas {len(articles)} notícias da Exame")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Exame: {str(e)}")

    # CNN Brazil Business
    try:
        logger.info("Buscando notícias da CNN Brazil (Negócios)...")
        soup = make_request('https://www.cnnbrasil.com.br/business/')
        if soup:
            news_items = soup.select('.home__list__item')
            cnn_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('h2.news-item-header__title')
                if title_elem and title_elem.a:
                    cnn_articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'CNN Brazil',
                        'category': 'Business'
                    })
            articles.extend(cnn_articles)
            logger.info(f"Encontradas {len(cnn_articles)} notícias da CNN Brazil")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da CNN Brazil: {str(e)}")

    return create_dataframe(articles)

def fetch_astronomy() -> pd.DataFrame:
    """Busca notícias de astronomia do Space.com e Galileu."""
    articles = []
    
    # Space.com
    try:
        logger.info("Buscando notícias do Space.com...")
        soup = make_request('https://www.space.com/news')
        if soup:
            news_items = soup.select('article.listing-item')
            for item in news_items[:10]:
                title_elem = item.select_one('h3.article-name')
                if title_elem and title_elem.a:
                    articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': f"https://www.space.com{title_elem.a['href']}",
                        'source': 'Space.com',
                        'category': 'Astronomy'
                    })
            logger.info(f"Encontradas {len(articles)} notícias do Space.com")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Space.com: {str(e)}")

    # Galileu
    try:
        logger.info("Buscando notícias da Galileu...")
        soup = make_request('https://revistagalileu.globo.com/ciencia/')
        if soup:
            news_items = soup.select('.feed-post-body')
            galileu_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('.feed-post-link')
                if title_elem:
                    galileu_articles.append({
                        'title': title_elem.text.strip(),
                        'link': title_elem['href'],
                        'source': 'Galileu',
                        'category': 'Astronomy'
                    })
            articles.extend(galileu_articles)
            logger.info(f"Encontradas {len(galileu_articles)} notícias da Galileu")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Galileu: {str(e)}")

    return create_dataframe(articles)

def fetch_economy() -> pd.DataFrame:
    """Busca notícias de economia da CNN Brazil Economy e Exame."""
    articles = []
    
    # CNN Brazil Economy
    try:
        logger.info("Buscando notícias da CNN Brazil (Economia)...")
        soup = make_request('https://www.cnnbrasil.com.br/economia/')
        if soup:
            news_items = soup.select('.home__list__item')
            for item in news_items[:10]:
                title_elem = item.select_one('h2.news-item-header__title')
                if title_elem and title_elem.a:
                    articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'CNN Brazil Economy',
                        'category': 'Economy'
                    })
            logger.info(f"Encontradas {len(articles)} notícias da CNN Brazil Economy")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da CNN Brazil Economy: {str(e)}")

    # Exame Economy
    try:
        logger.info("Buscando notícias da Exame (Economia)...")
        soup = make_request('https://exame.com/economia/')
        if soup:
            news_items = soup.select('article.article-card')
            exame_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('h2.article-card__title')
                if title_elem and title_elem.a:
                    exame_articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'Exame Economy',
                        'category': 'Economy'
                    })
            articles.extend(exame_articles)
            logger.info(f"Encontradas {len(exame_articles)} notícias da Exame Economy")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Exame Economy: {str(e)}")

    return create_dataframe(articles)

def fetch_crypto() -> pd.DataFrame:
    """Busca notícias de criptomoedas do Livecoins e Cointelegraph Brazil."""
    articles = []
    
    # Livecoins
    try:
        logger.info("Buscando notícias do Livecoins...")
        soup = make_request('https://livecoins.com.br/ultimas-noticias/')
        if soup:
            news_items = soup.select('article.jeg_post')
            for item in news_items[:10]:
                title_elem = item.select_one('h3.jeg_post_title')
                if title_elem and title_elem.a:
                    articles.append({
                        'title': title_elem.a.text.strip(),
                        'link': title_elem.a['href'],
                        'source': 'Livecoins',
                        'category': 'Cryptocurrency'
                    })
            logger.info(f"Encontradas {len(articles)} notícias do Livecoins")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Livecoins: {str(e)}")

    # Cointelegraph Brazil
    try:
        logger.info("Buscando notícias do Cointelegraph Brazil...")
        soup = make_request('https://br.cointelegraph.com/news')
        if soup:
            news_items = soup.select('article.post-card')
            cointelegraph_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('span.post-card__title')
                if title_elem:
                    link_elem = item.select_one('a.post-card__title-link')
                    if link_elem:
                        cointelegraph_articles.append({
                            'title': title_elem.text.strip(),
                            'link': f"https://br.cointelegraph.com{link_elem['href']}",
                            'source': 'Cointelegraph Brazil',
                            'category': 'Cryptocurrency'
                        })
            articles.extend(cointelegraph_articles)
            logger.info(f"Encontradas {len(cointelegraph_articles)} notícias do Cointelegraph Brazil")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Cointelegraph Brazil: {str(e)}")

    return create_dataframe(articles)
