"""O texto dos gráficos deve refletir os valores reais da base e os filtros."""
from datetime import date
from utils.dados import carregar_publicacao
from utils import interpretacoes as exp


def test_interpretacao_panorama_e_medias():
    df = carregar_publicacao()
    assert len(df) == 1440
    assert '1.440' in exp.panorama(df, 'indice')
    assert 'média geral' in exp.panorama(df, 'indice')
    assert 'ADC' in exp.panorama(df, 'adc')
    texto = exp.medias_diarias(df, date(2026, 11, 21), 'indice')
    assert '21/11' in texto
    assert 'média geral' in texto


def test_interpretacoes_respeitam_os_filtros():
    df = carregar_publicacao()
    dia = df[df['dia'] == date(2026, 11, 21)].copy()
    foco = dia[dia['hora'].between('15:30', '15:50')]
    texto = exp.minuto(foco, 'indice')
    assert '15:30' in texto and '15:50' in texto
    assert 'porcentagem' not in exp.contexto('indice')
    horas = foco.groupby('hora_cheia', as_index=False)['indice'].mean()
    assert '15:00' in exp.horarios(horas, 'indice', False)
    assert '21/11' in exp.distribuicao(dia, 'adc')
    assert '21/11' in exp.calor(dia, 'indice')


def test_ultimas_interpretacoes_sem_inventar_chuva():
    df = carregar_publicacao()
    assert 'chuva' not in exp.panorama(df, 'indice').lower()
    assert 'chuva' not in exp.minuto(df.iloc[:20], 'adc').lower()
