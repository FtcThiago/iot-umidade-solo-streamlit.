"""Carga e indicadores do projeto de monitoramento do solo.

Os arquivos de publicação contêm SOMENTE o histórico demonstrativo documentado.
A conexão PostgreSQL é opcional e usa credenciais privadas do Streamlit Secrets.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FUSO = 'America/Sao_Paulo'
HISTORICO = ROOT / 'dados' / 'leituras_publicacao.csv'
TESTE_FISICO = ROOT / 'dados' / 'teste_fisico_validacao.csv'


def validar_e_preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza exclusivamente as três colunas que constam no notebook."""
    exigidas = {'timestamp_local', 'solo_adc', 'indice_relativo_pct'}
    faltam = exigidas - set(df.columns)
    if faltam:
        raise ValueError(f'Faltam colunas no dataset: {", ".join(sorted(faltam))}')
    d = df.copy()
    d['data_hora'] = pd.to_datetime(d['timestamp_local'], errors='coerce', utc=True).dt.tz_convert(FUSO)
    d['adc'] = pd.to_numeric(d['solo_adc'], errors='coerce')
    d['indice'] = pd.to_numeric(d['indice_relativo_pct'].astype('string').str.replace(',', '.', regex=False), errors='coerce')
    d = d.dropna(subset=['data_hora', 'adc', 'indice'])
    d = d[d.adc.between(0,4095) & d.indice.between(0,100)].copy()
    d['origem'] = d['origem'] if 'origem' in d.columns else 'historico_demonstrativo'
    d = d.drop_duplicates(subset=['data_hora', 'adc', 'indice']).sort_values('data_hora').reset_index(drop=True)
    d['dia'] = d['data_hora'].dt.date
    d['hora'] = d['data_hora'].dt.strftime('%H:%M')
    d['hora_cheia'] = d['data_hora'].dt.strftime('%H:00')
    return d


def carregar_publicacao() -> pd.DataFrame:
    return validar_e_preparar(pd.read_csv(HISTORICO))


def carregar_postgres_config(config: dict) -> pd.DataFrame:
    """Consulta SOMENTE a tabela documentada, em sessão de leitura."""
    import psycopg
    if not config:
        raise ValueError('Configuração PostgreSQL não disponível.')
    required = ['host', 'port', 'dbname', 'user', 'password']
    if any(not config.get(k) for k in required):
        raise ValueError('Preencha host, port, dbname, user e password nos secrets.')
    with psycopg.connect(
        host=config['host'], port=int(config['port']), dbname=config['dbname'],
        user=config['user'], password=config['password'], connect_timeout=8,
        options='-c default_transaction_read_only=on',
        application_name='streamlit_iot_apresentacao',
        sslmode=config.get('sslmode','prefer'),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT timestamp_local, solo_adc, indice_relativo_pct
                           FROM telemetria_iot.importacao_csv
                           ORDER BY timestamp_local LIMIT 100000''')
            rows = cur.fetchall()
    df = pd.DataFrame(rows,columns=['timestamp_local','solo_adc','indice_relativo_pct'])
    df['origem']='historico_demonstrativo'
    return validar_e_preparar(df)


def resumo_diario(d: pd.DataFrame) -> pd.DataFrame:
    if d.empty:
        return pd.DataFrame(columns=['dia','leituras','adc_medio','adc_mediana','adc_desvio', 'adc_min','adc_max','indice_medio','indice_min','indice_max'])
    return (d.groupby('dia',as_index=False)
        .agg(leituras=('adc','size'),adc_medio=('adc','mean'),adc_mediana=('adc','median'),
             adc_desvio=('adc','std'),adc_min=('adc','min'),adc_max=('adc','max'),
             indice_medio=('indice','mean'),indice_min=('indice','min'),indice_max=('indice','max'))
        .sort_values('dia'))


def variacoes(d: pd.DataFrame) -> pd.DataFrame:
    v=d.sort_values('data_hora').copy()
    v['delta_adc'] = v.groupby('dia')['adc'].diff()
    v['intervalo_min'] = v.groupby('dia')['data_hora'].diff().dt.total_seconds()/60
    v['queda_importante'] = v['delta_adc'] <= -30
    return v


def indicadores(d: pd.DataFrame) -> dict:
    if d.empty:
        return dict(n=0)
    return dict(n=len(d), dias=d['dia'].nunique(), adc_medio=d['adc'].mean(),
                adc_min=d['adc'].min(),adc_max=d['adc'].max(),
                indice_medio=d['indice'].mean(), desvio=d['adc'].std(),
                inicio=d['data_hora'].min(),fim=d['data_hora'].max())


def leituras_reais_referencia() -> pd.DataFrame:
    return pd.read_csv(TESTE_FISICO)


def converter_csv_download(d: pd.DataFrame) -> bytes:
    result = d[['data_hora','adc','indice','origem']].copy()
    result['data_hora']=result['data_hora'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return result.to_csv(index=False).encode('utf-8-sig')
