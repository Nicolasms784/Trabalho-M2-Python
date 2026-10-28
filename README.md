# CineVibe

**Membros:** Enrico Barreto, Nicolas Milani, Vinicius Diniz.
**Dataset:** TMDB + https://www.themoviedb.org/
**App publicado:** https://trabalho-m2-python-gb599mbb7zmvgiudpcbsc6.streamlit.app/

## Funcionalidades
- [x] 1. Ler os dados do arquivo CSV do dataset.
- [x] 2. Converter as colunas que não estão num formato apropriado para os cálculos (números escritoscomo texto, valores por extenso, unidades junto do número, etc)
- [x] 3. Mostrar no mínimo 3 métricas sobre o dataset
- [x] 4. Classificar os registros em faixas a partir de uma coluna numérica e mostrar a faixa na tabela
- [x] 5. Uma tabela com os dados e nomes de coluna legíveis
- [x] 6. Uma busca por texto que não diferencie maiúsculas de minúsculas
- [x] 7. Um filtro por categoria, com as opções dos próprios dados (sem escrever à mão) e uma opção paramostrar todos
- [x] 8. Busca e filtro funcionando juntos
- [x] 9. Uma mensagem quando nenhum resultado for encontrado
- [x] 10. Código organizado em funções e módulos, com nomes que façam sentido no tema do grupo
- [x] 11. App publicado no Streamlit Community Cloud

## Funcionalidade extra
Mostrar a capa do filme com uma breve descrição/sinopse e uma função de Watchlist

## Como rodar
1. Certifica-te de que tens o Python instalado no teu computador.
2. Abre o terminal (PowerShell ou CMD) na pasta do projeto.
3. Instala as dependências necessárias (Streamlit e Pandas):
   pip install streamlit pandas

4.Executa o comando para iniciar a aplicação localmente:
  python -m streamlit run app.py
