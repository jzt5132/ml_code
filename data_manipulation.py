import pandas as pd
import numpy as np
from utils import log_table, get_logger_handle

logger = get_logger_handle(__name__)

def run_wrapper_func() -> None:
    # read data
    logger.info(
        "\n"
        "+-------------------+\n"
        "| Data Manipulation |\n"
        "+-------------------+"
    )
    logger.info("\n...read order and user data...")
    order_data = pd.read_csv('data_manipulation/order.csv')
    user_data = pd.read_csv('data_manipulation/user.csv')
    logger.info("\n...check original order_data...")
    log_table(order_data, logger)
    logger.info("\n...print original user_data...")
    log_table(user_data, logger)
    # check partial data
    logger.info("\n...check partial data...")
    log_table(order_data.head(n=10), logger)
    # check orderid and amount columns
    logger.info(
        "\n"
        "+------------------+\n"
        "| Column Selection |\n"
        "+------------------+"
    )
    logger.info("\n...check orderid and amount columns...")
    log_table(order_data.loc[:, ['orderid', 'amount']], logger)

    # get unique values
    logger.info(
        "\n"
        "+-----------------+\n"
        "| Unique Values   |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select distinct orderid\n"
        "from order_data"
    )
    logger.info(order_data["orderid"].unique())

    # count distinct
    logger.info(
        "\n"
        "+-----------------+\n"
        "| Count Distinct  |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select count(distinct orderid) \n"
        "from order_data\n"
    )
    logger.info(order_data["orderid"].nunique())

    # filter data
    logger.info(
        "\n"
        "+------------------+\n"
        "| Filter Operation |\n"
        "+------------------+"
    )
    logger.info(
        "---SQL---\n"
        "select * \n"
        "from order_data\n"
        "where uid = 10003"
    )
    log_table(order_data[order_data["uid"] == 10003], logger)

    logger.info(
        "---SQL---\n"
        "select * \n"
        "from order_data\n"
        "where uid = 10003 and amount > 50"
    )
    log_table(order_data[(order_data["uid"] == 10003)
              & (order_data["amount"] > 50)], logger)

    logger.info(
        "---SQL---\n"
        "select * \n"
        "from order_data\n"
        "where uid = 10003 or amount > 50"
    )
    log_table(order_data[(order_data["uid"] == 10003)
              | (order_data["amount"] > 50)], logger)

    logger.info(
        "---SQL---\n"
        "select * \n"
        "from order_data\n"
        "where uid is null"
    )
    log_table(order_data[order_data["uid"].isna()], logger)

    logger.info(
        "---SQL---\n"
        "select * \n"
        "from order_data\n"
        "where uid is not null"
    )
    log_table(order_data[~(order_data["uid"].isna())], logger)

    # Group by
    logger.info(
        "\n"
        "+-----------------+\n"
        "| Group Operation |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select uid, count(distinct orderid) \n"
        "from order_data\n"
        "group by uid"
    )
    log_table(order_data.groupby("uid")[
              "orderid"].nunique().reset_index(), logger)
    logger.info(
        "---SQL---\n"
        "select uid, count(orderid) \n"
        "from order_data\n"
        "group by uid"
    )
    log_table(order_data.groupby("uid")[
              "orderid"].count().reset_index(), logger)

    logger.info(
        "---SQL---\n"
        "select uid, count(distinct orderid) as order_cnt, sum(amount) as sum_amount \n"
        "from order_data\n"
        "group by uid"
    )
    log_table(order_data.groupby("uid")["orderid", "amount"].agg(
        {"orderid": np.size, "amount": np.sum}).reset_index(), logger)

    # Join Operation
    logger.info(
        "\n"
        "+----------------+\n"
        "| Join Operation |\n"
        "+----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select * from user as u \n"
        "left join\n"
        "order as o\n"
        "on u.uid = o.uid"
    )
    log_table(pd.merge(user_data, order_data, how="left",
              left_on="uid", right_on="uid"), logger)

    # Union Operation
    logger.info(
        "\n"
        "+-----------------+\n"
        "| Union Operation |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select * from order1\n"
        "union\n"
        "select * from order2"
    )
    log_table(pd.concat([order_data, order_data]).drop_duplicates(), logger)

    # Union Operation
    logger.info(
        "\n"
        "+-----------------+\n"
        "| Order Operation |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select uid, count(distinct orderid)\n"
        "from order_data\n"
        "group by uid\n"
        "order by count(distinct orderid) desc"
    )
    log_table(order_data.groupby("uid")["orderid"].nunique(
    ).sort_values(ascending=False).reset_index(), logger)
    logger.info(
        "---SQL---\n"
        "select uid, count(distinct orderid), sum(amount)\n"
        "from order_data\n"
        "group by uid\n"
        "order by uid desc, sum(amount)"
    )
    res_df = order_data.groupby("uid")["orderid", "amount"].agg({"orderid": np.size, "amount": np.sum}).reset_index().rename(
        columns={"orderid": "order_cnt", "amount": "amount_sum"}).sort_values(by=["uid", "amount_sum"], ascending=[False, True])
    log_table(res_df, logger)

    # Case when operation
    logger.info(
        "\n"
        "+---------------------+\n"
        "| Case When Operation |\n"
        "+---------------------+"
    )
    logger.info(
        "---SQL---\n"
        "select uid, order_cnt,\n"
        "case when sum_amount < 300 then '[0, 300]'\n"
        "     when sum_amount >= 300 and sum_amount < 600 then '[300, 600]'\n"
        "     when sum_amount >= 600 and sum_amount < 900 then '[600, 900]'\n"
        "else 'other' end as amt_interval\n"
        "from\n"
        "(\n"
        "   select uid, count(distinct orderid) as order_cnt, sum(amount) as sum_amount\n"
        "   from order_data\n"
        "   group by uid\n"
        "   order by uid desc, sum(amount)\n"
        ") as a"
    )
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

    # Update Operation
    logger.info(
        "\n"
        "+------------------+\n"
        "| Update Operation |\n"
        "+------------------+"
    )
    logger.info(
        "---SQL---\n"
        "update user set age = 20\n"
        "where age < 20\n"
    )
    user_data.loc[user_data["age"] < 20, "age"] = 20
    log_table(user_data, logger)

    # Delete Operation
    logger.info(
        "\n"
        "+------------------+\n"
        "| Delete Operation |\n"
        "+------------------+"
    )
    log_table(user_data[user_data['age'] != 30], logger)
    user_data.drop(["uid"], axis=1, inplace=True)
    log_table(user_data, logger)

    # String Matching
    logger.info(
        "\n"
        "+-----------------+\n"
        "| String Matching |\n"
        "+-----------------+"
    )
    logger.info(
        "---SQL---\n"
        "select *\n"
        "from order_data\n"
        "where ts like '%8/1%'"
    )
    log_table(order_data[order_data['ts'].astype(
        str).str.contains("8/1")], logger)

    # Row_number Operation
    logger.info(
        "\n"
        "+----------------------+\n"
        "| Row_number Operation |\n"
        "+----------------------+"
    )
    logger.info(
        "---SQL---\n"
        "select *, row_number() over (partition by uid order by orderid desc) as rank\n"
        "from order_data"
    )
    order_data["rank"] = order_data.groupby("uid")["orderid"].rank(
        ascending=False, method="first").astype(int)
    order_data.sort_values(by=["uid", "rank"], ascending=[
                           True, True], inplace=True)
    log_table(order_data, logger)


if __name__ == "__main__":
    run_wrapper_func()
