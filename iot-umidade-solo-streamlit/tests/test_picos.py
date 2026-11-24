"""Testes de consistência dos dados e picos a cada 10 minutos."""
from datetime import date
from utils.dados import carregar_publicacao
from utils.picos import mudancas_em_dez_minutos, resumo_dia


def test_periodo_e_quantidade():
    df = carregar_publicacao()
    assert len(df) == 1440
    assert df['data_hora'].is_unique
    assert list(df.groupby('dia').size()) == [240] * 6
    assert df['data_hora'].min().strftime('%d/%m %H:%M') == '17/11 14:00'
    assert df['data_hora'].max().strftime('%d/%m %H:%M') == '22/11 17:59'


def test_pico_do_dia_21():
    df = carregar_publicacao()
    dia = df[df['dia'] == date(2026, 11, 21)]
    assert resumo_dia(dia)['pico_umido']['indice'] == 32.7
    mud = mudancas_em_dez_minutos(dia)
    maior_queda = mud.loc[mud['delta_adc_10min'].idxmin()]
    assert maior_queda['data_hora'].strftime('%H:%M') == '15:40'
    assert maior_queda['delta_adc_10min'] == -96


def test_230_janelas_por_dia():
    df = carregar_publicacao()
    for _, dia in df.groupby('dia'):
        assert len(mudancas_em_dez_minutos(dia)) == 230
        assert resumo_dia(dia)['n'] == 240
