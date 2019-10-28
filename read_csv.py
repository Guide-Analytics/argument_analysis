##

# Argument Mining with Tone Analysis 6.0
# 'read_csv'
# Gide Inc 2019

##

import re
import time
from pyspark.sql.functions import regexp_replace, udf
from pyspark.sql.types import StringType
from spark_init import spark


# load_dataset_and_set_views:
# Purpose: reading the data from csv through SPARK
# Input; [String] path_author
# Output: [Spark DataFrame] auth_data
def load_dataset_and_set_views(path_author = "REVIEWS_AUTHORS.csv"):

    '''
    :param pathA: default csv file: REVIEWS_AUTHORS.csv
    :return: spark, reviews DataFrame, authors DataFrame
    '''

    # Try not to touch these commands.
    # These are normal Spark functions and it is the quickest way to handle Spark data
    while True:
        try:
            auth_data_raw = spark.read.csv(path_author, mode="PERMISSIVE", header='true', sep=',', inferSchema=True,
                                           multiLine=True, quote='"', escape='"')
            auth_data_raw = auth_data_raw.withColumn('Review Text', regexp_replace('Review Text', '"', ''))
            auth_data_raw = auth_data_raw.withColumn('Business Name', regexp_replace('Business Name', '"', ''))
            auth_data_raw = auth_data_raw.withColumn('Business Adddress', regexp_replace('Business Adddress', '"', ''))

            break
        except FileExistsError or FileNotFoundError:
            time.sleep(10)

    # Setting up Database/DataFrame header names

    auth_data = auth_data_raw.toDF("GOOGLE_REVIEWS ID", "Note", "Level", "Reviews Count", "Ratings Count", "Source URL",
                                   "Source Business Name", "Business Name", "Business Address", "Review Text",
                                   "Reviewer Name", "Review Rating", "Review Date", "Reviewer URL",
                                   "Scraped Time", "Like", "Review Photo")

    auth_data = auth_data.withColumn('Like', regexp_replace('Like', 'Like', ''))

    udf_text_cleaner = udf(text_cleaner, StringType())

    auth_data = auth_data.withColumn('Review Text', udf_text_cleaner('Review Text'))
    # auth_data = auth_data.withColumn('Like', regexp_replace('Like', 'null', ''))

    # Creating Temp views (for extracting and testing purposes)
    auth_data.createOrReplaceTempView("auth_data")

    return auth_data


# text_cleaner:
# Purpose: text cleaning to remove spaces, links, whitespaces, etc.
# Input; [String] text
# Output: [String] text
def text_cleaner(text):

    text = str(text)
    rules = [
       {r'>\s+': u'>'}, # removes spaces after a tag opens or closes
       {r'\s+': u' '}, # replace cons. spaces
       {r'\s*<br\s*/?>\s*': u'\n'}, # new lines after a <br>
       {r'</(div)\s*>\s*': u'\n'},
       {r'</(p|h\d)\s*>\s*': u'\n\n'}, # newline after </p> and </div> and <h1/>
       {r'<head>.*<\s*(/head|body)[^>]*>': u''}, # remove <head> to </head>
       {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'}, # show links instead of texts
       {r'[ \t]*<[^<]*?/?>': u''}, # remove reamining tags
       {r'^\s+': u''} # remove spaces beginning]}
    ]
    for rule in rules:
        for (k, v) in rule.items():
            regex = re.compile(k)
            text = regex.sub(v, text)
    text = text.rstrip()

    return text.lower()
