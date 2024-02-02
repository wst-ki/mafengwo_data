# builder:wstki
# 开发时间12:14,2024/2/2
# name:test6_pgsql
# 创建和连接数据库，如果创建了就不会重新创建了，用于保存各类的数据
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# 构建数据库连接字符串


def check_and_create_database(db_name = "Mafengwo"):
    """
    连接到Mafengwo数据库
    如果没有数据库就自动创建
    """
    try:
        # 连接默认的"postgres"数据库
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgre",
        )
        print("成功连接到默认数据库")

        # 创建数据库游标
        cursor = connection.cursor()

        # 检查数据库是否存在
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            # 如果数据库不存在，则创建
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()

            # 创建数据库
            cursor.execute("CREATE DATABASE {}".format(db_name))

            print(f"成功创建数据库: {db_name}")
        else:
            print(f"数据库已经存在: {db_name}")

        # 提交更改
        connection.commit()

    except Exception as e:
        print(f"连接或操作数据库时发生错误: {e}")

    finally:
        # 关闭数据库连接
        if connection:
            connection.close()
            print("数据库连接已关闭")



# 检查并创建数据库
check_and_create_database()

# 建立一个表格，用于装载所有城市的POI数据