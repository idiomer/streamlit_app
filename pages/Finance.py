import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.stock_util import Stock
from config import stock_db_path

# Config
st.set_page_config(page_title='My Finance Playground', page_icon=':bar_chart:', layout='wide')
# Title
st.title('My Finance Playground')

# 0. 想法
st.header('〇、想法')
st.checkbox("""将未来N天的盈利天数占比做为标签预测""")

# 1. 指数历史走势
st.header('一、指数历史走势')
stock = Stock(stock_db_path)
stock2name = {'sh.000300': '沪深300', 'sh.000905': '中证500'}
for stock_code, stock_name in stock2name.items():
    base_df = stock.load_stock(stock_code)  # 从db或网络加载数据
    base_df['近5年25分位'] = base_df['close'].rolling(1200).apply(lambda x: np.percentile(x, q=25))
    base_df['近5年50分位'] = base_df['close'].rolling(1200).median()
    base_df['近5年75分位'] = base_df['close'].rolling(1200).apply(lambda x: np.percentile(x, q=75))

    base_df.rename({'date': '日期', 'close': '收盘价'}, axis=1, inplace=True)
    fig = px.line(base_df, x="日期", y=["收盘价", "近5年25分位", "近5年50分位", "近5年75分位"]
        ,title=stock_name+"历史走势")
    fig.update_xaxes(nticks=40, tickformat="%Y-%m-%d", tickangle=45)
    st.plotly_chart(fig, use_container_width=True, theme='streamlit')
