import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Leilões de Caminhões", layout="wide")

st.title("🚛 Monitor de Leilões de Caminhões")

st.write("Atualização automática de leilões no Brasil (modo inicial)")

def buscar_leiloes():
    url = "https://www.sodresantoro.com.br/veiculos"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    resultados = []

    for item in soup.find_all("div"):
        texto = item.get_text().lower()

        if "caminh" in texto:
            resultados.append({
                "titulo": item.get_text().strip()[:200],
                "link": url
            })

    return resultados


if st.button("🔄 Atualizar leilões"):
    dados = buscar_leiloes()

    if not dados:
        st.warning("Nenhum caminhão encontrado.")
    else:
        for item in dados[:20]:
            st.markdown(f"""
            ### {item['titulo']}
            [Ver lote]({item['link']})
            ---
            """)
