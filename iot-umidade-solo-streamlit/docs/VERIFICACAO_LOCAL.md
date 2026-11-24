# Verificação de integridade do pacote

A revisão realizada na preparação deste ZIP incluiu:

- Compilação sintática (`py_compile`) de `app.py` e módulos auxiliares.
- Carga do histórico público: **144 linhas, 6 dias**.
- Verificação de média global ADC **2456,85** e índice médio **22,92%**, coerentes com o relatório.
- Geração sem erro das funções de gráfico (série ADC, índice, médias diárias, boxplot, mapa de calor, variações, histograma e teste físico).
- Teste das rotinas de filtro: três primeiros dias retornam **72 registros**.
- Detecção das duas quedas de ADC demonstrativas em 21/11: **−96 e −40**.
- Execução simulada do fluxo Python das oito páginas, com substitutos para chamadas da interface Streamlit.
- Confirmação de que o ZIP não contém arquivo `secrets.toml` com credenciais.

**Limitação importante:** este ambiente não dispõe da biblioteca Streamlit instalada e não teve acesso à instalação de novos pacotes pela internet. Portanto, **não foi possível abrir e validar visualmente o servidor Streamlit real aqui**. O usuário deverá fazer o teste final em Windows (conforme README) antes de publicar. A conexão ao PostgreSQL privado também não foi testada nesta etapa; o site público não precisa dela.
