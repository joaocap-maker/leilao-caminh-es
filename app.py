import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Leilões de Caminhões", layout="wide")

st.title("🚛 Painel Profissional - Leilões de Caminhões")

st.markdown("Sistema inteligente de monitoramento de leilões no Brasil")

# 🔎 Palavras-chave mais completas
PALAVRAS_CHAVE = [
    "caminhão", "caminhao", "truck",
    "volvo", "scania", "mercedes", "iveco",
    "basculante", "caçamba", "pipa", "6x2", "6x4"
]

# 🌎 Lista de sites
SITES = [
    {
        "nome": "Sodré Santoro",
        "url": "https://www.sodresantoro.com.br/veiculos"
    },
    {
        "nome": "VIP Leilões",
        "url": "https://www.vipleiloes.com.br"
    }
]


def contem_palavra(texto):
    texto = texto.lower()
    return any(p in texto for p in PALAVRAS_CHAVE)


def buscar_site(nome, url):
    resultados = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for item in soup.find_all("a"):
            texto = item.get_text().strip()

            if len(texto) > 20 and contem_palavra(texto):
                resultados.append({
                    "titulo": texto[:200],
                    "link": url,
                    "fonte": nome
                })

    except:
        pass

    return resultados


def buscar_todos():
    todos = []

    for site in SITES:
        dados = buscar_site(site["nome"], site["url"])
        todos.extend(dados)

    return todos


# 🎛️ FILTROS
filtro = st.selectbox(
    "Filtrar tipo de caminhão",
    ["Todos", "Basculante", "Pipa", "Cavalo Mecânico"]
)

# 🚀 BOTÃO
if st.button("🔎 Buscar caminhões nos leilões"):
    with st.spinner("Buscando oportunidades..."):
        dados = buscar_todos()

    if not dados:
        st.error("Nenhum caminhão encontrado (sites podem ter bloqueado temporariamente).")

    else:
        st.success(f"{len(dados)} oportunidades encontradas")

        for item in dados:
            titulo = item["titulo"].lower()

            # filtro simples
            if filtro == "Basculante" and "basculante" not in titulo:
                continue
            if filtro == "Pipa" and "pipa" not in titulo:
                continue

            st.markdown(f"""
            ### 🚛 {item['titulo']}
            **Fonte:** {item['fonte']}  
            [🔗 Ver lote]({item['link']})
            ---
            """)
