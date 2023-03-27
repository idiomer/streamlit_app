import time
import datetime
import streamlit as st

st.title('🛠️Tools')


def calculator(n=1):
    col1, col2 = st.columns(2, gap='medium')
    result = '表达式有误'
    with col1:
        expr = st.text_input(f'Python算术表达式{n}', placeholder='(1+2)*3 / 4**2', key=f'cal_{n}')
        if len(expr)>0 and all([True if ch.isdigit() or ch in '+-*/().' else False for ch in expr]):
            try:
                result = eval(expr)
            except:
                pass
        else:
            if expr == '':
                result = 0
    with col2:
        st.write(f"计算结果{n}为：\n\n", result)


def timestamp_convertor(n=1):
    col1, col2 = st.columns(2, gap='large')
    with col1:
        input_timestamp = st.number_input('时间戳(秒)', min_value=0, format='%d')
        st.write('北京时间\n\n', datetime.datetime.fromtimestamp(int(input_timestamp)))
    with col2:
        date_format = '%Y-%m-%d %H:%M:%S'
        input_date = st.text_input('北京时间', placeholder='1970-01-01 08:00:00')
        try:
            stamp = int(time.mktime(time.strptime(input_date, date_format))) if input_date else 0
        except:
            stamp = '日期格式有误'
        st.write('时间戳(秒)\n\n', stamp)


c1, c2 = st.columns(2, gap='small')
with c1:
    st.subheader('时间戳转换')
    with st.expander('**时间戳转换**', expanded=True):
        timestamp_convertor(1)
with c2:
    st.subheader('计算器')
    with st.expander('**计算器**', expanded=True):
        calculator(1)
        calculator(2)


