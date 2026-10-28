import ast
import os
import pandas as pd

ARQUIVO_CSV = "tmdb_2000_filmes.csv"

# Dicionario de traducao de generos do TMDB
MAPA_GENEROS = {
    28: "Acao",
    12: "Aventura",
    16: "Animacao",
    35: "Comedia",
    80: "Crime",
    99: "Documentario",
    18: "Drama",
    10751: "Familia",
    14: "Fantasia",
    36: "Historia",
    27: "Terror",
    10402: "Musica",
    9648: "Misterio",
    10749: "Romance",
    878: "Ficcao Cientifica",
    10770: "Cinema TV",
    53: "Suspense",
    10752: "Guerra",
    37: "Faroeste",
}


def carregar_e_tratar_dados():
  """Le os dados do CSV local obrigatoriamente e aplica o tratamento."""
  if not os.path.exists(ARQUIVO_CSV):
    return pd.DataFrame()

  df = pd.read_csv(ARQUIVO_CSV)
  return _processar_conversoes(df)


def _processar_conversoes(df):
  """Realiza a conversao de tipos de colunas e mapeamentos."""
  # Conversoes numericas
  df["vote_average"] = pd.to_numeric(
      df.get("vote_average", 0), errors="coerce"
  ).fillna(0.0)
  df["popularity"] = pd.to_numeric(
      df.get("popularity", 0), errors="coerce"
  ).fillna(0.0)

  # Tratamento de datas e extracao do ano
  if "release_date" in df.columns:
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["Ano"] = df["release_date"].dt.year.fillna(0).astype(int)
  else:
    df["Ano"] = 0

  # Converte IDs de generos em lista legivel
  def converter_generos(genre_ids):
    if isinstance(genre_ids, str):
      try:
        genre_ids = ast.literal_eval(genre_ids)
      except Exception:
        return "Desconhecido"

    if isinstance(genre_ids, list):
      nomes = [
          MAPA_GENEROS.get(g_id, "")
          for g_id in genre_ids
          if g_id in MAPA_GENEROS
      ]
      return ", ".join(nomes) if nomes else "Desconhecido"
    return "Desconhecido"

  if "genre_ids" in df.columns:
    df["Generos"] = df["genre_ids"].apply(converter_generos)
  elif "Generos" not in df.columns:
    df["Generos"] = "Desconhecido"

  # Classificacao dos registros em faixas a partir de coluna numerica
  def classificar_nota(nota):
    if nota >= 8.0:
      return "Obra-Prima (8.0+)"
    elif nota >= 6.5:
      return "Muito Bom (6.5 - 7.9)"
    elif nota >= 5.0:
      return "Regular (5.0 - 6.4)"
    else:
      return "Ruim (< 5.0)"

  df["Faixa de Avaliacao"] = df["vote_average"].apply(classificar_nota)

  # Renomeia colunas para nomes legiveis em portugues
  df_renomeado = df.rename(
      columns={
          "id": "id",
          "title": "Titulo",
          "release_date": "Data de Lancamento",
          "vote_average": "Nota Media",
          "popularity": "Popularidade",
          "overview": "Sinopse",
      }
  )

  return df_renomeado