# Publicação do site — Guia do zero (Windows)

Este guia foi escrito para o projeto **iot-umidade-solo-streamlit**, com arquivo de entrada `app.py` e dados prontos para publicação. Links oficiais consultados em novembro de 2026:

- [Criar um repositório GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [Documentação Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Fazer deploy da aplicação](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Gerenciar segredos](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## Parte A — Preparar a pasta do site

1. Extraia o ZIP para uma pasta chamada `iot-umidade-solo-streamlit`.
2. Abra a pasta: nela devem existir `app.py`, `requirements.txt`, `README.md`, `dados`, `imagens`, `utils` e `.streamlit`.
3. **Não inclua** qualquer arquivo chamado `.streamlit/secrets.toml` com senha; não inclua arquivos privados do banco.
4. Recomenda-se testar localmente antes de fazer upload público.

### Rodar no seu computador

1. No Explorador de Arquivos, entre na pasta do projeto.
2. Clique na barra do caminho, digite `cmd`, pressione Enter.
3. Execute:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

4. Abra o endereço mostrado no terminal, geralmente `http://localhost:8501`.
5. Teste navegação e filtros.
6. Para parar: `Ctrl + C`. Para sair do ambiente virtual: `deactivate`.

## Parte B — Criar o repositório no GitHub

1. Acesse [github.com](https://github.com/) e faça login.
2. No canto superior direito, use **+ → New repository** (ou seu equivalente atual).
3. Nome sugerido: `iot-umidade-solo-streamlit`.
4. Descrição sugerida: “Apresentação interativa do projeto IoT de monitoramento da umidade do solo — IESB”.
5. Escolha **Public** para usar como apresentação pública. Revise fotos e dados antes de publicar.
6. Para facilitar o upload manual, deixe as opções de README/gitignore inicial desmarcadas, pois já estão no pacote.
7. Clique em **Create repository**.

### Método 1 — Enviar os arquivos pelo navegador (mais fácil)

1. No novo repositório vazio, use **uploading an existing file** ou **Add file → Upload files**.
2. Abra a pasta do projeto e selecione **o conteúdo interno da pasta**, incluindo `app.py`, `requirements.txt`, `dados/`, `imagens/`, `utils/` e `docs/`.
3. Arquivos ocultos, como `.gitignore` e `.streamlit/config.toml`, podem exigir atenção extra no explorador. Garanta que a pasta `.streamlit` foi incluída.
4. **Não envie um ZIP como arquivo único**: o repositório deve mostrar diretamente `app.py` na raiz.
5. Revise o que será publicado para confirmar que não existe senha, `secrets.toml` real ou outro arquivo confidencial.
6. No campo da mensagem de commit, escreva `Versão inicial do site IoT` e clique em **Commit changes**.
7. Confira se `app.py` e `requirements.txt` aparecem na raiz do repositório.

### Método 2 — Enviar pelo terminal Git

Instale o [Git para Windows](https://git-scm.com/downloads/win) caso ainda não tenha. Na pasta raiz do projeto, abra um CMD e execute:

```bat
git init
git add .
git status
git commit -m "Versao inicial do projeto IoT"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/iot-umidade-solo-streamlit.git
git push -u origin main
```

**Substitua `SEU_USUARIO`** pelo seu nome de usuário no GitHub. O endereço é um **modelo**, não um link de repositório já existente. O `git status` deve ser verificado ANTES do commit para impedir arquivos indevidos. O GitHub pode solicitar autenticação pelo navegador.

Se o repositório remoto já tiver commits, use o método pelo navegador para evitar conflitos ou faça o procedimento Git com cuidado.

## Parte C — Publicar no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io/) e faça login.
2. Conecte sua conta GitHub quando solicitado; aprove as permissões necessárias.
3. No painel do Streamlit, clique **Create app**.
4. Se aparecer **Do you already have an app?**, escolha **Yup, I have an app**.
5. Selecione o repositório `SEU_USUARIO/iot-umidade-solo-streamlit`.
6. Branch: `main`.
7. **Main file path**: `app.py`.
8. Se aparecer campo para nome de aplicativo, escolha um nome disponível, como `iot-umidade-iesb`.
9. Em **Advanced settings**, mantenha uma versão de Python compatível (por exemplo, Python 3.12). **Não informe segredos** se for usar o CSV padrão.
10. Clique no botão de deploy. O serviço instalará automaticamente o `requirements.txt`.
11. Espere a interface concluir o deploy e abrir o site. O status e logs estarão no painel da aplicação.
12. Copie a URL `.streamlit.app` **realmente atribuída** pelo Streamlit. Não existe link válido antes desse passo.

O nome dos botões pode variar conforme atualizações da interface. Documentação oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Parte D — Testar o link antes de enviar ao professor

1. Abra a URL pública em **aba anônima** ou em outro dispositivo.
2. Confirme que fotos, tabelas e todos os gráficos aparecem.
3. Use **Dashboard** e escolha um intervalo menor. Verifique se os indicadores mudam.
4. Na página **Resultados**, confirme a distinção entre experimento físico e histórico demonstrativo.
5. Confira que nenhuma credencial, host interno ou dado privado é exibido.
6. Envie a URL do Streamlit ao professor junto com o relatório solicitado pela disciplina.

### Atualizar o site depois

1. Altere o arquivo local, teste e faça commit/push pelo terminal; ou envie uma nova versão pelo navegador.
2. O Streamlit acompanha o branch GitHub e atualiza a aplicação quando recebe novos commits.
3. Se a instalação falhar, abra os logs de deploy e confira `requirements.txt` e nomes dos arquivos.
4. Se as imagens falharem, confirme que a pasta `imagens` foi enviada e que os nomes são idênticos (maiúsculas/minúsculas importam na nuvem).

## Publicação com PostgreSQL privado (opcional)

A apresentação pública é pensada para funcionar com um CSV local e **não precisa** expor o banco institucional. Só configure PostgreSQL se possuir autorização institucional e um usuário limitado a leitura. Coloque os segredos no painel de configuração do Streamlit, **não no GitHub**. Para a maioria das apresentações, a fonte CSV é mais confiável e segura.
