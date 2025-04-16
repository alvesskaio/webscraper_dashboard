def format_link(title: str, url: str) -> str:
    """
    Formata um título e URL em uma string de link HTML.
    
    Args:
        title (str): O texto a ser exibido para o link
        url (str): A URL para qual o link aponta
        
    Returns:
        str: Link formatado em HTML
    """
    return f'<a href="{url}" target="_blank">{title}</a>'

def truncate_text(text: str, limit: int = 100) -> str:
    """
    Trunca o texto para um comprimento específico, adicionando reticências se necessário.
    
    Args:
        text (str): Texto a ser truncado
        limit (int): Comprimento máximo antes da truncagem
        
    Returns:
        str: Texto truncado com reticências se necessário
    """
    return text if len(text) <= limit else f"{text[:limit-3]}..."
