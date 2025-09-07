# Principais-criptomoedas-e-acoes-brasileiras
Este projeto é um dashboard interativo que analisa as principais criptomoedas e ações brasileiras, fornecendo um "termômetro de sentimento" do mercado baseado nas últimas notícias, gráficos de desempenho e recursos de engajamento como badges, simulador e glossário financeiro. Ele utiliza Streamlit para interface web, Plotly para gráficos interativos, TextBlob para análise de sentimento e integra APIs do CryptoCompare, NewsAPI e Yahoo Finance. Indicadores visuais, ranking de sentimento e elementos de gamificação tornam a experiência envolvente para investidores e entusiastas do mercado financeiro.

README.md Pronto para o GitHub
🏆 Analisador de Tendência de Criptomoedas & Ações Brasileiras

dashboard

Este projeto é um painel interativo para análise de sentimento, notícias e gráficos das principais criptomoedas e ações brasileiras. Um verdadeiro "termômetro do mercado" brasileiro e internacional, pronto para investidores e curiosos!

🚀 Funcionalidades
Ranking em tempo real dos ativos com sentimento mais otimista e pessimista.
Análise de sentimento automática sobre as últimas notícias.
Gráfico de preços interativo (7, 15, 30, 90 dias) usando Plotly.
Simulador virtual de investimento: veja quanto teria ganho/perdido se investisse R$1.000 no passado.
Gamificação: badges, contador de análises, experiência customizada.
Glossário educativo ("Aprenda+") e dicas de mercado no sidebar.
Interface moderna, responsiva e acessível.
🏗️ Tecnologias usadas
Streamlit (app web interativo)
Plotly (gráficos com zoom e hover)
TextBlob (análise de sentimento)
yfinance (cotações históricas ações)
APIs: CryptoCompare, NewsAPI
💻 Como usar
Clone este repositório

git clone https://github.com/seuusuario/nome-do-repo.git

cd nome-do-repo

Instale as dependências
bash
Copiar

   pip install streamlit requests textblob yfinance plotly
Cole suas API keys nas funções:
Abra app.py e substitua:

 - `"SUA_API_KEY_CRYPTOCOMPARE"` por sua chave do [CryptoCompare](https://min-api.cryptocompare.com/)
 - `"SUA_API_KEY_NEWSAPI"` por sua chave do [NewsAPI](https://newsapi.org/)
Inicie o app

bash
Copiar

   streamlit run app.py
Acesse no navegador o endereço mostrado (ex: http://localhost:8501)

🎨 Tema Claro/Escuro
Para ativar tema escuro, clique no menu lateral do Streamlit (Settings > Theme > Dark).


🏅 Gamificação e Engajamento
Ganhe badges por uso recorrente!
Veja as ações e criptos mais "quentes" do dia no ranking.
Simule ganhos virtuais e aprenda termos do mercado com o Aprenda+.
📚 Glossário e Didática
O dashboard inclui um glossário dinâmico ("Aprenda+") no menu lateral, com explicações claras de termos como "sentimento", "polaridade", "volume", entre outros.

📷 Imagem de exemplo
Inclua aqui um print do seu dashboard para chamar atenção (use o Streamlit, tire o print e troque o link acima).

📝 Contribua!
Sugestões, melhorias e novos recursos são bem-vindos!

Abra um issue ou envie seu pull request.

⚠️ Aviso
Esta ferramenta é apenas para fins educacionais e informativos. Não constitui recomendação de investimento. Consulte sempre um profissional do mercado.


Desenvolvido por AlvaroTavares
