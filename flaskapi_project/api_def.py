"""
This Module is used to define all the functions that the API can do
for example: get_data_by_date
    This function calls the analytics modules and gets the shop data by date
"""

from analytics import ShopDataAnalytics


def get_data_by_date(date):
    helper = ShopDataAnalytics(date=date)
    result = helper.getData()
    return result
