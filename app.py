#pip install streamlit requests textblob
#pip install yfinance matplotlib pandas
#pip install plotly
#  streamlit run app.py
#  pip install streamlit requests textblob yfinance plotly

import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go
from textblob import TextBlob
import datetime
import locale

# --------- Dados dos ativos --------
acoes = {
    "Banco do Brasil (BBAS3)": "BBAS3.SA",
    "Petrobras PN (PETR4)": "PETR4.SA",
    "Vale (VALE3)": "VALE3.SA",
    "Itaú Unibanco (ITUB4)": "ITUB4.SA",
    "Bradesco PN (BBDC4)": "BBDC4.SA",
    "Ambev (ABEV3)": "ABEV3.SA",
    "Magazine Luiza (MGLU3)": "MGLU3.SA",
    "B3 (B3SA3)": "B3SA3.SA",
    "Suzano (SUZB3)": "SUZB3.SA",
    "WEG (WEGE3)": "WEGE3.SA"
}
criptos = {
    "Bitcoin (BTC)": "BTC",
    "Ethereum (ETH)": "ETH",
    "Solana (SOL)": "SOL",
    "Ripple (XRP)": "XRP",
    "Cardano (ADA)": "ADA",
    "Dogecoin (DOGE)": "DOGE"
}
periodos = {"7 dias": 7, "15 dias": 15, "30 dias": 30, "90 dias": 90}
BADGES = [
    ("👋", "Novo visitante"),
    ("🔎", "Explorador de ativos"),
    ("🔥", "Assíduo: 10+ análises"),
    ("💰", "Simulador ativo")
]
GLOSSARIO = {
    "Sentimento": "Mede o clima (otimismo/pessimismo) das notícias do ativo.",
    "Polaridade": "Quanto um texto é positivo (+) ou negativo (-), de -1 a +1.",
    "Média móvel": "Indicador técnico que suaviza a curva de preços.",
    "Volume": "Quanto o ativo foi negociado em determinado período.",
    "Ranking de ativos": "Lista dos ativos com melhores e piores sentimentos recentes.",
    "Simulador": "Ferramenta virtual para ver quanto teria ganhado ou perdido investindo em determinada data.",
    "Tema escuro": "Em Streamlit: clique no menu lateral > Settings > Theme: Escuro."
}

# ----------------- Funções de negócio -----------------

def buscar_noticias_crypto(moeda):
    api_key = "335ac339603a1898b46c30f02064ca8ee45cda3820957c0c7e79f22f86eaa463"
    url = f"https://min-api.cryptocompare.com/data/v2/news/?categories={moeda}&lang=EN"
    headers = {"authorization": f"Apikey {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        noticias = [
            {"title": n.get("title"), "url": n.get("url")}
            for n in data.get("Data", [])
            if n.get("title") and isinstance(n.get("title"), str)
        ]
        return noticias
    else:
        return []

def buscar_noticias_acao(ticker, empresa_nome):
    api_key = "6448df59317341848edc932dd442d99b"
    busca = f'{ticker.replace(".SA","")} OR "{empresa_nome}"'
    url = (
        f'https://newsapi.org/v2/everything?q={busca}&language=pt&sortBy=publishedAt&pageSize=10&apiKey={api_key}'
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        noticias = [
            {"title": n.get("title"), "url": n.get("url")}
            for n in data.get("articles", [])
            if n.get("title") and isinstance(n.get("title"), str)
        ]
        return noticias
    else:
        return []

def analisar_sentimento(noticias):
    polarities = []
    for noticia in noticias:
        titulo = noticia.get("title")
        if titulo and isinstance(titulo, str):
            sentiment = TextBlob(titulo).sentiment.polarity
            polarities.append(sentiment)
    if len(polarities) == 0:
        return 0
    return sum(polarities)/len(polarities)

def prever_tendencia(sentimento):
    if sentimento > 0.1:
        return "😊", "POSITIVO", "Vai Subir?", "#47D147"
    elif sentimento < -0.1:
        return "😟", "NEGATIVO", "Vai Cair?", "#FF3C3C"
    else:
        return "😐", "NEUTRO", "Incerteza", "#FFD700"

def plotar_acao_interativo(ticker, dias):
    fim = datetime.datetime.today()
    inicio = fim - datetime.timedelta(days=dias+5)
    df = yf.download(ticker, start=inicio, end=fim)
    if df.empty or len(df) < dias // 2:
        return None
    df = df.tail(dias)
    df = df.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Close"],
        mode="lines+markers",
        line=dict(color="#1976D2"),
        marker=dict(size=9)
    ))
    fig.update_layout(
        title=f"Cotação dos últimos {dias} dias",
        xaxis_title="Data",
        yaxis_title="Preço de Fechamento (R$)",
        hovermode="x unified",
        template="plotly_white"
    )
    fig.update_xaxes(tickangle=45)
    return fig

def plotar_crypto_interativo(moeda, dias):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={moeda}&tsym=USD&limit={dias}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("Data", {}).get("Data", [])
        if not data:
            return None
        dates = [datetime.datetime.fromtimestamp(d["time"]).date() for d in data]
        prices = [d["close"] for d in data]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode="lines+markers",
            line=dict(color="#388E3C"),
            marker=dict(size=9)
        ))
        fig.update_layout(
            title=f"Cotação dos últimos {dias} dias",
            xaxis_title="Data",
            yaxis_title="Preço de Fechamento (USD)",
            hovermode="x unified",
            template="plotly_white"
        )
        fig.update_xaxes(tickangle=45)
        return fig
    else:
        return None

def mostrar_sentimento(sent, label, pergunta, cor, emoji):
    st.markdown(
        f"<div style='background-color:{cor};"
        f"border-radius:8px;padding:18px 22px;margin-bottom:8px'>"
        f"<span style='font-size:2.2rem;'>{emoji}</span>&nbsp; "
        f"<span style='font-size:1.5rem;font-weight:600;color:#222;'>{label}</span> "
        f"<span style='font-size:1.1rem; color:#222;'>"
        f" {'⬆️' if sent > 0.1 else '⬇️' if sent < -0.1 else '↔️'}"
        f"</span><br>"
        f"<span style='font-size:1.1rem;'>{pergunta}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<small>Média das polaridades: <b>{sent:.2f}</b> | -1 = muito negativo, +1 = muito positivo</small>",
        unsafe_allow_html=True
    )

# ------------ Badges/gamificação --------

def contar_analises():
    if "analises" not in st.session_state:
        st.session_state["analises"] = 0
    st.session_state["analises"] += 1
    return st.session_state["analises"]

def mostrar_badges():
    analises = st.session_state.get("analises", 1)
    badges = [BADGES[0]]
    if analises > 1:
        badges.append(BADGES[1])
    if analises > 10:
        badges.append(BADGES[2])
    st.markdown("".join([f"<span style='font-size:1.5rem;'>{b[0]}</span> <small>{b[1]}</small> &nbsp;" for b in badges]), unsafe_allow_html=True)

# --------- Ranking/top 3 widgets --------

@st.cache_data(ttl=300)
def ranking_sentimento():
    tabela_sentimento = []
    for nome, ticker in acoes.items():
        empresa_nome = nome.split('(')[0].strip()
        noticias = buscar_noticias_acao(ticker, empresa_nome)
        sent = analisar_sentimento(noticias)
        tabela_sentimento.append((nome, sent, "Ação"))
    for nome, moeda in criptos.items():
        noticias = buscar_noticias_crypto(moeda)
        sent = analisar_sentimento(noticias)
        tabela_sentimento.append((nome, sent, "Cripto"))
    return tabela_sentimento

def widget_ranking():
    st.markdown("## 📊 Ranking do Sentimento de Mercado")
    dados = ranking_sentimento()
    if dados:
        df_rank = sorted(dados, key=lambda x: x[1] if x[1] is not None else 0)
        st.markdown("#### 🟢 Top 3 otimismo")
        for ativo, sent, tipo in reversed(df_rank[-3:]):
            st.write(f"{'🪙' if tipo=='Cripto' else '📊'} `{ativo}`: **{sent:.2f}** {'🟢' if sent>0 else '🟡' if abs(sent)<=0.1 else '🔴'}")
        st.markdown("#### 🔴 Top 3 pessimismo")
        for ativo, sent, tipo in df_rank[:3]:
            st.write(f"{'🪙' if tipo=='Cripto' else '📊'} `{ativo}`: **{sent:.2f}** {'🟢' if sent>0 else '🟡' if abs(sent)<=0.1 else '🔴'}")
    st.write("---")

# -------------- Simulador virtual ---------

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def simulador_virtual(ativo, dias, tipo):
    st.markdown(f"### 💸 Simulação: Se eu tivesse investido R$ 1.000")
    if tipo == "Cripto":
        url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={ativo}&tsym=BRL&limit={dias}"
        data = requests.get(url).json().get("Data", {}).get("Data", [])
        if not data or len(data)<2:
            st.warning("Dados insuficientes.")
            return
        preco_inicio, preco_fim = data[0]["close"], data[-1]["close"]
    else:
        fim = datetime.datetime.today()
        inicio = fim - datetime.timedelta(days=dias+5)
        df = yf.download(ativo, start=inicio, end=fim)
        if df.empty or len(df)<2:
            st.warning("Dados insuficientes.")
            return
        preco_inicio, preco_fim = df['Close'].iloc[0], df['Close'].iloc[-1]
    rendimento = (preco_fim - preco_inicio)/preco_inicio
    valor_final = 1000*(1+rendimento)
    emoji = "🎉" if rendimento > 0 else "😬" if rendimento < 0 else "🤷‍"
    # Formatação pt-BR para valor_final
    valor_formatado = "R$ {:,.2f}".format(valor_final).replace(",", "X").replace(".", ",").replace("X", ".")
    percentual = f"{'+' if rendimento > 0 else ''}{rendimento*100:.2f}%"
    st.success(f"""
**Se você tivesse investido R$ 1.000 em {dias} dias:**
\n
Você teria agora **{valor_formatado}** {emoji}  ({percentual})
""")
# --------------- FEED EDUCATIVO -----------------

def feed_educativo_sidebar():
    st.markdown("## 🧠 Aprenda+ rápido")
    item = st.selectbox(":mag_right: Dica de mercado agora:", list(GLOSSARIO.keys()), key="aprenda")
    st.write(f"**{item}**: {GLOSSARIO[item]}")

# *************************************************
# ================= INTERFACE =====================
# *************************************************

st.set_page_config(page_title="Análise Cripto & Ações", layout="centered")
st.markdown("# 🏆 Analisador Interativo de Mercado Brasileiro")

with st.sidebar:
    st.markdown("## 🎮 Badges do Usuário")
    mostrar_badges()
    st.markdown("---")
    feed_educativo_sidebar()
    st.markdown("---")
    st.caption("*Sugestão: favorite esta página para acompanhar o ranking do sentimento do mercado!*")

widget_ranking()

col1, col2 = st.columns([1, 1])
with col1:
    opcao = st.radio("O que deseja analisar?", ["Criptomoedas", "Ações Brasileiras"], key="opcao")
with col2:
    periodo_txt = st.selectbox("Período do gráfico/simulação:", list(periodos.keys()), key="periodo")
dias_selecionados = periodos[periodo_txt]

if opcao == "Criptomoedas":
    moeda_nome = st.selectbox("Escolha a cripto:", list(criptos.keys()), key="cripto")
    ativo_ref = criptos[moeda_nome]
    display_name = moeda_nome
    ativo_tipo = "Cripto"
else:
    acao_nome = st.selectbox("Escolha a ação:", list(acoes.keys()), key="acao")
    ativo_ref = acoes[acao_nome]
    display_name = acao_nome
    ativo_tipo = "Ação"

st.markdown("---")
btn1, btn2 = st.columns(2)
btn_analisar = btn1.button("🔍 Analisar Tendência")
btn_simular = btn2.button("💸 Simular Investimento")

if btn_analisar or btn_simular:
    analises = contar_analises()
    with st.spinner("Buscando e analisando notícias e preços..."):
        if opcao == "Criptomoedas":
            noticias = buscar_noticias_crypto(ativo_ref)
        else:
            empresa_nome = display_name.split('(')[0].strip()
            noticias = buscar_noticias_acao(ativo_ref, empresa_nome)
        if not noticias:
            st.error("Não foi possível buscar notícias. Verifique as chaves das APIs ou tente novamente.")
        else:
            if btn_analisar:
                sentimento = analisar_sentimento(noticias)
                emoji, label, pergunta, cor = prever_tendencia(sentimento)
                mostrar_sentimento(sentimento, label, pergunta, cor, emoji)
                st.markdown("#### Principais notícias analisadas:")
                with st.expander("Abrir/Fechar notícias analisadas"):
                    for i, noticia in enumerate(noticias[:10]):
                        st.markdown(f"{i+1}. [{noticia['title']}]({noticia['url']})")
                st.divider()
                st.markdown(f"#### Gráfico dos últimos {dias_selecionados} dias de {display_name}")
                if opcao == "Criptomoedas":
                    fig = plotar_crypto_interativo(ativo_ref, dias_selecionados)
                else:
                    fig = plotar_acao_interativo(ativo_ref, dias_selecionados)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Não foi possível obter o gráfico para o ativo selecionado nesse período.")
            if btn_simular:
                simulador_virtual(ativo_ref, dias_selecionados, ativo_tipo)

st.caption(
    "Ferramenta experimental, sem fins de recomendação. "
    "Powered by CryptoCompare, NewsAPI, yfinance, Plotly & TextBlob | Feito por AlvaroTavares."
)

