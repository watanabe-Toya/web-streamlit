import pandas  as pd
import streamlit as st
import yfinance as yt
import altair as alt

st.title("株価可視化アプリ")

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください。
 """)

st.sidebar.write("""
## 表示日数選択
""")

days=st.sidebar.slider("日付",1,50,20)

st.write(f"""
### 過去　**{days}日間**　のGAFAの株価
 """)

#@st.cacheで2回目の繰り返し処理が早くできる
@st.cache
def get_data(days,tickers):
    df=pd.DataFrame()
    for company in tickers.keys():
        tkr=yt.Ticker(tickers[company])
      
        hist=tkr.history(period=f"{days}d")

        #書き換え
        hist.index=hist.index.strftime("%d %B %Y")
        #closeだけ取り出す
        hist=hist[["Close"]]
        #名前を会社名に変更
        hist.columns=[company]
        hist=hist.T
        hist.index.name="Name"
        #結合して更新する
        df=pd.concat([df,hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin,ymax=st.sidebar.slider(
        "範囲を指定してください",0.0,5000.0,(0.0,4000.0))

    tickers={
        "apple" : "AAPL",
        "facebook" : "FB",
        "google" : "GOOGL",
        "microsoft" : "MSFT",
        "netflix" : "NFLX",
        "amazon": "AMZN"
    }
    df=get_data(days,tickers)
    companies=st.multiselect("会社名を選択してください。",
    list(df.index),
    ["google","amazon","facebook","apple"])

    if not companies:
        st.error("少なくとも1社は選んでください。")
    else:
        data=df.loc[companies]
        st.write("### 株価(USD)",data.sort_index())
        data=data.T.reset_index()
        data=pd.melt(data,id_vars=["Date"]).rename(columns={"value":"Stock Prices(USD)"})

        chart=(
        alt.Chart(data)
        .mark_line(opacity=0.8,clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q",stack=None,scale=alt.Scale(domain=[ymin,ymax])),
            color="Name:N"
        )
    )
    #画面サイズに合わせる
    st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        "エラーが発生しましました。"
    )







