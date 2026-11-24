# 🌱 Monitoramento de umidade do solo — IESB

## ✅ Atualização V4 — 24/11/2026

Este repositório contém a apresentação Streamlit do projeto ESP32 + sensor capacitivo V1.2.

**[Abrir aplicação Streamlit](https://iot-umidade-solo-app-sjimj8wsmsroawnwcxcn8n.streamlit.app/)**

### Novidades no Dashboard

- **Seleção de dia**, de 17 a 22/11/2026;
- **Filtro por intervalo de minutos** dentro do dia;
- **Visualização minuto a minuto** com destaque para maior e menor índice relativo;
- Comparação entre ADC bruto e índice relativo de umidade;
- Variação do ADC em janelas de dez minutos;
- Média por dia e comparação por horário;
- Explicações em linguagem simples sob os gráficos.

### Navegação

O projeto Streamlit está em [`iot-umidade-solo-streamlit/`](iot-umidade-solo-streamlit/) (arquivo principal: [`app.py`](iot-umidade-solo-streamlit/app.py)).

O CSV de divulgação já contém 1.440 pontos do **histórico demonstrativo**, incluindo valores interpolados. Não equivale a 1.440 medições físicas independentes. Testes reais com ESP32 aparecem separadamente.

### Fotografias

A pasta [`imagens/`](iot-umidade-solo-streamlit/imagens/) reúne imagens reais do projeto. Novos acessórios serão mostrados na galeria quando suas fotografias forem incluídas no repositório.

### Rodar localmente

```bash
cd iot-umidade-solo-streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**Desenvolvimento acadêmico — IESB, 2026.**
