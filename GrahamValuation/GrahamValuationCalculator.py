import streamlit as st
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_analysts_info
import pandas_datareader as pdr

st.header("Graham's Stock Valuation Calculator")

ticker = st.text_input('Ticker', 'AAPL')
ng_pe = st.text_input('No Growth PE', 8.5)
multiplier = st.text_input('Multiplier of Growth Rate', 2)
margin = st.text_input('Margin of Safety(%)', 35)

data = {}
def get_data(ticker, ng_pe, multiplier, margin):
    quote = si.get_quote_table(ticker)
    current_price = quote["Quote Price"]
    eps = quote["EPS (TTM)"]
    growth_df = get_analysts_info(ticker)['Growth Estimates']
    growth_rate = growth_df.iloc[4][1]
    growth_rate = growth_rate.rstrip("%")
    aaa_df = pdr.get_data_fred('AAA')
    current_yield = aaa_df.iloc[-1][0]

    output = {
        "current_price": float(current_price),
        "eps": float(eps),
        "growth_rate": float(growth_rate),
        "current_yield": float(current_yield),
        "ng_pe": float(ng_pe),
        "multiplier": float(multiplier),
        "margin": float(margin)
    }
    return output 

if st.button('Calculate'):
    data = get_data(ticker, ng_pe, multiplier, margin)

    st.markdown("""---""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="EPS($)", value=data["eps"])
    with col2:
        st.metric(label="Projected Growth Rate (5 years)", value=data["growth_rate"])
    with col3:
        st.metric(label="Current Yield AAA Corp Bond", value=data["current_yield"])   

    st.markdown("""---""")

    int_value = (data["eps"] * (data["ng_pe"] + data["multiplier"] * data["growth_rate"] ) * 4.4)/ data["current_yield"]
    int_value = round(int_value,2)
    stock_price = round(data["current_price"],2)
    margin_rate = data["margin"] / 100
    accept_price = (1-margin_rate) * int_value
    accept_price = round(accept_price,2) 

    col4, col5, col6 = st.columns(3)
    with col4:
        st.subheader('Current Stock Price($)')
        st.subheader("**:blue[" + str(stock_price) + "]**")       
    with col5:
        st.subheader('Intrinsic Stock Value($)')
        st.subheader("**:blue[" + str(int_value) + "]**")
    with col6:
        st.subheader('Acceptable Buy Price($)')
        st.subheader("**:blue[" + str(accept_price) + "]**")
else:
    st.text("Click on Calculate button")




