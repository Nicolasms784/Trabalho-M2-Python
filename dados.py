import csv
import os
import unicodedata

CAMINHO_FILMES = "tmdb_2000_filmes.csv"

MAPA_GENEROS = {
    "28": "Acao",
    "12": "Aventura",
    "16": "Animacao",
    "35": "Comedia",
    "80": "Crime",
    "99": "Documentario",
    "18": "Drama",
    "10751": "Familia",
    "14": "Fantasia",
    "36": "Historia",
    "27": "Terror",
    "10402": "Musica",
    "9648": "Misterio",
    "10749": "Romance",
    "878": "Ficcao Cientifica",
    "10770": "Cinema TV",
    "53": "Suspense",
    "10752": "Guerra",
    "37": "Faroeste",
}


def ler_filmes(caminho=CAMINHO_FILMES):
    if not os.path.exists(caminho):
        return []
    filmes = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            filmes.append(linha)
    return filmes


def converter_numero(texto):
    if not texto:
        return 0.0
    try:
        return float(texto)
    except ValueError:
        return 0.0


def converter_ano(texto):
    if not texto or len(texto) < 4:
        return 0
    try:
        return int(texto[:4])
    except ValueError:
        return 0


def converter_generos(texto_ids):
    if not texto_ids:
        return "Desconhecido"
    
    texto_limpo = texto_ids.replace("[", "").replace("]", "").replace(" ", "")
    if not texto_limpo:
        return "Desconhecido"
    
    ids_lista = texto_limpo.split(",")
    nomes = []
    for id_g in ids_lista:
        if id_g in MAPA_GENEROS:
            nomes.append(MAPA_GENEROS[id_g])
            
    if len(nomes) == 0:
        return "Desconhecido"
    return ", ".join(nomes)


def remover_acentos(texto):
    if not texto:
        return ""
    normalizado = unicodedata.normalize("NFD", texto)
    apenas_letras = []
    for caractere in normalizado:
        if unicodedata.category(caractere) != "Mn":
            apenas_letras.append(caractere)
    return "".join(apenas_letras)


def preparar_filmes(linhas):
    filmes = []
    for i in range(len(linhas)):
        linha = linhas[i]
        id_original = str(linha.get("id", "")).strip()
        if not id_original:
            id_original = f"filme_{i}"
            
        titulo_original = linha.get("title", "Sem Titulo")
            
        filme = {
            "id": id_original,
            "titulo": titulo_original,
            "titulo_busca": remover_acentos(titulo_original).lower(),
            "ano": converter_ano(linha.get("release_date", "")),
            "nota": converter_numero(linha.get("vote_average", 0)),
            "popularidade": converter_numero(linha.get("popularity", 0)),
            "generos": converter_generos(linha.get("genre_ids", "")),
            "sinopse": linha.get("overview", "Sem sinopse disponivel."),
            "caminho_poster": linha.get("poster_path", ""),
        }
        filmes.append(filme)
    return filmes


def carregar_filmes(caminho=CAMINHO_FILMES):
    return preparar_filmes(ler_filmes(caminho))


if __name__ == "__main__":
    dados_brutos = ler_filmes()
    print("Total de linhas lidas:", len(dados_brutos))
    if len(dados_brutos) > 0:
        print("Primeiro filme preparado:", carregar_filmes()[0])