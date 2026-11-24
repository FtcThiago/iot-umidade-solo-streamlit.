# Verificação de integridade — versão atual (24/11/2026)

- Conjunto de publicação: **1.440 linhas**, distribuídas em seis dias com **240 linhas por dia** (17–22/11/2026, 14h00–17h59).
- Valores calculados da exportação mais recente: ADC médio **2456,98194** e índice relativo experimental médio **22,90361%**.
- O gráfico de panorama geral usa a mesma fonte do dashboard e exibe todas as seis séries diárias, as médias de cada dia e a média global.
- O gráfico de picos compara registros separados por dez minutos dentro do mesmo dia, sem inventar amostras.
- Os testes automatizados verificam contagens, resumos, variações, datas e gráficos, inclusive o panorama geral.
- Observações físicas reais devem ser interpretadas separadamente dos registros de demonstração e interpolação.

Para validar o aplicativo no ambiente local (com dependências instaladas):

~~~powershell
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
python -m streamlit run app.py
~~~

A conferência da interface hospedada e a conexão com o PostgreSQL privado exigem testes de execução; não se deve declarar esses testes como aprovados apenas pela revisão do código.
