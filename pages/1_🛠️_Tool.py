import time
import datetime
import streamlit as st

st.title('Tools')

st.header('时间戳和日期互转')
with st.expander('', expanded=True):
    col1, col2 = st.columns(2, gap='large')
    with col1:
        input_timestamp = st.number_input('时间戳(秒)', min_value=0, format='%d')
        st.write('北京时间：', datetime.datetime.fromtimestamp(int(input_timestamp)))
    with col2:
        date_format = '%Y-%m-%d %H:%M:%S'
        input_date = st.text_input('北京时间', placeholder='1970-01-01 08:00:00')
        try:
            stamp = int(time.mktime(time.strptime(input_date, date_format))) if input_date else 0
        except:
            stamp = '日期格式有误'
        st.write('时间戳(秒)：', stamp)


st.header('简易计算器')
with st.expander('简易计算器', expanded=True):
    col1, col2 = st.columns(2, gap='large')
    result = '表达式有误'
    with col1:
        expr = st.text_input('Python算术表达式', placeholder='(1+2)*3 / 4**2')
        if len(expr)>0 and all([True if ch.isdigit() or ch in '+-*/().' else False for ch in expr]):
            try:
                result = eval(expr)
            except:
                pass
        else:
            if expr == '':
                result = 0
    with col2:
        st.write("计算结果为：", result)
