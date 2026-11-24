"""Explicações curtas, calculadas do próprio histórico exibido no Streamlit.

Não cria observações e não atribui variações a chuva ou rega.
O índice é apenas uma escala relativa experimental, não um teor absoluto de água.
"""
import pandas as pd

def num(v, casas=1):
    return f'{float(v):,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def unidade(campo):
    return '%' if campo == 'indice' else ' ADC'

def delta(a, b, campo):
    diferenca = float(b) - float(a)
    if abs(diferenca) < (0.05 if campo == 'indice' else 0.5):
        return 'permaneceu praticamente estável'
    direcao = 'subiu' if diferenca > 0 else 'caiu'
    sufixo = ' pontos percentuais' if campo == 'indice' else ' pontos ADC'
    return f'{direcao} {num(abs(diferenca))}{sufixo}'

def contexto(campo):
    if campo == 'adc':
        return 'Neste sensor, valores ADC menores costumam corresponder a maior umidade relativa, não a uma porcentagem absoluta.'
    return 'O índice é relativo e experimental: não mede diretamente o percentual de água da terra.'

def panorama(df, campo):
    grupos = df.groupby('dia', sort=True)[campo].mean().sort_index()
    inicio, fim = grupos.index[0], grupos.index[-1]
    dia_max, dia_min = grupos.idxmax(), grupos.idxmin()
    sufixo = unidade(campo)
    return (
        f'Os pontos claros são os registros minuto a minuto, separados por dia; a linha escura une as médias de cada dia. '
        f'De {inicio.strftime("%d/%m")} a {fim.strftime("%d/%m")}, a média {delta(grupos.iloc[0], grupos.iloc[-1], campo)}, '
        f'passando de {num(grupos.iloc[0])}{sufixo} para {num(grupos.iloc[-1])}{sufixo}. '
        f'A média geral dos {len(df):,} registros é {num(df[campo].mean())}{sufixo}. '
        f'O maior valor médio foi em {dia_max.strftime("%d/%m")} ({num(grupos.max())}{sufixo}) '
        f'e o menor em {dia_min.strftime("%d/%m")} ({num(grupos.min())}{sufixo}). '
        + contexto(campo)
    ).replace('1,440', '1.440')

def minuto(df, campo):
    d = df.sort_values('data_hora')
    a, b = d.iloc[0], d.iloc[-1]
    alto, baixo = d.loc[d[campo].idxmax()], d.loc[d[campo].idxmin()]
    sufixo = unidade(campo)
    return (
        f'Cada ponto representa um minuto da seleção de {a["hora"]} a {b["hora"]}. '
        f'O indicador {delta(a[campo], b[campo], campo)} ao longo do intervalo '
        f'({num(a[campo])}{sufixo} → {num(b[campo])}{sufixo}). '
        f'O maior valor foi {num(alto[campo])}{sufixo} às {alto["hora"]}, '
        f'e o menor, {num(baixo[campo])}{sufixo} às {baixo["hora"]}. '
        + contexto(campo)
    )

def medias_diarias(df, dia, campo):
    agrupado = df.groupby('dia', sort=True)[campo].mean().sort_index()
    if dia not in agrupado.index:
        return 'Não há dados na data escolhida.'
    selecao = agrupado.loc[dia]
    geral = df[campo].mean()
    dif = abs(selecao - geral)
    comparacao = 'acima' if selecao > geral else 'abaixo' if selecao < geral else 'igual à'
    sufixo = unidade(campo)
    return (
        f'Cada barra é a média de um dia; a barra verde marca {dia.strftime("%d/%m")}. '
        f'Nessa data, a média foi {num(selecao)}{sufixo}, '
        f'{num(dif)}{" ponto(s) percentuais" if campo == "indice" else " pontos ADC"} {comparacao} '
        f'média geral de {num(geral)}{sufixo}. '
        f'A comparação resume a tendência diária, sem substituir a observação minuto a minuto.'
    )

def horarios(agrupado, campo, comparando):
    if agrupado.empty:
        return 'Não há leituras nas faixas horárias escolhidas.'
    maior = agrupado.loc[agrupado[campo].idxmax()]
    menor = agrupado.loc[agrupado[campo].idxmin()]
    sufixo = unidade(campo)
    modo = 'entre os dias selecionados na comparação' if comparando else 'do dia escolhido'
    def horario(r):
        texto = str(r['hora_cheia'])
        if comparando:
            texto += ' de ' + str(r['dia_label'])
        return texto
    return (
        f'As barras apresentam a média por hora {modo}, calculada somente a partir dos minutos filtrados. '
        f'A maior média está em {horario(maior)} ({num(maior[campo])}{sufixo}) '
        f'e a menor em {horario(menor)} ({num(menor[campo])}{sufixo}). '
        + contexto(campo)
    )

def distribuicao(df, campo):
    por_dia = df.groupby('dia')[campo].agg(['min','max','median'])
    variacao = (por_dia['max'] - por_dia['min']).idxmax()
    amplitude = (por_dia['max'] - por_dia['min']).max()
    return (
        f'Os pontos mostram as leituras e as caixas resumem sua concentração em cada dia. '
        f'O dia {variacao.strftime("%d/%m")} apresentou a maior amplitude entre mínimo e máximo '
        f'({num(amplitude)}{unidade(campo)}). Uma caixa maior sugere mais variação entre as leituras, '
        f'não necessariamente mais umidade. ' + contexto(campo)
    )

def calor(df, campo):
    horas = df.groupby(['dia','hora_cheia'])[campo].mean()
    maior_dia, maior_hora = horas.idxmax()
    menor_dia, menor_hora = horas.idxmin()
    return (
        f'Cada célula é a média das leituras de uma hora de um dia. '
        f'O maior valor médio ocorreu em {maior_dia.strftime("%d/%m")} às {maior_hora} '
        f'({num(horas.max())}{unidade(campo)}); o menor, em {menor_dia.strftime("%d/%m")} às {menor_hora} '
        f'({num(horas.min())}{unidade(campo)}). A cor serve para comparar horas e dias de modo visual. '
        + contexto(campo)
    )

def fisico(df):
    antes = df[df['etapa'].str.contains('antes da água', case=False, regex=False)]
    depois = df[df['etapa'].str.contains('Após adicionar água', case=False, regex=False)]
    if antes.empty or depois.empty:
        return 'O gráfico reúne os testes físicos selecionados, em ordem de execução; o eixo horizontal representa etapas, não minutos.'
    x, y = float(antes.iloc[0]['solo_adc']), float(depois.iloc[0]['solo_adc'])
    return (
        f'No teste com a planta, a leitura caiu de {num(x,0)} para {num(y,0)} ADC '
        f'após adicionar água, uma diferença de {num(x-y,0)} pontos. '
        f'Isso mostra que o sensor reagiu à mudança no substrato. '
        f'Os pontos seguintes representam leituras posteriores; o eixo mostra etapas, e não intervalos de tempo iguais.'
    )
