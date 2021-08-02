"""
This is the analytics module which generates the data for the api.
This module leverages pandas to do the data analysis
The module is broken into a series of steps that result in the expected data
getData->_formatData->_mergeAndFilterData->_getResult
"""

import sqlite3
import pandas as pd
import json
from collections import defaultdict

# defining dict keys, that appear in the API response
TOTAL_CUSTOMERS = "customers"
TOTAL_ITEMS = "items"
TOTAL_DISCOUNT = "total_discount_amount"
DISCOUNT_RATE_AVG = "discount_rate_avg"
ORDER_TOTAL_AVG = "order_total_avg"
COMMISSIONS = "commissions"
TOTAL_COMMISSIONS_GENERATED = "total"
COMMISSION_PER_ORDER_AVG = "order_average"
TOTAL_COMMISSIONS_PER_PROMOTION = "promotions"

class ShopDataAnalytics:
    def __init__(self, date):

        """
        Constructor to set the requested date and the database connection
        """
        self.requestedDate = date
        self.conn = sqlite3.connect('eshop_data.db')


    def getData(self):
        """
        Method to check if data exist for the requested date.
        If the data exist, it'll read the additional data and continue to call the other methods to
        finally get the result and return it
        """

        self.df_orders = pd.read_sql_query\
            ("SELECT * FROM orders where date(created_at) = '{}'".format(self.requestedDate), self.conn)
        if not self.df_orders.empty:
            orderids = self.df_orders['id'].unique().tolist()
            self.df_order_lines = pd.read_sql_query("SELECT * FROM order_lines where order_id in ({})".format
                                                    (', '.join('?'*len(orderids))), self.conn, params=orderids)
            self.df_commissions = pd.read_sql_query("SELECT * FROM commissions where date = '{}'".format
                                                    (self.requestedDate), self.conn)
            self.df_product_promotions = pd.read_sql_query("SELECT * FROM product_promotions where date = '{}'".format
                                                    (self.requestedDate), self.conn)
            self._formatData()
            self._mergeAndFilterData()
            return self._getResult()
        else:
            return {"Error": "No data found for the given date"}

    def _formatData(self):
        """
        Method for formatting the data and renaming the columns which will further be used to merge the dataframes
        """

        self.df_orders = self.df_orders.rename(columns={'id': 'order_id'})
        self.df_orders['created_at'] = self.df_orders['created_at'].str.split(" ").str[0]
        self.df_commissions = self.df_commissions.rename(columns={'date': 'created_at'})
        self.df_product_promotions = self.df_product_promotions.rename(columns={'date': 'created_at'})

    def _mergeAndFilterData(self):
        """
        Method for merging all the dataframes into a single dataframe with the relevant data.
        The merged dataframe is then used for the required analysis
        """

        self.df_order_data_for_requested_date = pd.merge(self.df_order_lines, self.df_orders, on='order_id', how='left')

        self.df_order_data_for_requested_date = pd.merge(self.df_order_data_for_requested_date, self.df_commissions,
                                                        on=['created_at', 'vendor_id'], how='left')
        self.df_order_data_for_requested_date = pd.merge(self.df_order_data_for_requested_date, self.df_product_promotions,
                                                        on=['created_at', 'product_id'], how='left')

        self.df_order_data_for_requested_date['promotion_id'] = self.df_order_data_for_requested_date['promotion_id'].astype('Int64')

        self.df_order_data_for_requested_date['commission_amount'] = self.df_order_data_for_requested_date['total_amount'] * \
                                                                self.df_order_data_for_requested_date['rate']

    def _getResult(self):
        """
        Method to calculate the required values, store them in a default dictionary and return it
        """

        data = defaultdict(defaultdict)

        data[TOTAL_CUSTOMERS] = int(self.df_order_data_for_requested_date['customer_id'].nunique())
        data[TOTAL_DISCOUNT] = self.df_order_data_for_requested_date['discounted_amount'].sum().round(2)
        data[TOTAL_ITEMS] = int(self.df_order_data_for_requested_date['quantity'].sum())
        data[ORDER_TOTAL_AVG] = self.df_order_data_for_requested_date['total_amount'].mean().round(2)
        data[DISCOUNT_RATE_AVG] = self.df_order_data_for_requested_date['discount_rate'].mean().round(2)

        data[COMMISSIONS][TOTAL_COMMISSIONS_PER_PROMOTION] = \
                                    self.df_order_data_for_requested_date.groupby('promotion_id')['commission_amount']\
                                    .sum().round(2).to_dict()
        data[COMMISSIONS][TOTAL_COMMISSIONS_GENERATED] = \
                                    self.df_order_data_for_requested_date['commission_amount'].sum().round(2)
        data[COMMISSIONS][COMMISSION_PER_ORDER_AVG] = \
                                    (data[COMMISSIONS][TOTAL_COMMISSIONS_GENERATED] /
                                     self.df_order_data_for_requested_date['order_id'].nunique()).round(2)

        return data