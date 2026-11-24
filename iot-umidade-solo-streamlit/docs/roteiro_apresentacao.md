# Roteiro rápido — apresentação navegável (aprox. 7–9 minutos)

Este roteiro acompanha o site Streamlit; abra-o e utilize **Próxima etapa →** ao concluir cada parte. Não é necessário decorar as frases exatamente.

## 1. Início (45 segundos)

**Mostre:** fotografia geral da planta, cartões e título.

**Fale:** “O projeto busca medir alterações na umidade do solo de uma planta usando um sensor barato. A ESP32 lê os valores, o Python organiza as informações e depois conseguimos analisar o histórico.”

**Destaque:** demonstração de integração completa entre hardware e dados.

## 2. Problema e proposta (40 segundos)

**Mostre:** objetivo geral e foto da sonda.

**Fale:** “Em casa, muitas vezes avaliamos a terra apenas observando ou tocando. Minha proposta é transformar essa observação em registros numéricos para acompanhar a evolução.”

## 3. Equipamentos e montagem (1 minuto)

**Mostre:** fotos da ESP32, sensor e montagem; três conexões e tabela de gastos.

**Fale:** “A ESP32 lê um sensor capacitivo V1.2 usando GPIO34. Os outros dois fios fazem a alimentação de 3,3 V e o GND. O kit de monitoramento foi montado e testado. Com a compra dos componentes reservados para o futuro, o total documentado foi de R$ 95,21.”

## 4. Como funciona (50 segundos)

**Mostre:** a sequência de cinco etapas e escolha a etapa Python.

**Fale:** “A leitura começa no solo e termina em informação: sensor, ESP32, cabo USB, programa Python, CSV, PostgreSQL e análises. O Python acrescenta data e hora.”

## 5. Coleta e armazenamento (1 minuto)

**Mostre:** nomes das três colunas e trecho de SQL.

**Fale:** “O PostgreSQL guarda o histórico consultado na tabela telemetria_iot.importacao_csv. O DBeaver é a interface que usei para gerenciar esse banco. O ADC é a leitura bruta e o índice é apenas uma escala experimental mais simples de interpretar.”

## 6. Dashboard (1 minuto e 40 segundos)

**Mostre:** primeiro o panorama dos seis dias com médias diárias e média geral; depois selecione o dia, filtre minutos e destaque os picos; o mapa de calor é complementar.

**Fale:** “Esta parte usa um histórico demonstrativo de seis dias, com 1.440 registros (240 em cada dia), para exercitar as consultas e a análise. Podemos filtrar um dia e os indicadores são recalculados. Entre 17 e 20/11, a média de ADC cresce; em 21/11 aparece uma mudança no cenário.”

**Faça uma interação:** selecione 21/11, observe o pico das 15h40 no gráfico de janelas de dez minutos, e retorne ao panorama geral.

## 7. Resultados (1 minuto)

**Mostre:** gráfico categórico do teste físico, imagem do sensor no vaso e resultados.

**Fale:** “No teste físico, observei 2501 ADC antes da água e 1915 após adicionar água; essa queda mostrou que o sensor reagiu. Também fiz uma coleta serial curta com várias leituras estáveis. Já os seis dias mostrados no dashboard são demonstrativos e não significam seis dias de coleta física contínua.”

**Limitação:** “O índice relativo não é uma porcentagem absoluta de água do solo.”

## 8. Conclusão (50 segundos)

**Mostre:** foto da bomba e conclusão.

**Fale:** “Consegui integrar sensor, ESP32, Python e PostgreSQL e visualizar os resultados. No futuro, a ideia é calibrar melhor o sensor, coletar por mais tempo e só depois estudar a bomba e a irrigação automática com os cuidados elétricos necessários.”

## Checklist antes da aula

- [ ] Site abre sem erro e exibe fotos.
- [ ] Todas as oito páginas navegam corretamente.
- [ ] Filtro do dashboard realmente modifica indicadores.
- [ ] Gráficos e dados aparecem mesmo sem internet nem ESP32.
- [ ] Link público abre em navegador privado/anônimo.
- [ ] Não compartilhar credenciais ou dados do servidor institucional.
