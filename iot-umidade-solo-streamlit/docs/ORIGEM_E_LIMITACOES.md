# Procedência das informações e limitações

## Conjunto histórico

- Fonte: seis CSVs apresentados no projeto e analisados no notebook executado do autor.
- Período: 17–22 de novembro de 2026, 24 registros por dia (intervalo de 10 minutos, de 14h às 17h50).
- Natureza: **série de demonstração, sintetizada para testar o pipeline e as visualizações**.
- Total: **144 registros**.
- Consulta usada no relatório: `telemetria_iot.importacao_csv`, PostgreSQL.
- Colunas: `timestamp_local`, `solo_adc`, `indice_relativo_pct`.
- Na publicação, uma coluna de rastreabilidade `origem = historico_demonstrativo` foi acrescentada ao CSV exportado; as três colunas medidas/analisadas não foram alteradas.
- Um salto de índice observado no dia 21/11 corresponde ao cenário de teste. **Não significa chuva real comprovada**.

## Observações físicas

Os experimentos de 22/11/2026 mostram valores fora do solo próximos a 2618 ADC; registro antes da rega de 2501; queda para 1915 após adicionar água; valores seguintes 2060, 2119, 2136 e 2165. Outra coleta serial curta relatou 57 valores entre cerca de 20h03 e 20h12, com leitura ADC entre 2446 e 2471. O arquivo `dados/teste_fisico_validacao.csv` preserva exclusivamente observações selecionadas do relatório sem inventar horários, medições adicionais ou intervalos entre etapas.

## Calibração

O índice de umidade (%) é a transformação linear experimental `((2618 - adc)/(2618 - 1915))*100`, limitada entre 0 e 100. Ele **não corresponde a teor volumétrico ou massa percentual absoluta de água**. Os extremos exigem calibração posterior em condições controladas.

## Escopo

A bomba, relés, Wi-Fi, OLED e DHT11 são apenas candidatos a futuras integrações. A versão demonstrada tem leitura ADC, USB serial, CSV e análise PostgreSQL; não liga dispositivos elétricos.

## Divulgação pública

As fotografias selecionadas foram fornecidas pelo autor e reduzidas para uso na apresentação; os rodapés com detalhes pessoais da câmera foram cortados quando presentes. Não são incluídas senhas, usuários do banco institucional ou detalhes privados do servidor. A publicação pública usa um CSV próprio, não uma conexão externa permanente.
