from pyspark.sql import SparkSession

def test_spark():
    spark = SparkSession.builder.appName("ehtn_test").getOrCreate()

    text_data = spark.read.text('hdfs://10.224.81.60:8020/data0/plants/yangju/2021/2021_01/2021_01_27/GTC1_11RCAOGC005_01.txt.gz')
    text_data.show()

    spark.stop()