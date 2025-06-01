import streamlit as st
import pandas as pd
from scrapers.noticias import (
    fetch_technology,
    fetch_business,
    fetch_astronomy,
    fetch_economy,
    fetch_crypto,
    fetch_test_g1
)
from utils import format_link, truncate_text

# Configuração da página
st.set_page_config(
    page_title="Notícias",
    page_icon="📰",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .news-card {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
        border-left: 4px solid #4361ee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .news-title {
        color: #333;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .news-source {
        color: #666;
        font-size: 0.85rem;
        font-style: italic;
    }
    .category-tech { border-left-color: #4361ee; }
    .category-business { border-left-color: #3a0ca3; }
    .category-astronomy { border-left-color: #7209b7; }
    .category-economy { border-left-color: #f72585; }
    .category-crypto { border-left-color: #4cc9f0; }
    .category-test { border-left-color: #4ade80; }

    .main-header {
        background-color: #f1f3f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .view-option {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho principal com estilo melhorado
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("📰 Agregador de Notícias")
st.markdown("Mantenha-se informado com as últimas notícias de várias fontes e categorias.")
st.markdown('</div>', unsafe_allow_html=True)

# Barra lateral
st.sidebar.title("Controles")

# Seleção de categoria
# Dicionário para mapear nomes em português para funções
CATEGORIAS = {
    "Tecnologia": "Technology",
    "Negócios": "Business",
    "Astronomia": "Astronomy",
    "Economia": "Economy",
    "Criptomoedas": "Cryptocurrency",
    "Teste (G1)": "TestG1"  # Categoria de teste
}

# Ícones para categorias
CATEGORY_ICONS = {
    "Tecnologia": "💻",
    "Negócios": "💼",
    "Astronomia": "🔭",
    "Economia": "📊",
    "Criptomoedas": "🪙",
    "Teste (G1)": "🧪"
}

# Mapeamento de categorias para classes CSS
CATEGORY_CLASSES = {
    "Technology": "category-tech",
    "Business": "category-business",
    "Astronomy": "category-astronomy",
    "Economy": "category-economy",
    "Cryptocurrency": "category-crypto",
    "TestG1": "category-test"
}

# Seleção de categoria em português
categoria_pt = st.sidebar.selectbox(
    "Selecione a Categoria",
    list(CATEGORIAS.keys())
)

# Convertendo a categoria selecionada para inglês
categoria = CATEGORIAS[categoria_pt]

# Opções de visualização
view_option = st.sidebar.radio(
    "Formato de Visualização",
    ["Cards", "Tabela Compacta", "Lista Simples"]
)

# Número de notícias a exibir
max_news = st.sidebar.slider(
    "Número máximo de notícias",
    min_value=5,
    max_value=50,
    value=15,
    step=5
)

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
        "Cryptocurrency": fetch_crypto,
        "TestG1": fetch_test_g1  # Nova função de teste
    }

    # Debug: Imprimir informações úteis
    with st.sidebar.expander("📝 Informações de Debug"):
        st.write(f"Categoria selecionada: {categoria}")
        st.write(f"Função chamada: {funcoes_categoria[categoria].__name__}")

    try:
        # Buscar notícias da categoria
        df = funcoes_categoria[categoria]()
        if not df.empty:
            with st.sidebar.expander("📝 Informações de Debug"):
                st.write(f"Número de notícias encontradas: {len(df)}")
        return df
    except Exception as e:
        st.sidebar.error(f"Erro ao buscar notícias: {str(e)}")
        return pd.DataFrame()

# Função para criar card HTML de notícia
def create_news_card(title, link, source, category_class):
    """Cria um card HTML para exibir uma notícia."""
    card_html = f"""
    <div class="news-card {category_class}">
        <div class="news-title">
            <a href="{link}" target="_blank">{title}</a>
        </div>
        <div class="news-source">Fonte: {source}</div>
    </div>
    """
    return card_html

# Função para criar lista simples de notícias
def create_news_list(news_df):
    """Cria uma lista simples de notícias."""
    for _, row in news_df.iterrows():
        st.markdown(f"• [{row['title']}]({row['link']}) - _{row['source']}_")

# Conteúdo principal
try:
    # Exibir ícone e título da categoria
    st.subheader(f"{CATEGORY_ICONS.get(categoria_pt, '📰')} {categoria_pt}")

    with st.spinner(f"Buscando notícias de {categoria_pt}..."):
        df = buscar_noticias(categoria)

        if df.empty:
            st.warning("Nenhuma notícia encontrada para a categoria selecionada.")
        else:
            # Limitar o número de notícias conforme definido no slider
            df = df.head(max_news)

            # Traduzir nomes das colunas (para uso na exibição em tabela)
            df_display = df.rename(columns={
                'title': 'título',
                'source': 'fonte',
                'category': 'categoria'
            })

            # Escolher o formato de exibição
            if view_option == "Cards":
                # Exibir em formato de cards
                category_class = CATEGORY_CLASSES.get(categoria, "")

                # Criar grid com 2 colunas
                col1, col2 = st.columns(2)

                # Distribuir as notícias entre as duas colunas
                for i, (_, row) in enumerate(df.iterrows()):
                    card = create_news_card(
                        title=truncate_text(row['title'], 120),
                        link=row['link'],
                        source=row['source'],
                        category_class=category_class
                    )

                    # Alternar entre as colunas
                    if i % 2 == 0:
                        col1.markdown(card, unsafe_allow_html=True)
                    else:
                        col2.markdown(card, unsafe_allow_html=True)

            elif view_option == "Tabela Compacta":
                # Criar links clicáveis
                df_display['título'] = df.apply(
                    lambda row: format_link(truncate_text(row['title'], 80), row['link']),
                    axis=1
                )

                # Remover coluna de link pois já está embutida no título
                df_display = df_display.drop('link', axis=1)

                # Exibir o dataframe com links clicáveis
                st.write(df_display.to_html(escape=False), unsafe_allow_html=True)

            else:  # Lista Simples
                create_news_list(df)

            # Exibir estatísticas
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 📈 Estatísticas")
            st.sidebar.markdown(f"**Total de artigos:** {len(df)}")
            source_stats = df['source'].value_counts()

            st.sidebar.markdown("#### 🔍 Fontes:")
            for source, count in source_stats.items():
                st.sidebar.markdown(f"- **{source}**: {count} artigos")

except Exception as e:
    st.error(f"Ocorreu um erro ao processar as notícias: {str(e)}")
    with st.expander("Ver detalhes do erro"):
        st.exception(e)
