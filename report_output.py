##

# Argument Mining with Tone Analysis 6.0
# 'report_output'
# Gide Inc 2019

##

from arg_extract import argument_analyzer, argument_sentence_analyzer, tone_analyzer
from read_csv import load_dataset_and_set_views
from pyspark.sql.functions import udf, regexp_replace, explode
from pyspark.sql.types import ArrayType, StringType, StructField, StructType, DataType


# report_output:
# Purpose: Load author data and analyze argument and tone for each review
# Input: None
# Output: None (CSV file)
def report_output():

    auth_data = load_dataset_and_set_views()

    udf_arg_extract = udf(argument_analyzer, StringType())
    udf_sentence_ext = udf(argument_sentence_analyzer, StringType())

    udf_tone_extract = udf(tone_analyzer, StringType())

    # allsubsets = lambda l: [[z for z in y] for y in chain(*[combinations(l, n) for n in range(1, len(l) + 1)])]

    new_auth_data = auth_data.withColumn('arg_exts', udf_arg_extract('Review Text'))
    new_auth_data = auth_data.withColumn('arg_sents', udf_sentence_ext('Review Text'))
    new_auth_data = new_auth_data.withColumn('review_emotion', udf_tone_extract('Review Text'))
    new_auth_data = new_auth_data.withColumn('arg_sents_emotion', udf_tone_extract('arg_sents'))
    new_auth_data.write.format('csv').mode('overwrite').option("header", "true").save("author_info")


report_output()



