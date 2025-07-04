import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging
import time
import random

# Configuração do logging com mais detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def make_request(url: str) -> BeautifulSoup:
    """Faz requisição HTTP e retorna objeto BeautifulSoup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        logger.info(f"Tentando acessar URL: {url}")

        # Adiciona um delay aleatório entre 1 e 3 segundos
        time.sleep(1 + 2 * random.random())

        response = requests.get(url, headers=headers, timeout=15)
        logger.info(f"Status code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            logger.info(f"Página carregada com sucesso: {len(response.text)} bytes")
            return soup
        else:
            logger.error(f"Erro no status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Erro ao acessar {url}: {str(e)}")
        return None

def validate_article(title: str, link: str, base_url: str) -> bool:
    """Valida se um artigo tem título e link válidos."""
    if not title or not link or len(title) < 5:
        return False

    # Normaliza o link
    if not link.startswith(('http://', 'https://')):
        if not link.startswith('/'):
            link = '/' + link
        link = base_url.rstrip('/') + link

    return True  # Simplificando a validação para evitar falsos negativos

def create_dataframe(articles: List[Dict]) -> pd.DataFrame:
    """Cria DataFrame a partir da lista de artigos."""
    if not articles:
        logger.warning("Nenhum artigo encontrado para criar o DataFrame")
        return pd.DataFrame(columns=['title', 'link', 'source', 'category'])

    logger.info(f"Criando DataFrame com {len(articles)} artigos")
    return pd.DataFrame(articles)

def fetch_technology() -> pd.DataFrame:
    """Busca notícias de tecnologia do Olhar Digital e Canaltech."""
    articles = []

    # Olhar Digital
    try:
        logger.info("Iniciando busca no Olhar Digital...")
        base_url = 'https://olhardigital.com.br/editorias/noticias/'
        soup = make_request(base_url)

        if soup:
            # Busca por artigos na página inicial
            logger.info("Buscando artigos no Olhar Digital...")

            # Tenta diferentes áreas da página
            news_areas = [
                soup.select('.main-carousel article'),  # Carrossel principal
                soup.select('.featured-posts article'),  # Posts em destaque
                soup.select('.latest-posts article'),   # Últimos posts
                soup.select('.post-list article'),      # Lista de posts
                soup.select('article.post')             # Artigos gerais
            ]

            for area in news_areas:
                logger.info(f"Encontrados {len(area)} artigos em uma área")
                for item in area:
                    # Tenta diferentes elementos para título e link
                    title_elem = (
                        item.select_one('h1 a') or
                        item.select_one('h2 a') or
                        item.select_one('h3 a') or
                        item.select_one('.title a') or
                        item.select_one('a[title]')
                    )

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')

                        logger.info(f"Encontrado artigo: {title[:50]}... - {link}")

                        if validate_article(title, link, base_url):
                            if not link.startswith(('http://', 'https://')):
                                link = base_url + link.lstrip('/')

                            articles.append({
                                'title': title,
                                'link': link,
                                'source': 'Olhar Digital',
                                'category': 'Technology'
                            })

    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Olhar Digital: {str(e)}")
        logger.exception("Detalhes do erro:")

    # Canaltech
    try:
        logger.info("Buscando notícias do Canaltech...")
        base_url = 'https://canaltech.com.br'
        soup = make_request(base_url)

        if soup:
            logger.info("Buscando artigos no Canaltech...")

            # Tenta diferentes áreas da página
            news_areas = [
                soup.select('.featured-news article'),  # Notícias em destaque
                soup.select('.latest-news article'),    # Últimas notícias
                soup.select('.news-list article'),      # Lista de notícias
                soup.select('article.news-item'),       # Items de notícia
                soup.select('.main-content article')    # Conteúdo principal
            ]

            for area in news_areas:
                logger.info(f"Encontrados {len(area)} artigos em uma área")
                for item in area:
                    # Tenta diferentes elementos para título e link
                    title_elem = (
                        item.select_one('h1 a') or
                        item.select_one('h2 a') or
                        item.select_one('h3 a') or
                        item.select_one('.title a') or
                        item.select_one('a[title]')
                    )

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')

                        logger.info(f"Encontrado artigo: {title[:50]}... - {link}")

                        if validate_article(title, link, base_url):
                            if not link.startswith(('http://', 'https://')):
                                link = base_url + link.lstrip('/')

                            articles.append({
                                'title': title,
                                'link': link,
                                'source': 'Canaltech',
                                'category': 'Technology'
                            })

    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Canaltech: {str(e)}")
        logger.exception("Detalhes do erro:")

    logger.info(f"Total de artigos encontrados: {len(articles)}")
    return create_dataframe(articles)

def fetch_business() -> pd.DataFrame:
    """Busca notícias de negócios da Exame e CNN Brazil."""
    articles = []

    # Exame
    try:
        logger.info("Buscando notícias da Exame (Negócios)...")
        base_url = 'https://exame.com'
        soup = make_request(base_url + '/negocios/')
        if soup:
            news_items = soup.select('article.article-card')
            for item in news_items[:10]:
                title_elem = item.select_one('h2.article-card__title')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        articles.append({
                            'title': title,
                            'link': link,
                            'source': 'Exame',
                            'category': 'Business'
                        })
            logger.info(f"Encontradas {len(articles)} notícias da Exame")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Exame: {str(e)}")

    # CNN Brazil Business
    try:
        logger.info("Buscando notícias da CNN Brazil (Negócios)...")
        base_url = 'https://www.cnnbrasil.com.br'
        soup = make_request(base_url + '/business/')
        if soup:
            news_items = soup.select('.home__list__item')
            cnn_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('h2.news-item-header__title')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        cnn_articles.append({
                            'title': title,
                            'link': link,
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
        base_url = 'https://www.space.com'
        soup = make_request(base_url + '/news')
        if soup:
            news_items = soup.select('article.listing-item')
            for item in news_items[:10]:
                title_elem = item.select_one('h3.article-name')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        articles.append({
                            'title': title,
                            'link': base_url + link,
                            'source': 'Space.com',
                            'category': 'Astronomy'
                        })
            logger.info(f"Encontradas {len(articles)} notícias do Space.com")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Space.com: {str(e)}")

    # Galileu
    try:
        logger.info("Buscando notícias da Galileu...")
        base_url = 'https://revistagalileu.globo.com'
        soup = make_request(base_url + '/ciencia/')
        if soup:
            news_items = soup.select('.feed-post-body')
            galileu_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('.feed-post-link')
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem['href']

                    if validate_article(title, link, base_url):
                        galileu_articles.append({
                            'title': title,
                            'link': link,
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
        base_url = 'https://www.cnnbrasil.com.br'
        soup = make_request(base_url + '/economia/')
        if soup:
            news_items = soup.select('.home__list__item')
            for item in news_items[:10]:
                title_elem = item.select_one('h2.news-item-header__title')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        articles.append({
                            'title': title,
                            'link': link,
                            'source': 'CNN Brazil Economy',
                            'category': 'Economy'
                        })
            logger.info(f"Encontradas {len(articles)} notícias da CNN Brazil Economy")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da CNN Brazil Economy: {str(e)}")

    # Exame Economy
    try:
        logger.info("Buscando notícias da Exame (Economia)...")
        base_url = 'https://exame.com'
        soup = make_request(base_url + '/economia/')
        if soup:
            news_items = soup.select('article.article-card')
            exame_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('h2.article-card__title')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        exame_articles.append({
                            'title': title,
                            'link': link,
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
        base_url = 'https://livecoins.com.br'
        soup = make_request(base_url + '/ultimas-noticias/')
        if soup:
            news_items = soup.select('article.jeg_post')
            for item in news_items[:10]:
                title_elem = item.select_one('h3.jeg_post_title')
                if title_elem and title_elem.a:
                    title = title_elem.a.text.strip()
                    link = title_elem.a['href']

                    if validate_article(title, link, base_url):
                        articles.append({
                            'title': title,
                            'link': link,
                            'source': 'Livecoins',
                            'category': 'Cryptocurrency'
                        })
            logger.info(f"Encontradas {len(articles)} notícias do Livecoins")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Livecoins: {str(e)}")

    # Cointelegraph Brazil
    try:
        logger.info("Buscando notícias do Cointelegraph Brazil...")
        base_url = 'https://br.cointelegraph.com'
        soup = make_request(base_url + '/news')
        if soup:
            news_items = soup.select('article.post-card')
            cointelegraph_articles = []
            for item in news_items[:10]:
                title_elem = item.select_one('span.post-card__title')
                if title_elem:
                    link_elem = item.select_one('a.post-card__title-link')
                    if link_elem:
                        title = title_elem.text.strip()
                        link = link_elem['href']

                        if validate_article(title, link, base_url):
                            cointelegraph_articles.append({
                                'title': title,
                                'link': base_url + link,
                                'source': 'Cointelegraph Brazil',
                                'category': 'Cryptocurrency'
                            })
            articles.extend(cointelegraph_articles)
            logger.info(f"Encontradas {len(cointelegraph_articles)} notícias do Cointelegraph Brazil")
    except Exception as e:
        logger.error(f"Erro ao buscar notícias do Cointelegraph Brazil: {str(e)}")

    return create_dataframe(articles)

def fetch_test_g1() -> pd.DataFrame:
    """
    Busca notícias do G1 como teste de validação do scraper.
    Esta função é otimizada para maior confiabilidade.
    """
    articles = []
    base_url = 'https://g1.globo.com'

    try:
        logger.info(f"Iniciando teste com G1 ({base_url})...")

        # Usando parâmetros mais robustos para a requisição
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        }

        # Aplicando delay mais longo para evitar bloqueios
        time.sleep(2)

        try:
            logger.info("Fazendo requisição para G1...")
            response = requests.get(base_url, headers=headers, timeout=20)
            logger.info(f"Status da requisição: {response.status_code}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.info(f"HTML carregado com sucesso: {len(response.text)} bytes")

                # Log para verificar se o título da página está correto
                page_title = soup.title.text if soup.title else "Sem título"
                logger.info(f"Título da página: {page_title}")

                # Elementos onde normalmente ficam as manchetes no G1
                selectors = [
                    '.feed-post-body',
                    '.bastian-feed-item',
                    '.bstn-item',
                    '.post'
                ]

                total_found = 0

                for selector in selectors:
                    news_items = soup.select(selector)
                    logger.info(f"Seletor '{selector}': encontrados {len(news_items)} itens")
                    total_found += len(news_items)

                    for item in news_items[:10]:  # Limitando a 10 itens por seletor
                        # Tentando diferentes padrões comuns para títulos no G1
                        title_candidates = [
                            item.select_one('.feed-post-link'),
                            item.select_one('.bstn-hl-title'),
                            item.select_one('a.gui-card-content__title'),
                            item.select_one('h2 a'),
                            item.select_one('h3 a')
                        ]

                        title_elem = next((t for t in title_candidates if t is not None), None)

                        if title_elem:
                            title = title_elem.get_text(strip=True)

                            # Buscando o link (pode estar no próprio elemento ou em um parent)
                            if title_elem.name == 'a':
                                link = title_elem.get('href', '')
                            else:
                                link_elem = title_elem.find_parent('a')
                                link = link_elem.get('href', '') if link_elem else ''

                            if title and link:
                                logger.info(f"Artigo encontrado: '{title[:30]}...' - Link: {link[:50]}...")

                                # Normalizando o link
                                if not link.startswith(('http://', 'https://')):
                                    link = base_url + link.lstrip('/')

                                articles.append({
                                    'title': title,
                                    'link': link,
                                    'source': 'G1',
                                    'category': 'Test'
                                })

                logger.info(f"Total de elementos encontrados com todos os seletores: {total_found}")

                if not articles:
                    # Se não encontrou nada, tentar uma abordagem mais genérica
                    logger.warning("Nenhum artigo encontrado com os seletores específicos. Tentando abordagem genérica...")

                    # Procurando qualquer link que pareça uma notícia
                    all_links = soup.select('a[href*="/noticia/"]')
                    logger.info(f"Encontrados {len(all_links)} links genéricos de notícias")

                    for link_elem in all_links[:15]:  # Limitando a 15 links
                        title = link_elem.get_text(strip=True)
                        link = link_elem.get('href', '')

                        if title and len(title) > 20 and link:  # Filtrar títulos curtos demais
                            logger.info(f"Artigo encontrado (genérico): '{title[:30]}...'")

                            # Normalizando o link
                            if not link.startswith(('http://', 'https://')):
                                link = base_url + link.lstrip('/')

                            articles.append({
                                'title': title,
                                'link': link,
                                'source': 'G1',
                                'category': 'Test'
                            })
            else:
                logger.error(f"Falha na requisição: status code {response.status_code}")

        except requests.exceptions.Timeout:
            logger.error("Timeout na requisição para o G1")
        except requests.exceptions.ConnectionError:
            logger.error("Erro de conexão ao acessar o G1")

    except Exception as e:
        logger.error(f"Erro não esperado ao buscar notícias do G1: {str(e)}")
        logger.exception("Detalhes do erro:")

    # Removendo duplicatas pelo título
    if articles:
        df = pd.DataFrame(articles)
        df = df.drop_duplicates(subset=['title'])
        logger.info(f"Total de {len(df)} artigos únicos encontrados do G1")
        return df
    else:
        logger.warning("Nenhum artigo encontrado no G1")
        return pd.DataFrame(columns=['title', 'link', 'source', 'category'])
