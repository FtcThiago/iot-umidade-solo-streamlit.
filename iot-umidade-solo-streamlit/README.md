# 🌱 Da terra aos dados — Apresentação IoT no Streamlit

Aplicação de apresentação acadêmica do projeto **Sistema IoT de Telemetria e Análise da Umidade do Solo para Monitoramento de Plantas Domésticas**, desenvolvido no **Centro Universitário IESB** (2026), na graduação em Ciência de Dados e Inteligência Artificial.

**Autor:** Thiago Félix Teixiera Chaves · **Professor:** Sérgio Cortez

> **Estado atual:** aplicação publicada no [Streamlit Community Cloud](https://iot-umidade-solo-app-sjimj8wsmsroawnwcxcn8n.streamlit.app/); código versionado no GitHub.

## Visão geral

- A **ESP32** realiza leituras do sensor capacitivo de umidade V1.2 pelo **GPIO34** e envia os registros pela porta serial USB.
- Um script **Python** captura as leituras e associa data/hora, permitindo gravar CSV e outros formatos estruturados.
- O histórico foi importado para a tabela PostgreSQL `telemetria_iot.importacao_csv`, consultada no **DBeaver** e em **Jupyter Notebook**.
- A aplicação Streamlit organiza uma **apresentação navegável com oito seções** e oferece gráficos interativos com filtros.
- O controle automático de bomba, o monitoramento Wi-Fi remoto e a calibração física absoluta são **melhorias futuras**.

### ⚠️ Procedência do histórico

O arquivo `dados/leituras_publicacao.csv` contém **1.440 pontos de um histórico demonstrativo ampliado**, organizado entre **17 e 22/11/2026** (240 registros por dia, com intervalos de um minuto; 1.296 valores interpolados). Os dados correspondem à série utilizada na análise do relatório, mas **não são seis dias de aquisição física contínua**. A validação física em 22/11/2026 é mostrada **separadamente**, com observações selecionadas em `dados/teste_fisico_validacao.csv`. O índice relativo (%) é uma **transformação experimental** dos valores ADC; não é um percentual absoluto de água do solo.

## Estrutura do projeto

```text
iot-umidade-solo-streamlit/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── dados/
│   ├── leituras_publicacao.csv
│   └── teste_fisico_validacao.csv
├── imagens/
│   ├── iesb_logo.png
│   ├── planta_geral.jpg
│   ├── sensor_na_planta.jpg
│   ├── montagem_prototipo.jpg
│   ├── esp32.jpg
│   └── bomba_mangueira.jpg  (e outras fotos reais, ver a pasta)
├── utils/
│   ├── dados.py
│   └── graficos.py
└── docs/
    ├── roteiro_apresentacao.md
    ├── PUBLICACAO_GITHUB_STREAMLIT.md
    └── ORIGEM_E_LIMITACOES.md
```

## 1. Executar no Windows (iniciantes)

1. Extraia o ZIP deste projeto numa pasta local, por exemplo `Documentos\iot-umidade-solo-streamlit`.
2. Abra a pasta no Explorador de Arquivos, clique na barra de endereço, digite **`cmd`** e pressione Enter.
3. Instale as bibliotecas:

   ```powershell
   py -m pip install -r requirements.txt
   ```
4. Inicie a aplicação:

   ```powershell
   py -m streamlit run app.py
   ```
5. Abra o endereço local mostrado, geralmente `http://localhost:8501`.
6. Use a barra lateral para navegar pelas oito etapas. Na seção **Dashboard**, altere o período e o indicador para atualizar os gráficos.
7. Pressione `Ctrl + C` no terminal para encerrar.

**Opcional:** use ambiente virtual antes da instalação:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

O site **não exige ESP32 conectada** nem acesso ao PostgreSQL para funcionar em modo demonstração.

## 2. Fonte pública e fonte PostgreSQL

### CSV público — recomendado para apresentação

A aplicação usa por padrão `dados/leituras_publicacao.csv`. É uma cópia derivada dos mesmos seis CSVs incluídos no projeto de relatório. Não contém nomes de servidor, usuário ou senha.

### PostgreSQL privado — opcional

Se possuir autorização para consultar o banco com um usuário de **somente leitura**:

1. Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` **apenas em sua máquina**.
2. Configure os campos de conexão nesse arquivo privado.
3. Reinicie o Streamlit.
4. Na barra lateral, selecione **PostgreSQL privado**.

A consulta é fixa e apenas de leitura:

```sql
SELECT timestamp_local, solo_adc, indice_relativo_pct
FROM telemetria_iot.importacao_csv
ORDER BY timestamp_local
LIMIT 100000;
```

O arquivo real `secrets.toml` é bloqueado pelo `.gitignore`, mas **verifique sempre o que está sendo enviado ao GitHub**. Não publique credenciais, hosts internos, dumps privados ou dados não autorizados. Em hospedagem externa, conecte somente se houver autorização de acesso, política institucional compatível e infraestrutura liberada. O modo CSV funciona mesmo sem o servidor.

## 3. Funcionalidades da apresentação

| Seção | O que mostrar |
|---|---|
| Início | Proposta, foto da planta, panorama do projeto |
| Problema e proposta | Motivação, objetivos e escopo |
| Equipamentos | Fotos reais, função da ESP32, sonda e conectores, investimento |
| Como funciona | Fluxo interativo da leitura ao banco |
| Coleta e armazenamento | Explicação das colunas e consulta SQL |
| Dashboard | Filtros, métricas calculadas, gráficos Plotly, exportação CSV |
| Resultados | Validação física, mudanças do ADC e interpretação |
| Conclusão | Resultados alcançados e melhorias futuras |

Use **Modo apresentação** na lateral para deixar as explicações técnicas recolhidas durante a exposição oral.

## 4. Publicação no GitHub e Streamlit Community Cloud

Leia **[docs/PUBLICACAO_GITHUB_STREAMLIT.md](docs/PUBLICACAO_GITHUB_STREAMLIT.md)**. O tutorial inclui método pelo navegador, método por Git, configuração do Streamlit Community Cloud, obtenção do link e verificação de erros.

> O GitHub **guarda o repositório**. O Streamlit Community Cloud **executa a aplicação**. Apenas após o deploy concluído haverá link público real.

## 5. Bases e referências técnicas

- Relatório técnico do projeto, edição 2026 (material do autor).
- Notebook `Notebook_IoT_PostgreSQL_Importacao_CSV(2).ipynb` executado sobre a tabela PostgreSQL.
- [Documentação oficial Streamlit](https://docs.streamlit.io/)
- [Publicação no Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Psycopg 3](https://www.psycopg.org/psycopg3/docs/)

## 6. Limitações e verificações

- O código foi verificado sintaticamente e suas rotinas de análise podem ser testadas sem rede.
- A conexão com o PostgreSQL institucional **não é necessária** para a apresentação pública.
- Não há acionamento de bomba nem controle de dispositivos pelo site.
- A execução final do Streamlit deve ser verificada na máquina do usuário antes do deploy.
- Dados reais futuros devem ser documentados em arquivos próprios, identificados como experimentais e com coleta comprovável.


## Melhorias da versão 2 (em revisão)

- **Modo apresentação:** navegação por etapas com indicador visual e notas de fala discretas, acessíveis em cada tela.
- **Dashboard interativo:** escolha ADC ou índice experimental para atualizar panorama global, série por minuto, comparação diária e resumo por horário.
- **Análise contextual:** um resumo calculado para o intervalo escolhido explica a variação da média entre o primeiro e o último dia filtrado.
- **Critério exploratório ajustável:** no painel de padrões, o limiar das quedas de ADC pode ser alterado de 10 a 100; eventos não são apresentados como prova de chuva.
- **Galeria ampliada:** imagens reais adicionais da montagem e da planta.

### Verificação rápida antes de publicar

Execute `python -m pytest -q` se tiver `pytest` instalado, e depois `streamlit run app.py`.
Confirme que os filtros e gráficos mudam juntos, que a navegação funciona em celular e que o modo apresentação permite abrir o roteiro rápido.

Este ramo de desenvolvimento não altera os arquivos CSV nem as credenciais de conexão ao PostgreSQL.


## Dashboard e histórico ampliado — novembro/2026

A fonte pública contém 1.440 pontos para seis tardes (14h00–17h59). Mantém os 144 valores anteriores e acrescenta 1.296 estimativas interpoladas entre referências, permitindo demonstrar gráficos por dia, por minuto, por hora e mudanças em janelas de dez minutos. Esses 1.440 pontos não são 1.440 medições físicas independentes. Os testes físicos da ESP32 estão descritos separadamente.

O aplicativo expõe preços totais comprovados (R$ 76,32; R$ 7,56; R$ 11,33, total R$ 95,21), amplia a galeria com as imagens já publicadas e não apresenta dicas de apresentação. A bomba e os relés continuam reservados para evolução futura.

## Painel de gráficos com filtros (24/11/2026)

A página Dashboard mostra um **gráfico único com os seis dias**, suas **médias diárias** e a **média geral de todo o conjunto**, sem ligar sessões noturnas como se fossem medições. Também permite escolher **uma data**, ajustar o intervalo de **minutos**, alternar entre índice experimental (%) e ADC, e marcar os extremos (maior e menor índice).

A análise de mudança relevante compara medições separadas por **dez minutos**. Pontos consecutivos relacionados ao mesmo evento são agrupados; uma queda do ADC não identifica necessariamente uma causa física.

A exportação do banco `telemetria_iot.importacao_csv` foi validada: **1.440 linhas**, **240 por dia**, de **17 a 22/11/2026**, das **14h00 às 17h59**. Todos os valores do CSV do site coincidem com os da exportação recebida. O histórico inclui interpolação; não representa monitoramento físico ininterrupto.

### Fotos novas na galeria

O aplicativo suporta imagens opcionais em `imagens/galeria_extra/`. A galeria só exibe os arquivos que já foram enviados, sem imagens quebradas. As 15 fotos novas dos componentes estão no pacote fornecido no chat e devem ser enviadas ao mesmo diretório, preservando os nomes dos arquivos. Fotografia de componente adquirido não implica sua utilização no sistema de aquisição já validado.

## Revisão V5 — panorama geral e conferência de contagens

- Visão conjunta dos seis dias em um gráfico único, mostrando os valores minuto a minuto (opcionais), médias diárias e média global.
- Total atual: **1.440 registros, 240 por dia**. As **144 referências iniciais** não são o total atual; foram complementadas com 1.296 pontos interpolados/simulados.
- Médias da exportação validada: **2.456,98 ADC** e **22,90%** de índice relativo experimental.
- Os gráficos apenas agregam os valores do arquivo/banco escolhido. Não criam novas observações físicas ou eventos de chuva.
- Testes atualizados para o volume correto de dados e textos de documentação revisados.

## Correção V6 — compatibilidade com a base de 1.440 registros

A versão hospedada estava exibindo 144 registros apesar de o CSV mais recente
no GitHub conter 1.440. **Causa provável:** a função `buscar_csv()` utilizava
`@st.cache_data` sem TTL; a aplicação podia reutilizar o DataFrame anterior
quando o arquivo foi atualizado. O cache foi removido dessa função.

Verificações adicionadas à interface:

- Contador na barra lateral **"Registros realmente carregados"**, que reflete o DataFrame usado nos gráficos, sem número fixo.
- Validação obrigatória do CSV: 1.440 registros, seis dias, 240 por dia. Caso falhe, o aplicativo mostra um erro e para, em vez de exibir 144 linhas como se fosse tudo.
- Se o PostgreSQL privado opcional ainda retornar 144 linhas, o painel avisa e muda automaticamente para o CSV de 1.440 registros, **sem afirmar que o banco foi atualizado**.
- **Gráfico 1:** panorama geral das seis tardes, suas leituras minuto a minuto, médias diárias e média global.
- **Gráfico 2:** escolha um dia e o intervalo de minutos, com os picos identificados dentro da seleção.
- A versão da barra lateral e o rodapé foram atualizados para **V6** para facilitar a verificação de implantação.

A aplicação pública lê os registros do CSV. Para atualizar a tabela no banco PostgreSQL,
é necessário importar os registros no banco separadamente; o aplicativo não faz escritas no banco.
