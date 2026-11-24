"""Apresentação acadêmica interativa — Projeto IoT de umidade do solo.

Publicação padrão: CSV de histórico demonstrativo presente no repositório.
Opcional: PostgreSQL com credenciais armazenadas somente nos secrets do Streamlit.
"""
from __future__ import annotations
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.dados import (ROOT, carregar_publicacao, carregar_postgres_config,
                         resumo_diario, variacoes, indicadores,
                         leituras_reais_referencia, converter_csv_download)
from utils import graficos as g
from utils.picos import mudancas_em_dez_minutos, resumo_dia

st.set_page_config(page_title='Projeto IoT | Umidade do Solo — IESB',
                   page_icon='🌱', layout='wide', initial_sidebar_state='expanded')
IMAGENS = ROOT / 'imagens'
SECO, UMIDO = 2618, 1915
ETAPAS=[
    ('Início', '🏠'),
    ('Problema e proposta', '🎯'),
    ('Equipamentos e montagem', '🔧'),
    ('Como funciona', '🔄'),
    ('Coleta e armazenamento', '🗃️'),
    ('Dashboard', '📊'),
    ('Resultados', '🔎'),
    ('Conclusão e evolução', '🌿'),
]

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {font-family:"DM Sans",sans-serif;}
.stApp{background:#f6f9fa;color:#193241}
h1,h2,h3,[data-testid="stMetricLabel"]{font-family:"Manrope",sans-serif!important;letter-spacing:-.025em!important}
.block-container {padding-top:1.9rem;max-width:1280px;padding-bottom:3.7rem}
[data-testid="stSidebar"]{background:#f0f5f5;border-right:1px solid #d9e5e6}
[data-testid="stSidebar"] .stRadio label {font-size:.96rem}
[data-testid="stMetric"]{border:1px solid #e0e9eb;border-radius:17px;padding:17px 18px;background:#fff;box-shadow:0 4px 18px rgba(17,51,67,.035)}
[data-testid="stMetricValue"]{color:#153b4b;font-weight:780}
[data-testid="stMetricLabel"]{color:#57717e}
[data-testid="stImage"] img{border-radius:16px;object-fit:cover}
[data-testid="stPlotlyChart"]{background:white;border:1px solid #e2eaec;border-radius:17px;padding:9px 9px 1px 9px}
[data-testid="stExpander"]{border:1px solid #e0e9eb;border-radius:13px;background:#fff}
.stButton button[kind="primary"]{border-radius:10px;background:#0d766b;border-color:#0d766b}
.stButton button {border-radius:10px}
.hero{border-radius:23px;padding:37px 36px 33px;background:linear-gradient(115deg,#0f3344,#123d43 62%,#106657);color:#edf8f7;min-height:320px;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;width:280px;height:280px;right:-110px;top:-140px;border:1px solid rgba(196,244,226,.3);border-radius:50%;box-shadow:0 0 0 52px rgba(196,244,226,.045),0 0 0 114px rgba(196,244,226,.025)}
.hero h1{font-size:clamp(2rem,3.0vw,3.2rem);line-height:1.14;margin:.36rem 0 1.1rem;font-weight:790;letter-spacing:-.04em;color:#fff}
.hero p{font-size:1.03rem;color:#c4dfdc;max-width:600px;line-height:1.65}
.pill{display:inline-block;background:#1f6d66;color:#d1f8e8;border:1px solid #3a8a7e;padding:5px 12px;border-radius:99px;font-size:.77rem;font-weight:700;letter-spacing:.08em}
.eyebrow{color:#078b7c;font-weight:800;text-transform:uppercase;letter-spacing:.13em;font-size:.75rem;margin-bottom:7px}
.lead{font-size:1.09rem;color:#567080;line-height:1.6;margin-top:-.35rem;margin-bottom:1.2rem}
.soft-card{background:#fff;border:1px solid #e1eaec;border-radius:17px;padding:20px 22px;margin-bottom:13px;box-shadow:0 4px 18px rgba(14,50,67,.025);height:100%}
.soft-card h4{color:#183845;font-family:Manrope,sans-serif;font-size:1.0rem;margin:0 0 9px}
.soft-card p{color:#587180;line-height:1.55;margin:0;font-size:.94rem}
.small-tag{background:#e7f4ee;border:1px solid #c7e2d8;border-radius:9px;color:#127a68;padding:5px 9px;font-size:.8rem;font-weight:700;display:inline-block}
.note{border-left:3px solid #0f9d86;background:#eaf5f2;border-radius:0 11px 11px 0;padding:12px 17px;color:#315c5b;margin:16px 0;line-height:1.55}
.seq{border:1px solid #dae8e7;background:white;border-radius:14px;padding:18px;min-height:137px}
.seq b{font-size:1rem;color:#184958}.seq p{font-size:.88rem;color:#607786;margin:9px 0 0}
.caption{color:#6a838d;font-size:.80rem;margin-top:6px}
.kpi-band{margin:0 0 18px;background:#e9f4f0;border:1px solid #cee4dc;border-radius:13px;padding:12px 16px;color:#32635c}
.callout-strong{border:1px solid #d6e9e2;background:#eff8f3;border-radius:15px;padding:19px 22px;color:#24584f}
.source-note{color:#587780;font-size:.8rem;border-top:1px solid #e0e8e9;margin-top:22px;padding-top:11px}
.presentation-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid #d9e7e6;background:#fff;padding:11px 17px;border-radius:13px;margin-bottom:18px;color:#42636a;font-size:.87rem}
.presentation-bar b{color:#0b7168}.insight-card{border-left:4px solid #158c79;background:#fff;border-radius:11px;padding:16px 18px;margin:10px 0 16px;border-top:1px solid #e2ebea;border-right:1px solid #e2ebea;border-bottom:1px solid #e2ebea}
.insight-card strong{color:#153e45}.insight-card p{color:#53717a;margin:.35rem 0 0;line-height:1.5}
[data-testid="stCaptionContainer"]{color:#6c8590}
@media(max-width:760px){.hero{padding:25px 20px;min-height:auto}.block-container{padding-left:.8rem;padding-right:.8rem}.hero h1{font-size:2rem}}
</style>''',unsafe_allow_html=True)


def tag(txt):
    st.markdown(f'<span class="small-tag">{txt}</span>',unsafe_allow_html=True)


def section(kicker,title,subtitle=None):
    st.markdown(f'<div class="eyebrow">{kicker}</div>',unsafe_allow_html=True)
    st.title(title)
    if subtitle:st.markdown(f'<p class="lead">{subtitle}</p>',unsafe_allow_html=True)


def card(title,desc):
    st.markdown(f'<div class="soft-card"><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)


def imagem(path,caption=None):
    file=IMAGENS/path
    if file.exists(): st.image(str(file),use_container_width=True,caption=caption)


def nav_move(delta):
    atual=int(st.session_state.get('etapa',0))
    st.session_state.etapa=max(0,min(len(ETAPAS)-1,atual+delta))


if 'etapa' not in st.session_state:st.session_state.etapa=0
st.sidebar.image(str(IMAGENS/'iesb_logo.png'),width=94)
st.sidebar.markdown('### Projeto IoT')
st.sidebar.caption('Ciência de Dados e Inteligência Artificial  ·  IESB 2026')
st.sidebar.divider()
st.sidebar.markdown('**Navegação da apresentação**')
st.sidebar.radio('Seções',range(len(ETAPAS)),
    format_func=lambda i:f'{ETAPAS[i][1]}  {ETAPAS[i][0]}',
    key='etapa', label_visibility='collapsed')
idx=int(st.session_state.etapa)
st.sidebar.progress((idx+1)/len(ETAPAS),text=f'Etapa {idx+1} de {len(ETAPAS)}')
st.sidebar.toggle('Modo apresentação',value=True,key='modo_apresentacao',
    help='Mantém tabelas técnicas recolhidas; desative para expandir os detalhes.')
st.sidebar.caption('Visão resumida' if st.session_state.modo_apresentacao else 'Visão técnica ampliada')
st.sidebar.caption('Dados de apresentação: histórico demonstrativo. A validação física é mostrada separadamente.')
st.sidebar.divider()
st.sidebar.markdown('**Thiago Félix Teixiera Chaves**')
st.sidebar.caption('Prof. Sérgio Cortez')
st.sidebar.caption('Brasília · 2026')

# Dados públicos e opção privada: nenhuma credencial armazenada no repositório.
@st.cache_data(ttl=45,show_spinner=False)
def buscar_postgres(config: dict):
    return carregar_postgres_config(config)

@st.cache_data(show_spinner=False)
def buscar_csv():
    return carregar_publicacao()

try:
    configuracao_pg=dict(st.secrets['postgres']) if 'postgres' in st.secrets else None
except Exception:
    configuracao_pg=None

fonte='CSV de apresentação'
if configuracao_pg:
    fonte=st.sidebar.selectbox('Fonte de dados',
        ['CSV de apresentação','PostgreSQL privado'],index=0,
        help='A consulta ao PostgreSQL usa credenciais nos Secrets, nunca no repositório.')
try:
    if fonte=='PostgreSQL privado':
        base=buscar_postgres(configuracao_pg)
    else:
        base=buscar_csv()
except Exception:
    st.sidebar.warning('Banco indisponível. Exibindo histórico do CSV de apresentação.')
    fonte='CSV de apresentação'
    base=buscar_csv()

if base.empty:
    st.error('A fonte de dados não retornou registros válidos.')
    st.stop()


# ------------------ PÁGINAS ------------------
def tela_inicio():
    a,b=st.columns([1.32,1],gap='large')
    with a:
        st.markdown('''<div class="hero">
          <span class="pill">IESB · PROJETO DE INTERNET DAS COISAS</span>
          <h1>Da terra aos dados:<br>monitoramento inteligente do solo</h1>
          <p>Uma planta doméstica, um sensor capacitivo e uma ESP32. Um projeto que transforma sinais analógicos em registros, estatísticas e descobertas visuais.</p>
          <span style="font-size:.84rem;color:#88d9c8">Sensor → ESP32 → Python → PostgreSQL → Análise</span>
          </div>''',unsafe_allow_html=True)
    with b:imagem('planta_geral.jpg','Protótipo aplicado a uma planta doméstica — registro do projeto.')
    st.write('')
    c1,c2,c3,c4=st.columns(4,gap='medium')
    with c1:st.metric('Dias no histórico',str(base['dia'].nunique()))
    with c2:st.metric('Leituras do histórico',f'{len(base):,}'.replace(',','.'))
    with c3:st.metric('Custo documentado','R$ 95,21')
    with c4:st.metric('Gráficos analíticos','4 principais')
    st.write('')
    section('A proposta','Uma solução simples, de ponta a ponta',
            'O principal resultado é a integração entre montagem eletrônica, programação, armazenamento e análise de dados.')
    cols=st.columns(4,gap='medium')
    infos=[('01 · Hardware','O sensor detecta alterações na condição do substrato e a ESP32 lê o sinal.'),
           ('02 · Aquisição','As leituras são enviadas ao computador pela comunicação USB/Serial.'),
           ('03 · Persistência','Python organiza os valores em CSV; PostgreSQL armazena o histórico de análise.'),
           ('04 · Exploração','Gráficos e estatísticas ajudam a observar tendências e alterações no sinal.')]
    for col,(ti,de) in zip(cols,infos):
        with col:card(ti,de)
    st.markdown('<div class="note">O site utiliza um <b>histórico demonstrativo</b> para apresentar análises de vários dias. Os testes físicos realizados com a planta são apresentados separadamente, sem supor coleta contínua nesse período.</div>',unsafe_allow_html=True)
    st.button('Explorar os gráficos →',type='primary',key='ir_dashboard',
              on_click=nav_move,args=(5,))


def tela_problema():
    section('Etapa 01 · Motivação','Por que acompanhar a umidade do solo?',
            'Regar uma planta envolve decisões que frequentemente são feitas apenas pela aparência da terra ou por uma rotina fixa.')
    a,b=st.columns(2,gap='large')
    with a:
        card('Problema','Sem medição, pequenas mudanças na condição do substrato podem passar despercebidas. O controle manual tende a depender de observações pontuais.')
        card('Proposta','Construir um protótipo econômico para transformar as alterações percebidas por um sensor em dados consultáveis, organizados por data e horário.')
    with b:imagem('planta_detalhe.jpg','Sonda posicionada no solo, com os terminais acima da superfície.')
    st.subheader('Objetivo e entregas')
    a,b,c=st.columns(3)
    with a:card('Medir','Capturar a leitura analógica do sensor de umidade do solo.')
    with b:card('Armazenar','Registrar os dados e consultá-los em uma estrutura relacional.')
    with c:card('Analisar','Construir métricas e gráficos que mostrem a variação das leituras.')
    st.info('A irrigação automática foi prevista no escopo original, mas a primeira versão validada se concentra no monitoramento. A minibomba não é acionada por este site.')


def tela_equipamentos():
    section('Etapa 02 · Hardware','Componentes e montagem',
            'Uma arquitetura de baixo custo: ESP32, sensor capacitivo V1.2 e três conexões elétricas para a leitura analógica.')
    a,b,c=st.columns(3,gap='medium')
    with a:
        imagem('esp32.jpg','ESP32 DevKit — microcontrolador.')
        card('ESP32 DevKit','Lê o canal analógico GPIO34, calcula médias e transmite os dados por USB.')
    with b:
        imagem('sensor_capacitivo.jpg','Sensor capacitivo de umidade V1.2.')
        card('Sensor capacitivo','Fornece um sinal analógico relacionado à presença de água no substrato.')
    with c:
        imagem('montagem_prototipo.jpg','Fase de testes e montagem do circuito.')
        card('Cabos e protoboard','Jumpers e cabo USB auxiliaram as conexões e a validação inicial da montagem.')
    st.subheader('Conexões utilizadas')
    st.dataframe(pd.DataFrame([
        {'Terminal do sensor':'GND','Pino ESP32':'GND','Papel':'Referência elétrica'},
        {'Terminal do sensor':'VCC','Pino ESP32':'3V3','Papel':'Alimentação 3,3 V'},
        {'Terminal do sensor':'AOUT','Pino ESP32':'GPIO34 (D34)','Papel':'Leitura do sinal analógico'},
    ]),hide_index=True,use_container_width=True)
    with st.expander('Ver outros equipamentos e a previsão de investimento', expanded=not st.session_state.modo_apresentacao):
        a,b=st.columns([1,1])
        with a:imagem('componentes.jpg','Componentes disponíveis no kit adquirido.')
        with b:
            st.dataframe(pd.DataFrame([
                ('Kit ESP32 e acessórios','R$ 76,32'),('Sensor capacitivo V1.2','R$ 7,56'),
                ('Kit bomba de água (futuro)','R$ 11,33'),('Total documentado','R$ 95,21')],
                columns=['Aquisição','Custo']),hide_index=True,use_container_width=True)
            st.caption('A bomba, os relés, o visor OLED e o DHT11 não foram integrados ao protótipo validado.')
    st.subheader('Galeria ampliada — equipamentos e montagem')
    fotos=[('esp32.jpg','ESP32'),('sensor_capacitivo.jpg','Sensor capacitivo V1.2'),
           ('jumpers.jpg','Jumpers'),('montagem_prototipo.jpg','ESP32 e protoboard'),
           ('sensor_na_planta.jpg','Sensor na planta'),('sonda_no_solo.jpg','Sonda no solo'),
           ('planta_geral.jpg','Planta monitorada'),('planta_detalhe.jpg','Planta em detalhe'),
           ('componentes.jpg','Componentes adquiridos'),('rele.jpg','Relé — etapa futura'),
           ('bomba_mangueira.jpg','Bomba — etapa futura')]
    for inicio in range(0,len(fotos),3):
        colunas=st.columns(3,gap='medium')
        for col,(arquivo,legenda) in zip(colunas,fotos[inicio:inicio+3]):
            with col:imagem(arquivo,legenda)
    st.subheader('Galeria dos acessórios complementares')
    st.caption('As peças adicionais foram adquiridas, mas não integram o circuito de leitura validado. Alguns itens poderão ser usados em melhorias futuras.')
    fotos_extras = [
        ('modulo_rele_duplo.jpg', 'Relé de dois canais — expansão futura'),
        ('cabos_jumper_kit.jpg', 'Cabos jumper do kit'),
        ('leds_botoes.jpg', 'LEDs e botões para testes'),
        ('visao_modulos.jpg', 'Sensores e componentes disponíveis'),
        ('modulo_rele_simples.jpg', 'Relé de um canal — expansão futura'),
        ('sensor_luz_ldr.jpg', 'Sensor de luminosidade LDR'),
        ('esp32_close.jpg', 'ESP32 DevKit em detalhe'),
        ('sensor_movimento_pir.jpg', 'Sensor de movimento PIR'),
        ('sensor_dht11.jpg', 'DHT11 — temperatura e umidade do ar'),
        ('modulos_conjunto.jpg', 'Módulos complementares'),
        ('kit_usb_pilhas_jumpers.jpg', 'Cabo USB, suporte de pilhas e jumpers'),
        ('display_oled.jpg', 'Visor OLED — expansão futura'),
        ('protoboard_embalada.jpg', 'Protoboard'),
        ('bomba_agua.jpg', 'Bomba para futura irrigação'),
        ('cabo_usb.jpg', 'Cabo USB'),
    ]
    pasta_extra = IMAGENS / 'galeria_extra'
    presentes = [(nome, titulo) for nome, titulo in fotos_extras if (pasta_extra / nome).exists()]
    if presentes:
        for inicio in range(0, len(presentes), 3):
            colunas = st.columns(3, gap='medium')
            for col, (arquivo, legenda) in zip(colunas, presentes[inicio:inicio + 3]):
                with col:
                    st.image(str(pasta_extra / arquivo), caption=legenda, use_container_width=True)
    else:
        st.caption('As novas fotografias serão exibidas nesta seção quando a pasta galeria_extra for publicada.')
    st.markdown('<div class="note">Custos conforme comprovantes: kit ESP32 e acessórios <b>R$ 76,32</b>; sensor capacitivo <b>R$ 7,56</b>; kit de bomba para etapa futura <b>R$ 11,33</b>; total <b>R$ 95,21</b>. Durante os testes, mantenha toda eletrônica afastada de água e tomadas.</div>',unsafe_allow_html=True)


def tela_fluxo():
    section('Etapa 03 · Arquitetura','Como o sistema transforma terra em informação',
            'Siga o caminho da leitura física até a análise em Python.')
    items=[('1 · Sensor','Observa alterações do substrato e produz sinal analógico.'),
           ('2 · ESP32','Converte o sinal em ADC e transmite os valores pela serial.'),
           ('3 · USB / Python','Recebe a linha, associa o horário do computador e salva registros.'),
           ('4 · CSV / PostgreSQL','Organiza o histórico e permite consultas por data e valores.'),
           ('5 · Notebook / Site','Calcula estatísticas e apresenta gráficos interativos.')]
    cols=st.columns(5,gap='small')
    for col,(ti,de) in zip(cols,items):
        with col:st.markdown(f'<div class="seq"><b>{ti}</b><p>{de}</p></div>',unsafe_allow_html=True)
    st.write('')
    escolha=st.selectbox('Explore uma etapa do fluxo',range(5),
                        format_func=lambda i:items[i][0],index=2)
    detalhamento=[
        'O sensor capacitivo v1.2 é inserido no substrato, preservando os componentes e o conector acima da terra.',
        'A ESP32 usa o GPIO34, faz 20 amostras para compor uma média e envia leituras aproximadamente a cada 10 segundos.',
        'Um programa Python captura a comunicação serial e registra a data e a hora a partir do relógio do computador.',
        'Os arquivos CSV permitem importação no PostgreSQL. No projeto, a tabela consultada foi telemetria_iot.importacao_csv.',
        'O notebook permite analisar os 1.440 pontos demonstrativos por dia, minuto, horário e mudanças relevantes, com explicações simples.'
    ]
    st.markdown(f'<div class="callout-strong"><b>{items[escolha][0]}</b><br>{detalhamento[escolha]}</div>',unsafe_allow_html=True)
    st.subheader('Validação física documentada')
    st.write('Antes de construir o histórico analítico, o circuito foi testado com alterações reais do substrato: as leituras passaram de valores próximos a 2501 para 1915 após adição de água. Isso mostrou sensibilidade do protótipo, sem representar ainda uma calibração absoluta.')


def tela_coleta():
    section('Etapa 04 · Banco de dados','Da leitura da terra ao PostgreSQL',
            'O sensor produziu os valores ADC; a ESP32 enviou-os por USB; Python registrou os horários e CSV; o DBeaver importou os registros no banco.')
    st.subheader('1. Teste físico')
    st.write('O sensor capacitivo foi conectado à ESP32 (3V3, GND e GPIO34). O código Arduino enviou as leituras pela serial aproximadamente a cada dez segundos, nos testes reais.')
    st.subheader('2. Registro em Python')
    st.write('Um programa Python leu a porta serial COM3 e acrescentou data e hora a cada leitura, salvando três colunas em CSV: timestamp_local, solo_adc e indice_relativo_pct.')
    st.subheader('3. PostgreSQL com DBeaver')
    st.write('Os arquivos CSV foram importados manualmente pelo DBeaver para o banco PostgreSQL, na tabela `telemetria_iot.importacao_csv`. O notebook consulta esses registros e o site usa um CSV de publicação, sem expor senhas.')
    st.subheader('4. Histórico da demonstração')
    st.write('O conjunto de análise abrange 17 a 22 de novembro de 2026, das 14h00 às 17h59. São 240 pontos por dia, totalizando 1.440, com um minuto de intervalo. Partiu-se de 144 pontos de referência; os intervalos foram completados por interpolação e pequenas variações simuladas. **Não significa seis dias de coleta física contínua.**')
    c1,c2,c3=st.columns(3)
    with c1:card('Data e hora','timestamp_local — horário da leitura em Brasília.')
    with c2:card('ADC','solo_adc — valor analógico do sensor.')
    with c3:card('Índice relativo (%)','indice_relativo_pct — escala experimental baseada em ADC 2618 e 1915.')
    st.code('''SELECT timestamp_local, solo_adc, indice_relativo_pct
FROM telemetria_iot.importacao_csv
ORDER BY timestamp_local;''',language='sql')
    d=base[['data_hora','adc','indice']].head(8).copy()
    d['data_hora']=d['data_hora'].dt.strftime('%d/%m/%Y %H:%M')
    d.columns=['Data/hora','ADC','Índice relativo (%)']
    st.dataframe(d,hide_index=True,use_container_width=True)
    st.caption('O índice é uma transformação para comparação, não a porcentagem absoluta de água no solo.')

def tela_dashboard():
    section('Etapa 05 · Análise interativa', 'Evolução da umidade e picos',
            'Selecione um dia e intervalo de minutos para conhecer a variação do sensor e encontrar os pontos mais importantes.')
    st.caption('Histórico demonstrativo do PostgreSQL: 1.440 pontos em 6 tardes. Os testes físicos da ESP32 são apresentados na página Resultados.')
    dias = sorted(base['dia'].unique())
    dia = st.selectbox('Escolha o dia', dias,
        index=next((i for i, d in enumerate(dias) if d.strftime('%Y-%m-%d') == '2026-11-21'), 0),
        format_func=lambda d: d.strftime('%d/%m/%Y'), key='dia_dashboard')
    valores = ['Índice relativo (%)', 'ADC bruto']
    modo = st.radio('Indicador do gráfico', valores, horizontal=True, key='indicador_dashboard')
    coluna = 'indice' if modo == valores[0] else 'adc'
    nome_eixo = 'Índice relativo experimental (%)' if coluna == 'indice' else 'Leitura ADC'
    dia_completo = base[base['dia'] == dia].sort_values('data_hora').copy()
    horarios = dia_completo['hora'].tolist()
    if not horarios:
        st.warning('Não existem leituras na data escolhida.')
        return
    inicio, fim = st.select_slider('Filtrar horário da coleta (minuto a minuto)',
        options=horarios, value=(horarios[0], horarios[-1]), key='horario_dashboard')
    foco = dia_completo[dia_completo['hora'].between(inicio, fim)].copy()
    if foco.empty:
        st.info('Nenhuma leitura nesse horário.')
        return
    indic = resumo_dia(foco)
    mais_umido = indic['pico_umido']
    mais_seco = indic['pico_seco']
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric('Leituras no filtro', str(indic['n']))
    with c2:
        st.metric('Índice médio', f"{indic['indice_medio']:.1f}%")
    with c3:
        st.metric('Maior índice', f"{mais_umido['indice']:.1f}%", mais_umido['hora'], delta_color='off')
    with c4:
        st.metric('Menor índice', f"{mais_seco['indice']:.1f}%", mais_seco['hora'], delta_color='off')
    st.subheader('1 · Evolução minuto a minuto')
    fig = px.line(foco, x='data_hora', y=coluna,
        labels={'data_hora': 'Horário (Brasília)', coluna: nome_eixo})
    fig.update_traces(line=dict(color='#0f9d86', width=3), mode='lines+markers',
                      marker=dict(size=3), hovertemplate='%{x|%H:%M}<br>%{y:.1f}<extra></extra>')
    if st.checkbox('Destacar os picos de umidade no gráfico', value=True, key='marcar_picos'):
        for linha, nome, cor in [
            (mais_umido, 'Maior umidade relativa', '#198754'),
            (mais_seco, 'Menor umidade relativa', '#c75d48')
        ]:
            fig.add_trace(go.Scatter(
                x=[linha['data_hora']], y=[linha[coluna]], mode='markers+text',
                name=nome, text=[nome + ' · ' + linha['hora']], textposition='top center',
                marker=dict(color=cor, size=13, line=dict(color='white', width=2)),
                hovertemplate='%{text}<br>%{y:.1f}<extra></extra>'))
    fig.update_layout(height=470, hovermode='x unified', xaxis_title='Horário (Brasília)',
                      yaxis_title=nome_eixo, margin=dict(t=42, b=40))
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Cada ponto representa um minuto do histórico escolhido. As marcações identificam o maior e o menor índice do intervalo filtrado; o ADC bruto diminui quando a umidade relativa aumenta.')
    st.subheader('2 · Momentos de maior mudança')
    limiar = st.slider('Qual queda do ADC em dez minutos destacar?', 10, 100, 30, 5, key='limiar_picos')
    janelas = mudancas_em_dez_minutos(dia_completo)
    janelas = janelas[janelas['data_hora'].dt.strftime('%H:%M').between(inicio, fim)].copy()
    eventos = janelas[janelas['delta_adc_10min'] <= -limiar].copy()
    if eventos.empty:
        st.info(f'Nenhuma queda superior ou igual a {limiar} ADC em dez minutos neste intervalo. Isso não indica erro nos dados.')
    else:
        eventos['novo_evento'] = eventos['data_hora'].diff().dt.total_seconds().gt(600).fillna(True)
        eventos['grupo'] = eventos['novo_evento'].cumsum()
        destaques = (eventos.sort_values('delta_adc_10min')
                            .drop_duplicates('grupo').sort_values('data_hora'))
        nomes = destaques['data_hora'].dt.strftime('%d/%m %H:%M')
        destaque_fig = px.bar(x=nomes, y=-destaques['delta_adc_10min'],
                             labels={'x':'Horário de referência', 'y':'Queda do ADC em 10 minutos'})
        destaque_fig.update_traces(marker_color='#d7a455', text=(-destaques['delta_adc_10min']).round(0).astype(int), textposition='outside')
        destaque_fig.update_layout(height=340, margin=dict(t=38, b=35))
        st.plotly_chart(destaque_fig, use_container_width=True)
        for reg in destaques.itertuples(index=False):
            st.caption(f"{reg.data_hora.strftime('%d/%m às %H:%M')}: queda de {-reg.delta_adc_10min:.0f} pontos ADC em dez minutos.")
    st.caption('Janelas vizinhas que apontam para a mesma alteração foram agrupadas. Quedas de ADC são indicativas de maior umidade relativa, mas não provam chuva ou rega.')
    st.subheader('3 · Média diária: comparação entre os seis dias')
    resumo = resumo_diario(base).copy()
    resumo['dia_label'] = resumo['dia'].apply(lambda d: d.strftime('%d/%m'))
    cores = ['#0f9d86' if d == dia else '#9dbdbb' for d in resumo['dia']]
    media_fig = px.bar(resumo, x='dia_label', y='indice_medio',
                       text_auto='.1f', labels={'dia_label':'Dia', 'indice_medio':'Índice relativo médio (%)'})
    media_fig.update_traces(marker_color=cores, textposition='outside')
    media_fig.update_layout(height=360, yaxis_range=[0, max(40, resumo['indice_medio'].max() + 6)])
    st.plotly_chart(media_fig, use_container_width=True)
    st.caption('Compare os seis dias de forma simples: a barra verde destaca o dia selecionado, e as demais mostram a média do índice relativo de umidade.')
    st.subheader('4 · Comparação entre horários')
    comparar = st.checkbox('Comparar também com outros dias', value=False, key='comparar_dias')
    if comparar:
        aux = base[base['hora'].between(inicio, fim)].copy()
        aux['dia_label'] = aux['dia'].apply(lambda d: d.strftime('%d/%m'))
        horas = aux.groupby(['dia_label','hora_cheia'], as_index=False)['indice'].mean()
        hfig = px.bar(horas, x='hora_cheia', y='indice', color='dia_label', barmode='group',
                      labels={'hora_cheia':'Faixa horária','indice':'Índice médio (%)','dia_label':'Dia'})
    else:
        horas = foco.groupby('hora_cheia', as_index=False)['indice'].mean()
        hfig = px.bar(horas, x='hora_cheia', y='indice',
                      labels={'hora_cheia':'Faixa horária','indice':'Índice médio (%)'})
        hfig.update_traces(marker_color='#245f87')
    hfig.update_layout(height=380)
    st.plotly_chart(hfig, use_container_width=True)
    st.caption('As barras representam a média por faixa horária. Se a opção de comparação estiver marcada, mostram as mesmas faixas em outros dias.')
    with st.expander('Tabela dos minutos selecionados e download'):
        visao = foco[['data_hora','adc','indice']].copy()
        visao['data_hora'] = visao['data_hora'].dt.strftime('%d/%m/%Y %H:%M')
        visao.columns = ['Data/hora','Leitura ADC','Índice relativo (%)']
        st.dataframe(visao, hide_index=True, use_container_width=True, height=360)
        st.download_button('Baixar CSV do intervalo', data=converter_csv_download(foco),
                           file_name=f"umidade_{dia.strftime('%Y%m%d')}_{inicio.replace(':','')}_{fim.replace(':','')}.csv",
                           mime='text/csv', key='baixar_intervalo')
    with st.expander('Outros gráficos técnicos'):
        a, b = st.columns(2)
        with a:
            st.plotly_chart(g.distribuicao(base), use_container_width=True)
        with b:
            st.plotly_chart(g.mapa_calor(base), use_container_width=True)
        st.caption('Distribuição por dia e mapa de calor ajudam em análises técnicas, mas não são necessários para explicar os picos.')
    st.caption('O histórico de seis tardes é demonstrativo e inclui pontos interpolados: eles não representam novas observações físicas independentes.')

def tela_resultados():
    section('Etapa 06 · Evidências','Resultados e interpretação',
            'O protótipo foi testado fisicamente, e o histórico demonstrativo permitiu avaliar a análise de dados em janelas temporais.')
    a,b=st.columns([1.05,.95],gap='large')
    with a:
        st.subheader('Teste físico: resposta à água')
        obs=leituras_reais_referencia()
        st.plotly_chart(g.teste_fisico(obs),use_container_width=True)
        st.caption('Leituras reais selecionadas, na sequência registrada. Os intervalos de tempo entre etapas não foram medidos, portanto o eixo horizontal é categórico.')
    with b:
        imagem('sonda_no_solo.jpg','Sensor capacitivo instalado no vaso (registro do projeto).')
        st.write('A queda de **2501 para 1915 ADC** após adicionar água confirmou uma resposta do sensor à mudança de condição do substrato.')
        st.caption('Em outra coleta física curta, foram relatadas 57 leituras entre 20h03 e 20h12 em 22/11, com ADC de 2446 a 2471.')
    st.subheader('O que o histórico demonstrativo mostrou')
    r=resumo_diario(base)
    primeiro=r.iloc[0];mais_seco=r.loc[r.adc_medio.idxmax()]
    eventos=variacoes(base); event=eventos[eventos['delta_adc']<=-30]
    c1,c2,c3=st.columns(3)
    with c1:card('Tendência de secagem',f"O ADC médio passou de {primeiro.adc_medio:.1f} no primeiro dia para {mais_seco.adc_medio:.1f} em {mais_seco.dia.strftime('%d/%m')}.")
    with c2:card('Alteração relevante','O cenário demonstrativo inclui mudança relevante no ADC em 21/11, indicando maior umidade relativa.')
    with c3:card('Limite interpretativo','O índice é experimental; alterações rápidas não identificam, sozinhas, a causa da umidificação.')
    st.markdown('<div class="note">As observações de vários dias representam <b>um cenário de demonstração</b>. Não foram coletadas continuamente pelo sensor nos seis dias; a confirmação física está documentada em testes separados.</div>',unsafe_allow_html=True)


def tela_conclusao():
    section('Etapa 07 · Encerramento','Do protótipo à evolução futura',
            'A etapa atual entrega monitoramento, registro e análise; a automação da rega depende de desenvolvimento e validações adicionais.')
    l,r=st.columns([1.2,.8],gap='large')
    with l:
        st.subheader('O que foi alcançado')
        st.markdown('''- ✅ Leitura analógica de umidade com **ESP32 + GPIO34**.
- ✅ Comunicação serial do protótipo para o computador.
- ✅ Registro de leituras com Python e arquivos CSV.
- ✅ Consulta de histórico no **PostgreSQL** por notebook.
- ✅ Estatísticas e gráficos para análise exploratória.''')
        st.subheader('Próximos avanços')
        st.markdown('''- **Coleta física prolongada** e melhores referências de calibração.
- **Alertas e monitoramento remoto** mediante conectividade adequada.
- **Integração segura de bomba e relé**, em uma versão futura, com alimentação e proteção apropriadas.
- Modelos preditivos quando houver histórico real suficiente.''')
    with r:
        imagem('bomba_mangueira.jpg','Bomba e mangueira adquiridas, reservadas para desenvolvimento futuro.')
        st.markdown('<div class="callout-strong"><b>Escopo atual</b><br>Monitoramento e análise. O aplicativo não aciona bomba, relé ou nenhum equipamento físico.</div>',unsafe_allow_html=True)
    st.write('')
    st.markdown('''<div class="hero" style="min-height:150px;padding:28px 32px">
      <span class="pill">CONCLUSÃO</span>
      <h1 style="font-size:1.85rem">Uma solução simples, uma arquitetura completa.</h1>
      <p style="margin-bottom:0">O projeto demonstra como hardware de baixo custo, armazenamento relacional e visualização de dados podem se complementar no monitoramento ambiental doméstico.</p>
      </div>''',unsafe_allow_html=True)
    st.caption('Centro Universitário IESB · Graduação em Ciência de Dados e Inteligência Artificial · Prof. Sérgio Cortez')

PAGINAS=[tela_inicio,tela_problema,tela_equipamentos,tela_fluxo,tela_coleta,tela_dashboard,tela_resultados,tela_conclusao]
st.markdown(f'<div class="presentation-bar"><span><b>{ETAPAS[idx][1]} Etapa {idx+1:02d}/{len(ETAPAS):02d}</b> · {ETAPAS[idx][0]}</span><span>IESB · 2026</span></div>',unsafe_allow_html=True)
PAGINAS[idx]()
st.divider()
prev,next_=st.columns([1,1])
with prev:
    st.button('← Etapa anterior',disabled=idx==0,on_click=nav_move,args=(-1,),use_container_width=True)
with next_:
    st.button('Próxima etapa →',disabled=idx==len(ETAPAS)-1,on_click=nav_move,args=(1,),type='primary',use_container_width=True)
st.caption('Projeto acadêmico de IoT · Dados demonstrativos e experimentos físicos apresentados com procedência distinta · IESB 2026')
