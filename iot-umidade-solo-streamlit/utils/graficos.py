"""Visualizações interativas Plotly para séries físicas e históricas do projeto."""
import plotly.express as px
import plotly.graph_objects as go
from .dados import resumo_diario, variacoes

VERDE = '#0f9d86'
AZUL = '#1e4563'
DOURADO = '#d7a455'
CORES = ['#0f9d86','#245f87','#4e88b1','#94b9be','#d7a455','#ad846f']


def acabamento(fig, altura=410, ytitle=None):
    fig.update_layout(
        height=altura, template='plotly_white',
        margin=dict(l=12,r=22,t=28,b=28),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial, sans-serif',color='#233746',size=13),
        hovermode='x unified', showlegend=False,
        xaxis=dict(showgrid=False,showline=True,linecolor='#d9e4e8'),
        yaxis=dict(gridcolor='#e8eff2', zerolinecolor='#d5e0e5'),
    )
    if ytitle: fig.update_yaxes(title=ytitle)
    return fig


def serie_temporal(df, campo='adc'):
    ytitle = 'Leitura ADC (0–4095)' if campo=='adc' else 'Índice relativo experimental (%)'
    fig=go.Figure()
    for i,(dia,parte) in enumerate(df.groupby('dia')):
        fig.add_trace(go.Scatter(x=parte['data_hora'], y=parte[campo],
            name=dia.strftime('%d/%m'),mode='lines+markers',
            line=dict(color=CORES[i%len(CORES)],width=2.5),
            marker=dict(size=5),hovertemplate='%{x|%d/%m %H:%M}<br>%{y:.1f}<extra></extra>'))
    fig=acabamento(fig,440,ytitle)
    fig.update_layout(showlegend=True,legend=dict(orientation='h',y=-.18,x=0))
    return fig


def resumo_por_dia(df, campo='adc_medio'):
    r=resumo_diario(df).copy()
    r['dia_label']=r['dia'].apply(lambda dt:dt.strftime('%d/%m'))
    qual='ADC médio' if campo=='adc_medio' else 'Índice médio (%)'
    fig=go.Figure()
    if campo=='adc_medio':
        fig.add_trace(go.Bar(x=r['dia_label'], y=r[campo],name=qual,marker_color=AZUL,
            error_y=dict(type='data',symmetric=False,array=r['adc_max']-r['adc_medio'],
                arrayminus=r['adc_medio']-r['adc_min'],visible=True,color='#b1a58a'),
            hovertemplate='%{x}<br>ADC médio: %{y:.1f}<extra></extra>'))
    else:
        fig.add_trace(go.Bar(x=r['dia_label'], y=r['indice_medio'],marker_color=VERDE,
            hovertemplate='%{x}<br>Índice médio: %{y:.1f}%<extra></extra>'))
    return acabamento(fig,365,qual)


def distribuicao(df, campo='adc'):
    d=df.copy();d['dia_label']=d['dia'].apply(lambda x:x.strftime('%d/%m'))
    eixo='Leitura ADC' if campo=='adc' else 'Índice relativo experimental (%)'
    fig=px.box(d,x='dia_label',y=campo,points='all',color_discrete_sequence=[VERDE],
        labels={'dia_label':'Dia',campo:eixo}, hover_data=['hora'])
    fig.update_traces(jitter=.25,pointpos=0,marker_size=5)
    return acabamento(fig,390,eixo)


def mapa_calor(df, campo='indice'):
    pv=df.pivot_table(index='hora_cheia',columns='dia',values=campo,aggfunc='mean')
    pv=pv.sort_index()
    if pv.empty: return acabamento(go.Figure())
    fig=go.Figure(go.Heatmap(z=pv.values, x=[d.strftime('%d/%m') for d in pv.columns],
        y=pv.index.to_list(),colorscale=[[0,'#ecf5f4'],[.5,'#80cbbc'],[1,'#096c63']],
        texttemplate='%{z:.1f}', textfont=dict(size=12),
        colorbar=dict(title='ADC' if campo=='adc' else 'Índice %'),
        hovertemplate='%{x} | %{y}<br>%{z:.1f}'+(' ADC' if campo=='adc' else '%')+'<extra></extra>'))
    return acabamento(fig,340,'Horário')


def diferencas(df, limiar=30):
    v=variacoes(df).dropna(subset=['delta_adc']).copy()
    colors=[DOURADO if z<=-limiar else '#7898a7' for z in v['delta_adc']]
    fig=go.Figure(go.Bar(x=v['data_hora'],y=v['delta_adc'],marker_color=colors,
        hovertemplate='%{x|%d/%m %H:%M}<br>ΔADC: %{y:+.0f}<extra></extra>'))
    fig.add_hline(y=-limiar,line_dash='dot',line_color=DOURADO,
        annotation_text=f'Limiar exploratório −{limiar}',annotation_position='top left')
    return acabamento(fig,390,'Variação ADC entre leituras')


def histograma(df):
    fig=px.histogram(df,x='adc',nbins=25,color_discrete_sequence=[AZUL],
        labels={'adc':'Leitura ADC'})
    return acabamento(fig,350,'Contagem de leituras')


def teste_fisico(df):
    fig=go.Figure(go.Scatter(x=df['etapa'],y=df['solo_adc'],mode='lines+markers',
        line=dict(color=VERDE,width=3),marker=dict(size=11,color=VERDE),
        hovertemplate='%{x}<br>ADC: %{y}<extra></extra>'))
    fig=acabamento(fig,350,'Leitura ADC')
    fig.update_xaxes(tickangle=-22)
    return fig

def panorama_geral(df, campo='indice', mostrar_minutos=True):
    """Seis dias no mesmo gráfico: leituras originais, médias diárias e geral.

    Não cria novas medições: todas as estatísticas vêm das linhas recebidas.
    Cada dia tem seu próprio traço para NÃO desenhar medições inexistentes à noite.
    """
    if campo not in ('indice', 'adc'):
        raise ValueError('Indicador inválido para o panorama.')
    ytitle = 'Índice relativo experimental (%)' if campo == 'indice' else 'Leitura ADC'
    fig = go.Figure()
    if df.empty:
        return acabamento(fig, 475, ytitle)

    dados = df.sort_values('data_hora').copy()
    medias = []
    instantes = []
    rotulos = []
    totais = []
    for i, (dia, parte) in enumerate(dados.groupby('dia', sort=True)):
        parte = parte.sort_values('data_hora')
        if mostrar_minutos:
            fig.add_trace(go.Scatter(
                x=parte['data_hora'], y=parte[campo],
                name='Leituras registradas (1 min)',
                legendgroup='minutos', showlegend=(i == 0),
                mode='lines', opacity=0.58,
                line=dict(color='#87b9b5', width=1.7),
                hovertemplate='%{x|%d/%m às %H:%M}<br>Valor: %{y:.1f}<extra></extra>',
            ))
        # O marcador usa o centro da sessão somente como posição visual
        # da média do dia, não como uma observação naquele instante.
        instantes.append(parte['data_hora'].iloc[len(parte)//2])
        medias.append(float(parte[campo].mean()))
        rotulos.append(dia.strftime('%d/%m'))
        totais.append(len(parte))

    fig.add_trace(go.Scatter(
        x=instantes, y=medias, name='Média de cada dia',
        mode='lines+markers+text', text=[f'{x:.1f}' for x in medias],
        textposition='top center', textfont=dict(color='#1e4563', size=11),
        line=dict(color='#1e4563', width=3.2),
        marker=dict(size=11, color='#0f9d86', line=dict(color='white', width=1.3)),
        customdata=totais,
        hovertemplate='Dia %{x|%d/%m}<br>Média: %{y:.2f}<br>Registros: %{customdata}<extra></extra>'
    ))
    global_media = float(dados[campo].mean())
    sufixo = '%' if campo == 'indice' else ' ADC'
    fig.add_hline(
        y=global_media, line_dash='dash', line_color='#d7a455', line_width=2,
        annotation_text=f'Média geral: {global_media:.2f}{sufixo}',
        annotation_position='bottom left'
    )
    fig = acabamento(fig, 475, ytitle)
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation='h', y=-0.22, x=0),
        xaxis_title='Dias de novembro de 2026',
        margin=dict(l=20, r=18, t=30, b=40),
    )
    fig.update_xaxes(tickmode='array', tickvals=instantes, ticktext=rotulos,
                     showgrid=True, gridcolor='#edf1f2')
    return fig

