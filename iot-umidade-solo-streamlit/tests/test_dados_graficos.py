"""Testes de integridade e gráficos do conjunto de publicação."""
from utils.dados import carregar_publicacao, resumo_diario, variacoes, indicadores
from utils import graficos as g


def test_base_historica():
    df=carregar_publicacao()
    assert len(df)==1440
    assert df["dia"].nunique()==6
    assert df.groupby("dia").size().tolist()==[240]*6
    assert df["origem"].eq("historico_demonstrativo").all()
    assert df["adc"].between(0,4095).all()


def test_resumo_e_variacoes():
    df=carregar_publicacao()
    r=resumo_diario(df)
    assert r["leituras"].sum()==1440
    assert indicadores(df)["n"]==1440
    assert variacoes(df)["delta_adc"].isna().sum()==6


def test_graficos_filtrados():
    df=carregar_publicacao()
    dia=df[df["dia"].eq(df["dia"].iloc[0])].copy()
    assert len(dia)==240
    assert len(g.panorama_geral(df,'indice').data)==7
    assert len(g.panorama_geral(df,'adc',False).data)==1
    assert abs(df['indice'].mean()-22.9036111111)<0.001
    for fig in [g.serie_temporal(dia,"indice"),g.resumo_por_dia(dia,"indice_medio"),
                g.distribuicao(dia,"indice"),g.mapa_calor(dia,"adc"),
                g.diferencas(dia,limiar=50),g.histograma(dia)]:
        assert len(fig.data)>0
