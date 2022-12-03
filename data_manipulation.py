import pandas as pd
import numpy as np
from utils import log_table, get_logger_handle

logger = get_logger_handle(__name__)


if __name__  == "__main__":
    # read data
    order_data = pd.read_csv('data_manipulation/order.csv')
    user_data = pd.read_csv('data_manipulation/user.csv')
    log_table(order_data, logger)
    log_table(user_data, logger)
    # check partial data
    logger.info("\n...check partial data...")
    log_table(order_data.head(n=10), logger)
    # check orderid and amount columns
    logger.info("\n...check orderid and amount columns...")
    log_table(order_data.loc[:, ['orderid', 'amount']], logger)

    # get unique vales
    # SQL
    # ----------
    # select distinct orderid 
    # from order_data
    # ----------
    logger.info("\n...get unique vales...")
    logger.info(order_data["orderid"].unique())

    # count distinct 
    # SQL
    # ----------
    # select count(distinct orderid) 
    # from order_data
    # ----------
    logger.info("\n count distinct...")
    logger.info(order_data["orderid"].nunique())

    # filter data
    # SQL
    # ----------
    # select * from order_data 
    # where uid = 10003
    # ----
    logger.info("\n filter data...")
    log_table(order_data[order_data["uid"]==10003], logger)
    # select * from order_data 
    # where uid = 10003 and amount > 50
    log_table(order_data[(order_data["uid"]==10003) & (order_data["amount"] > 50)], logger)
    # select * from order_data 
    # where uid = 10003 or amount > 50
    log_table(order_data[(order_data["uid"]==10003) | (order_data["amount"] > 50)], logger)
    # select * from order_data 
    # where uid is null
    logger.info("\n select * from order_data where uid is null...")
    log_table(order_data[order_data["uid"].isna()], logger)
    # select * from order_data 
    # where uid is not null
    logger.info("\n select * from order_data where uid is not null...")
    log_table(order_data[~(order_data["uid"].isna())], logger)


    # Group by
    # select uid, count(distinct orderid) 
    # from order_data 
    # group by uid
    log_table(order_data.groupby("uid")["orderid"].nunique().reset_index(), logger)
    # select uid, count(orderid) 
    # from order_data 
    # group by uid
    log_table(order_data.groupby("uid")["orderid"].count().reset_index(), logger)

    # ----------
    # select uid, count(distinct orderid) as order_cnt, sum(amount) as sum_amount 
    # from order_data 
    # group by uid
    log_table(order_data.groupby("uid")["orderid","amount"].agg({"orderid": np.size,"amount": np.sum }).reset_index(), logger)

    # ----------
    # select * from user as u 
    # left join 
    # order as o 
    # on u.uid = o.uid
    # ----------
    log_table(pd.merge(user_data, order_data, how="left", left_on="uid", right_on="uid"), logger)

    # ----------
    # select * from order1 
    # union 
    # select * from order2
    # ----------
    log_table(pd.concat([order_data, order_data]).drop_duplicates(), logger)

    # ----------
    # select uid, count(distinct orderid)
    # from order_data
    # group by uid
    # order by count(distinct orderid) desc
    # ----------
    log_table(order_data.groupby("uid")["orderid"].nunique().sort_values(ascending=False).reset_index(), logger)



    # select uid, count(distinct orderid), sum(amount)
    # from order_data
    # group by uid
    # order by uid desc, sum(amount)
    res_df = order_data.groupby("uid")["orderid", "amount"].agg({"orderid":np.size, "amount":np.sum}).reset_index().rename(columns={"orderid": "order_cnt", "amount": "amount_sum"}).sort_values(by=["uid", "amount_sum"], ascending=[False, True])
    log_table(res_df, logger)

    # case when operation
    # ----------
    # select uid, order_cnt, 
    # case when sum_amount < 300 then '[0, 300]' 
    #      when sum_amount >= 300 and sum_amount < 600 then '[300, 600]' 
    #      when sum_amount >= 600 and sum_amount < 900 then '[600, 900]' 
    # else 'other' end as amt_interval
    # from
    # (
    #   select uid, count(distinct orderid) as order_cnt, sum(amount) as sum_amount
    #   from order_data
    #   group by uid
    #   order by uid desc, sum(amount)
    # ) as a
    # ----------
    def get_amt_interval(x):
        if x < 300:
            return '[0, 300]'
        elif x < 600:
            return '[300, 600]'
        elif x < 900:
            return '[600, 900]'
        else:
            return "others"
    res_df["amt_interval"] = res_df["amount_sum"].map(get_amt_interval)
    log_table(res_df, logger)


    # ----------
    # update user set age = 20 
    # where age < 20
    # ----------
    user_data.loc[user_data["age"] < 20, "age"] = 20    
    log_table(user_data, logger)

    # droo data
    # ----------
    log_table(user_data[user_data['age']!=30], logger)
    user_data.drop(["uid"], axis=1, inplace=True)
    log_table(user_data, logger)


    # ----------
    # select *
    # from order_data
    # where ts like "%8/1%"
    # ----------1
    log_table(order_data[order_data['ts'].astype(str).str.contains("8/1")], logger)

    # ----------
    # select *, row_number() over (partition by uid order by orderid desc) as rank
    # from order_data
    # ----------
    order_data["rank"] = order_data.groupby("uid")["orderid"].rank(ascending=False, method="first").astype(int)
    order_data.sort_values(by=["uid", "rank"], ascending=[True, True], inplace=True)
    log_table(order_data, logger)
