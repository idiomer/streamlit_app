# # https://30days.streamlit.app/?challenge=Day+3
# """ requirement.txt
# pip install streamlit
# pip install plotly
# pip install streamlit_pandas_profiling
# """
# from datetime import datetime
# import time

# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
# import streamlit as st
# from streamlit_pandas_profiling import st_profile_report


# st.set_page_config(page_title='My Data Playground', page_icon=':bar_chart:', layout='wide')
# st.title('My Data Playground')

# with st.expander('About this app'):
#     st.write('This app shows the various ways on how you can layout your Streamlit app.')
#     # st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

# # st.write(st.secrets['message'])
# the_sidebar = st.sidebar.selectbox('分类1', ('功能演示', '文档链接'))
# sidebar2 = st.sidebar.selectbox('分类2', ('功能演示', '文档链接'))
# if the_sidebar == '功能演示':
#     st.write('## 0. DataFrame展示')
#     df = pd.DataFrame({
#         'first column': [1, 2, 3, 4],
#         'second column': [10, 20, 30, 40]
#     })
#     st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

#     st.write('## [1. st.button](https://docs.streamlit.io/library/api-reference/widgets/st.button)')
#     if st.button('Say hello'):
#         st.write('Why hello there')
#     else:
#         st.write('Goodbye')


#     st.header('2. st.selectbox')
#     option = st.selectbox(
#         'What is your favorite color?',
#         ('Blue', 'Red', 'Green'))
#     st.write('Your favorite color is ', option)


#     st.header('3. st.multiselect')
#     options = st.multiselect(
#         'What are your favorite colors',
#         ['Green', 'Yellow', 'Red', 'Blue'],
#         ['Yellow', 'Red'])
#     st.write('You selected:', options)


#     st.header('4. st.checkbox')
#     st.write('What would you like to order?')
#     icecream = st.checkbox('Ice cream')
#     coffee = st.checkbox('Coffee')
#     cola = st.checkbox('Cola')
#     if icecream:
#         st.write("Great! Here's some more 🍦")
#     if coffee: 
#         st.write("Okay, here's some coffee ☕")
#     if cola:
#         st.write("Here you go 🥤")


#     st.header('5. st.progress')
#     my_bar = st.progress(0)
#     for percent_complete in range(100):
#         time.sleep(0.05)
#         my_bar.progress(percent_complete + 1)
#     st.balloons()



#     st.header('6. st.form')
#     with st.form('my_form'):
#         st.subheader('**Order your coffee**')
#         # Input widgets
#         coffee_bean_val = st.selectbox('Coffee bean', ['Arabica', 'Robusta'])
#         coffee_roast_val = st.selectbox('Coffee roast', ['Light', 'Medium', 'Dark'])
#         brewing_val = st.selectbox('Brewing method', ['Aeropress', 'Drip', 'French press', 'Moka pot', 'Siphon'])
#         serving_type_val = st.selectbox('Serving format', ['Hot', 'Iced', 'Frappe'])
#         milk_val = st.select_slider('Milk intensity', ['None', 'Low', 'Medium', 'High'])
#         owncup_val = st.checkbox('Bring own cup')
#         # Every form must have a submit button
#         submitted = st.form_submit_button('Submit')
#     if submitted:
#         st.markdown(f'''
#             ☕ You have ordered:
#             - Coffee bean: `{coffee_bean_val}`
#             - Coffee roast: `{coffee_roast_val}`
#             - Brewing: `{brewing_val}`
#             - Serving type: `{serving_type_val}`
#             - Milk: `{milk_val}`
#             - Bring own cup: `{owncup_val}`
#             ''')
#     else:
#         st.write('☝️ Place your order!')




#     st.write('## [10. st.line_chart](https://docs.streamlit.io/library/api-reference/widgets/st.line_chart)')
#     chart_data = pd.DataFrame(
#         np.random.randn(20, 3),
#         columns=['a', 'b', 'c'])
#     st.line_chart(chart_data)


#     # st.header('20. `streamlit_pandas_profiling`')
#     # df = pd.read_csv('./penguins_cleaned.csv')
#     # pr = df.profile_report()
#     # st_profile_report(pr)

# elif the_sidebar == '文档链接':
#     st.write("""## 文档链接
# #### 文本
# - [st.write](https://docs.streamlit.io/library/api-reference/text/st.write)
# - [st.markdown](https://docs.streamlit.io/library/api-reference/text/st.markdown)
# - [st.header](https://docs.streamlit.io/library/api-reference/text/st.header)
# - [st.subheader](https://docs.streamlit.io/library/api-reference/text/st.subheader)
# - [st.caption](https://docs.streamlit.io/library/api-reference/text/st.caption)
# - [st.text](https://docs.streamlit.io/library/api-reference/text/st.text)
# - [st.latex](https://docs.streamlit.io/library/api-reference/text/st.latex)
# - [st.code](https://docs.streamlit.io/library/api-reference/text/st.code)
# #### 组件
# - [st.button](https://docs.streamlit.io/library/api-reference/widgets/st.button)
# - [st.slider](https://docs.streamlit.io/library/api-reference/widgets/st.slider)
# - [st.select_slider](https://docs.streamlit.io/library/api-reference/widgets/st.select_slider)
# - st.selectbox
# - st.file_uploader
# #### 图表
# - [st.line_chart](https://docs.streamlit.io/library/api-reference/widgets/st.line_chart)
# - [st.altair_chart](https://docs.streamlit.io/library/api-reference/widgets/st.altair_chart)

# """)
# else:
#     st.write('Unknown Exception')


# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


def dict2md(one_dict):
    md_list = []
    for name, url in one_dict.items():
        md_list.append(f'- [{name}]({url})')
    return '\n'.join(md_list)

chatgpt_sites = {
    'OpenAI': 'https://chat.openai.com/chat',
    'YQCloud': 'https://chat9.yqcloud.top',
    'GITHUB收集': 'https://github.com/xx025/carrot',
}
streamlit_sites = {
    'Streamlit API Reference': 'https://docs.streamlit.io/library/api-reference',
    'Streamlit API Cheatsheet': 'https://daniellewisdl-streamlit-cheat-sheet-app-ytm9sg.streamlit.app',
    'Streamlit Components Hub': 'https://components.streamlit.app',
    'Streamlit Gallery': 'https://streamlit.io/gallery',
}

# Config
st.set_page_config(page_title='My Data Playground', page_icon=':bar_chart:', layout='wide')

# Title
st.title('My Data Playground')

# Content
c1, c2, c3 = st.columns(3, gap='small')
with c1:
    st.success('**ChatGPT**'+'\n'+dict2md(chatgpt_sites), icon="💡")
with c2:
    st.warning('**Streamlit**'+'\n'+dict2md(streamlit_sites), icon="💻")
with c3:
    st.error('**Data: [Flipside Crypto](https://flipsidecrypto.xyz)**', icon="🧠")
