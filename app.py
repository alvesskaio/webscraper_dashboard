import streamlit as st
import pandas as pd
from scrapers.noticias import (
    fetch_technology,
    fetch_business,
    fetch_astronomy,
    fetch_economy,
    fetch_crypto
)
from utils import format_link, truncate_text

# Configuração da página
st.set_page_config(
    page_title="Agregador de Notícias",
    page_icon="📰",
    layout="wide"
)

# Título e descrição
st.title("📰 Agregador de Notícias")
st.markdown("Agregador de notícias em tempo real de várias fontes e categorias.")

# Barra lateral
st.sidebar.title("Controles")

# Seleção de categoria
# Dicionário para mapear nomes em português para funções
CATEGORIAS = {
    "Tecnologia": "Technology",
    "Negócios": "Business",
    "Astronomia": "Astronomy",
    "Economia": "Economy",
    "Criptomoedas": "Cryptocurrency"
}

# Seleção de categoria em português
categoria_pt = st.sidebar.selectbox(
    "Selecione a Categoria",
    list(CATEGORIAS.keys())
)

# Convertendo a categoria selecionada para inglês
categoria = CATEGORIAS[categoria_pt]

# Botão de atualização
if st.sidebar.button("🔄 Atualizar Dados"):
    st.experimental_rerun()

# Função para buscar notícias baseada na categoria
@st.cache_data(ttl=300)  # Cache por 5 minutos
def buscar_noticias(categoria: str) -> pd.DataFrame:
    """
    Busca notícias da categoria selecionada.
    
    Args:
        categoria (str): Categoria selecionada em inglês
        
    Returns:
        pd.DataFrame: DataFrame com as notícias
    """
    # Mapeamento de categorias para funções
    funcoes_categoria = {
        "Technology": fetch_technology,
        "Business": fetch_business,
        "Astronomy": fetch_astronomy,
        "Economy": fetch_economy,
        "Cryptocurrency": fetch_crypto
    }
    
    # Debug: Imprimir informações úteis
    st.sidebar.markdown("### Debug Info")
    st.sidebar.write(f"Categoria selecionada: {categoria}")
    st.sidebar.write(f"Função chamada: {funcoes_categoria[categoria].__name__}")
    
    try:
        # Buscar notícias da categoria
        df = funcoes_categoria[categoria]()
        st.sidebar.write(f"Número de notícias encontradas: {len(df)}")
        return df
    except Exception as e:
        st.sidebar.error(f"Erro ao buscar notícias: {str(e)}")
        return pd.DataFrame()

# Conteúdo principal
try:
    with st.spinner(f"Buscando notícias de {categoria_pt}..."):
        df = buscar_noticias(categoria)
        
        if df.empty:
            st.warning("Nenhuma notícia encontrada para a categoria selecionada.")
        else:
            # Traduzir nomes das colunas
            df = df.rename(columns={
                'title': 'título',
                'source': 'fonte',
                'category': 'categoria'
            })
            
            # Criar links clicáveis
            df['título'] = df.apply(
                lambda row: format_link(truncate_text(row['título']), row['link']),
                axis=1
            )
            
            # Remover coluna de link pois já está embutida no título
            df_display = df.drop('link', axis=1)
            
            # Exibir o dataframe com links clicáveis
            st.write(df_display.to_html(escape=False), unsafe_allow_html=True)
            
            # Exibir estatísticas
            st.sidebar.markdown("---")
            st.sidebar.markdown("### Estatísticas")
            st.sidebar.markdown(f"Total de artigos: {len(df)}")
            source_stats = df['fonte'].value_counts()
            st.sidebar.markdown("#### Fontes:")
            for source, count in source_stats.items():
                st.sidebar.markdown(f"- {source}: {count}")

except Exception as e:
    st.error(f"Ocorreu um erro: {str(e)}")
    st.exception(e)
