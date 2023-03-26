import time, datetime
import sqlite3

import requests
import baostock as bs
import pandas as pd

def get_date(n, base_date=None, fmt='%Y-%m-%d'):
    if base_date is None:
        base_date = time.strftime('%Y-%m-%d')
    base_dt = datetime.datetime.strptime(base_date, fmt)
    the_dt = base_dt + datetime.timedelta(days=n)
    return the_dt.strftime(fmt)

class Stock:
    def __init__(self, db_path=None) -> None:
        self.db_path = db_path

    @staticmethod
    def print_help():
        help_str = """
        stocks = {
            'sh.000300': '沪深300',
            'sh.000905': '中证500',
        }
        st = Stock('Z:/alipan/stock/stock.db')
        for stock_code in stocks.keys():
            st.init_stock(stock_code)    # 若数据库中已存在则自动跳过初始化
            st.update_stock(stock_code)
            print()        
        for stock_code in stocks.keys():
            st.init_or_update_index_pe_pb(stock_code)
            print()

        df = st.load_stock('sh.000300')  # 从db或网络加载数据
        # df = Stock().get_stock_history('sh.000300')  # 从网络加载数据
        pepb_df = st.load_index_pepb('sh.000300')  # 从db或网络加载数据
        df300 = base_df.merge(pepb_df, on=['date', 'code'], how='left')
        """.replace('\n'+' '*8, '\n')
        print(help_str)

    @staticmethod
    def print_schema() -> None:
        schema_str = """
        # date:         string:    日期(2023-01-03)
        # code:         string:    标的代码(sh.000300)
        # open:         float64:   开盘价(3864.8356)
        # high:         float64:   最高价(3893.9904)
        # low:          float64:   最低价(3831.2450)
        # close:        float64:   收盘价(3887.8992)
        # preclose:     float64:   昨日收盘价(3871.6338)
        # volume:       int64:     成交量(11505187500)
        # amount:       float64:   成交额(2.075402e+11)
        # adjustflag:   int32:     (3)
        # trun:         float64:   换手率(0.401618)
        # tradestatus:  int32:     交易状态(1)
        # pctChg:       float64:   当日跌涨幅百分比(0.420117)
        # isST:         int32      是否ST(0)
        """.replace('        # ', '')
        print(schema_str)

    def _read_sql_query(self, sql):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn)

    def _read_sql_table(self, table_name):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(f'SELECT * FROM {table_name}', conn)

    def get_stock_history(self, code='sh.000300', start_date='2004-12-31', end_date=None, verbose=False):
        lg = bs.login()
        if verbose:
            print('login respond error_code:'+lg.error_code)
            print('login respond  error_msg:'+lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=start_date, end_date=end_date or time.strftime('%Y-%m-%d'),
            frequency="d", adjustflag="3")
        bs.logout()
        if verbose:
            print('query_history_k_data_plus respond error_code:'+rs.error_code)
            print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        # 整理数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)

        # 手动转换数据类型
        for col in df.columns:
            if col in 'open,high,low,close,preclose,amount,turn,pctChg'.split(','):
                df[col] = df[col].astype('float64')
            if col in 'volume'.split(','):
                df[col] = df[col].astype('int64')
            if col in 'adjustflag,tradestatus,isST'.split(','):
                df[col] = df[col].replace('', '-1').astype('int32')
        return df

    def _format_code(self, code, format='lower.digit'):
        parts = code.split('.')
        assert len(parts) == 2, 'code must be like sh.000300 or 000300.SH'
        if parts[0].isdigit() and parts[1].isalpha():
            digit, alpha = parts
        elif parts[0].isalpha() and parts[1].isdigit():
            alpha, digit = parts
        else:
            raise ValueError('code must be like sh.000300 or 000300.SH')

        if format == 'standard' or format == 'lower.digit':
            return f'{alpha.lower()}.{digit}'
        elif format == 'upper.digit':
            return f'{alpha.upper()}.{digit}'
        elif format == 'digit.lower':
            return f'{digit}.{alpha.lower()}'
        elif format == 'digit.upper':
            return f'{digit}.{alpha.upper()}'
        else:
            raise ValueError('format error')

    def _get_table_name_by_code(self, code, prefix='', postfix=''):
        code = self._format_code(code, 'standard')
        tb_name = code.replace('.', '')
        if prefix: tb_name = prefix + '_' + tb_name
        if postfix: tb_name = tb_name + '_' + postfix
        return tb_name

    def get_index_guzhi(self, code, category='pe'):
        """ 从网页抓取指数pe或pb
        来源: https://funddb.cn/site/index
        """
        code = self._format_code(code, 'digit.upper')
        url = "https://api.jiucaishuo.com/v2/guzhi/newtubiaolinedata"
        payload = {"gu_code": code, "pe_category": category, "year": -1} # -1:全部
        resp = requests.post(url, json=payload)
        if not resp.ok or int(resp.json()['code']) != 0:
            print(f'{resp.status_code}: {resp.reason}')
            print(f'{resp.text}')
            raise Exception('pe/pb抓取失败')
        data_json = resp.json()

        df = pd.DataFrame()
        temp_df = pd.DataFrame(
            data_json["data"]["tubiao"]["series"][0]["data"],
            columns=["timestamp", "value"],
        )
        df["date"] = (
            pd.to_datetime(temp_df["timestamp"], unit="ms", utc=True)
            .dt.tz_convert("Asia/Shanghai")
            .dt.date.astype(str)
        )
        df["code"] = self._format_code(code, 'standard')
        df[category] = pd.to_numeric([item[1] for item in data_json["data"]["tubiao"]["series"][1]["data"]])
        return df

    def get_index_pe_pb(self, code, sleep=1):
        """ 从网页抓取指数的pe和pb
        """
        pe_df = self.get_index_guzhi(code, 'pe')
        time.sleep(sleep)
        pb_df = self.get_index_guzhi(code, 'pb')
        return pe_df.merge(pb_df, on=['date', 'code'], how='outer')

    def _count_table(self, table_name):
        result = self._read_sql_query(f'select count(1) as cnt from {table_name}')
        return int(result['cnt'].iloc[0])

    def _exists_table(self, table_name):
        tables = self._read_sql_query("SELECT name FROM sqlite_master WHERE type='table'")['name'].tolist()
        return (table_name in tables)

    def init_stock(self, code, start_date='2004-12-31', end_date=None, force_init=False, verbose=True):
        end_date = end_date or get_date(0)
        table_name = self._get_table_name_by_code(code)
        if not force_init and self._exists_table(table_name):
            print(f'[WARN] {table_name} 表已存在，跳过初始化。若需强制初始化，可设置force_init=True')
            return

        df = self.get_stock_history(code, start_date, end_date)
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

        st, ed = df['date'].min(), df['date'].max()
        if verbose:
            print(f'[DEBUG] {table_name} 初始化{len(df)}条数据({st}~{ed})')

    def update_stock(self, code, verbose=True):
        table_name = self._get_table_name_by_code(code)
        if verbose:
            before_cnt = self._count_table(table_name)

        prev_max_date = str(self._read_sql_query(f'select max(date) as max_date from {table_name}')['max_date'].iloc[0])
        start_date = get_date(1, prev_max_date)
        if verbose:
            print(f'[DEBUG] {table_name} 上次数据更新到{prev_max_date}')
        df = self.get_stock_history(code, start_date=start_date)

        if len(df) > 0:
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
            if verbose:
                after_cnt = self._count_table(table_name)
                print(f'[DEBUG] {table_name} 更新前记录数: {before_cnt}条')
                print(f'[DEBUG] {table_name} 更新后记录数: {after_cnt}条(~{df["date"].max()})')
                assert after_cnt-before_cnt == len(df), f'{table_name}更新前后记录数不等于len(df)，请检查'
        else:
            if verbose:
                print(f'[DEBUG] {table_name} 暂无新增数据')            

    def load_stock(self, code, verbose=True):
        table_name = self._get_table_name_by_code(code)
        if self.db_path is not None:
            if verbose: print(f'[INFO] 从db加载数据{table_name}')
            df = self._read_sql_table(table_name)
        else:
            if verbose: print(f'[INFO] 从网络加载数据{table_name}')
            df = self.get_stock_history()
        return df.sort_values('date')

    def init_or_update_index_pe_pb(self, code, verbose=True):
        stardand_code = self._format_code(code, format='standard')
        table_name = self._get_table_name_by_code(code, prefix='pepb')

        new_df = self.get_index_pe_pb(code)
        if self._exists_table(table_name):
            exists_df = self._read_sql_query(f'SELECT * FROM {table_name}')
            all_df = pd.concat([exists_df, new_df], axis=0, ignore_index=True, sort=True).drop_duplicates(subset=['date'], keep='last')
        else:
            exists_df = pd.DataFrame()
            all_df = new_df
        if len(all_df) > 0:
            all_df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            if verbose:
                before_cnt, after_cnt = len(exists_df), len(all_df)
                before_st, before_ed = (exists_df["date"].min(), exists_df["date"].max()) if len(exists_df) else ("", "")
                after_st, after_ed = (all_df["date"].min(), all_df["date"].max()) if len(all_df) else ("", "")
                print(f'[DEBUG]: {table_name} pepb更新前: {before_cnt}条({before_st}~{before_ed})')
                print(f'[DEBUG]: {table_name} pepb更新后: {after_cnt}条({after_st}~{after_ed})')
        else:
            if verbose: print(f'[DEBUG] {table_name} pepb无数据')

    def load_index_pepb(self, code, verbose=True):
        table_name = self._get_table_name_by_code(code, prefix='pepb')
        if self.db_path is not None:
            if verbose: print(f'[INFO] 从db加载数据{table_name}')
            df = self._read_sql_table(table_name)
        else:
            if verbose: print(f'[INFO] 从网络加载数据{table_name}')
            df = self.get_index_pe_pb()
        return df.sort_values('date')
