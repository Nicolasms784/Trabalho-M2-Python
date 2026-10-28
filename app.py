import dados
import streamlit as st

st.set_page_config(page_title="CineVibe", page_icon="🎬", layout="wide")

if "lista_de_desejos" not in st.session_state:
    st.session_state.lista_de_desejos = []

filmes = dados.carregar_filmes()

st.title("🎬 CineVibe")
st.caption("Explore a biblioteca de filmes, pesquise por titulo, filtre por genero e gerencie sua watchlist!")


def calcular_media_notas(lista_filmes):
    if len(lista_filmes) == 0:
        return 0.0
    soma = 0
    for filme in lista_filmes:
        soma = soma + filme["nota"]
    return soma / len(lista_filmes)


def encontrar_mais_popular(lista_filmes):
    if len(lista_filmes) == 0:
        return "N/A"
    mais_popular = lista_filmes[0]
    for filme in lista_filmes:
        if filme["popularidade"] > mais_popular["popularidade"]:
            mais_popular = filme
    return mais_popular["titulo"]


def classificar_nota(nota):
    if nota >= 8.0:
        return "Obra-Prima (8.0+)"
    elif nota >= 6.5:
        return "Muito Bom (6.5 - 7.9)"
    elif nota >= 5.0:
        return "Regular (5.0 - 6.4)"
    else:
        return "Ruim (< 5.0)"


def listar_generos_unicos(lista_filmes):
    generos = []
    for filme in lista_filmes:
        if filme["generos"] != "Desconhecido":
            partes = filme["generos"].split(", ")
            for g in partes:
                if g not in generos:
                    generos.append(g)
    generos.sort()
    return generos


def buscar_por_titulo(lista_filmes, busca):
    if not busca:
        return lista_filmes
    termo_busca = dados.remover_acentos(busca).lower()
    resultado = []
    for filme in lista_filmes:
        if termo_busca in filme["titulo_busca"]:
            resultado.append(filme)
    return resultado


def filtrar_por_genero(lista_filmes, genero):
    if genero == "Todos":
        return lista_filmes
    resultado = []
    for filme in lista_filmes:
        if genero.lower() in filme["generos"].lower():
            resultado.append(filme)
    return resultado


def montar_tabela(lista_filmes):
    tabela = []
    for filme in lista_filmes:
        linha = {
            "Titulo": filme["titulo"],
            "Ano": filme["ano"] if filme["ano"] > 0 else "Desconhecido",
            "Generos": filme["generos"],
            "Nota Media": filme["nota"],
            "Faixa de Avaliacao": classificar_nota(filme["nota"]),
            "Popularidade": filme["popularidade"],
        }
        tabela.append(linha)
    return tabela


if len(filmes) == 0:
    st.error("Erro ao carregar os dados do arquivo CSV.")
else:
    qtd_watchlist = len(st.session_state.lista_de_desejos)
    aba_explorar, aba_watchlist = st.tabs(
        ["🔍 Explorar Filmes", f"🔖 Watchlist ({qtd_watchlist})"]
    )

    with aba_explorar:
        st.subheader("📊 Visao Geral da Biblioteca")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Filmes", len(filmes))
        col2.metric("Media Geral de Notas", f"{calcular_media_notas(filmes):.2f} / 10")
        col3.metric("Filme Mais Popular", encontrar_mais_popular(filmes))

        st.markdown("---")

        st.sidebar.header("🔍 Painel de Controle")
        busca = st.sidebar.text_input("Buscar por titulo:")

        opcoes_generos = ["Todos"] + listar_generos_unicos(filmes)
        genero_selecionado = st.sidebar.selectbox(
            "Filtrar por Estilo de Filme (Genero)", opcoes_generos
        )

        encontrados = filtrar_por_genero(filmes, genero_selecionado)
        encontrados = buscar_por_titulo(encontrados, busca)

        st.sidebar.markdown(f"**Filmes encontrados:** {len(encontrados)}")

        FILMES_POR_PAGINA = 24
        total_paginas = max(1, (len(encontrados) - 1) // FILMES_POR_PAGINA + 1)

        if "num_pagina" in st.session_state and st.session_state.num_pagina > total_paginas:
            st.session_state.num_pagina = 1

        pagina_atual = st.sidebar.number_input(
            "Pagina", min_value=1, max_value=total_paginas, value=1, key="num_pagina"
        )

        inicio = (pagina_atual - 1) * FILMES_POR_PAGINA
        fim = inicio + FILMES_POR_PAGINA
        filmes_exibidos = encontrados[inicio:fim]

        st.subheader(
            f"Exibindo pagina {pagina_atual} de {total_paginas} (Total filtrado: {len(encontrados)} filmes)"
        )

        if len(filmes_exibidos) == 0:
            st.warning("Nenhum filme foi encontrado com esse titulo. Tente ajustar os parametros!")
        else:
            num_colunas = 4
            colunas = st.columns(num_colunas)
            for i in range(len(filmes_exibidos)):
                filme = filmes_exibidos[i]
                coluna_atual = colunas[i % num_colunas]
                with coluna_atual:
                    caminho_poster = filme["caminho_poster"]
                    if caminho_poster and str(caminho_poster).strip() != "":
                        url_capa = f"https://image.tmdb.org/t/p/w500{caminho_poster}"
                        st.image(url_capa, use_container_width=True)
                    else:
                        st.image(
                            "https://via.placeholder.com/500x750?text=Sem+Capa",
                            use_container_width=True,
                        )

                    st.markdown(f"### {filme['titulo']}")
                    
                    ano = filme["ano"] if filme["ano"] > 0 else "Desconhecido"
                    st.write(f"📅 Ano: {ano} | ⭐ Nota: {filme['nota']}")
                    st.write(f"🎬 {filme['generos']}")

                    id_filme = filme["id"]
                    esta_na_lista = id_filme in st.session_state.lista_de_desejos
                    if esta_na_lista:
                        if st.button("✅ Watchlist", key=f"btn_rem_{id_filme}_{i}"):
                            st.session_state.lista_de_desejos.remove(id_filme)
                            st.rerun()
                    else:
                        if st.button("➕ Watchlist", key=f"btn_add_{id_filme}_{i}"):
                            st.session_state.lista_de_desejos.append(id_filme)
                            st.rerun()

                    with st.expander("Ver Sinopse"):
                        st.write(filme["sinopse"])
                    st.markdown("---")

        with st.expander("Ver dados em formato de tabela completa"):
            st.dataframe(montar_tabela(encontrados), use_container_width=True)

    with aba_watchlist:
        st.subheader("🔖 Filmes Salvos na sua Watchlist")

        if len(st.session_state.lista_de_desejos) == 0:
            st.info(
                "Sua Watchlist esta vazia! Explore os filmes e clique em **➕ Watchlist** para adicionar."
            )
        else:
            filmes_watchlist = []
            for filme in filmes:
                if filme["id"] in st.session_state.lista_de_desejos:
                    filmes_watchlist.append(filme)

            st.write(f"Voce tem **{len(filmes_watchlist)}** filme(s) na sua lista:")

            num_colunas = 4
            colunas_watchlist = st.columns(num_colunas)
            for i in range(len(filmes_watchlist)):
                filme = filmes_watchlist[i]
                coluna_atual = colunas_watchlist[i % num_colunas]
                with coluna_atual:
                    caminho_poster = filme["caminho_poster"]
                    if caminho_poster and str(caminho_poster).strip() != "":
                        url_capa = f"https://image.tmdb.org/t/p/w500{caminho_poster}"
                        st.image(url_capa, use_container_width=True)
                    else:
                        st.image(
                            "https://via.placeholder.com/500x750?text=Sem+Capa",
                            use_container_width=True,
                        )

                    st.markdown(f"### {filme['titulo']}")
                    
                    ano = filme["ano"] if filme["ano"] > 0 else "Desconhecido"
                    st.write(f"📅 Ano: {ano} | ⭐ Nota: {filme['nota']}")
                    st.write(f"🎬 {filme['generos']}")

                    id_filme = filme["id"]
                    if st.button("❌ Remover", key=f"btn_w_rem_{id_filme}_{i}"):
                        st.session_state.lista_de_desejos.remove(id_filme)
                        st.rerun()

                    with st.expander("Ver Sinopse"):
                        st.write(filme["sinopse"])
                    st.markdown("---")