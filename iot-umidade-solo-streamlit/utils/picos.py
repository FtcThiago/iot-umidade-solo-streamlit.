"""Análise dos extremos de umidade relativa e mudanças em janelas de 10 minutos."""
import pandas as pd


def mudancas_em_dez_minutos(df: pd.DataFrame) -> pd.DataFrame:
    """Compara instantes separados por exatamente 10 minutos no mesmo dia."""
    campos = ['dia', 'data_hora', 'adc', 'indice']
    atual = df[campos].sort_values('data_hora').copy()
    atual['tempo_anterior'] = atual['data_hora'] - pd.Timedelta(minutes=10)
    anterior = df[campos].rename(columns={
        'data_hora': 'tempo_anterior',
        'adc': 'adc_anterior',
        'indice': 'indice_anterior',
    })
    saida = atual.merge(anterior, on=['dia', 'tempo_anterior'],
                         how='left', validate='many_to_one')
    saida['delta_adc_10min'] = saida['adc'] - saida['adc_anterior']
    saida['delta_indice_10min'] = saida['indice'] - saida['indice_anterior']
    return saida.dropna(subset=['delta_adc_10min']).sort_values('data_hora')


def resumo_dia(df: pd.DataFrame) -> dict:
    """Picos do intervalo selecionado, sem inferir causas físicas."""
    if df.empty:
        raise ValueError('O período selecionado está vazio.')
    serie = df.sort_values('data_hora').copy()
    janela = mudancas_em_dez_minutos(serie)
    return {
        'n': len(serie),
        'pico_umido': serie.loc[serie['indice'].idxmax()],
        'pico_seco': serie.loc[serie['indice'].idxmin()],
        'maior_aumento_10min': (
            janela.loc[janela['delta_indice_10min'].idxmax()]
            if not janela.empty else None
        ),
        'indice_medio': serie['indice'].mean(),
    }
