##

# Argument Mining with Tone Analysis 6.0
# 'arg_extract'
# Gide Inc 2019

# SPACY_ARGUING_LEXICON
# From the works of:
# Swapna Somasundaran, Josef Ruppenhofer and Janyce Wiebe (2007) Detecting Arguing and Sentiment in Meetings,
# SIGdial Workshop on Discourse and Dialogue, Antwerp, Belgium, September 2007 (SIGdial Workshop 2007)

##


from __future__ import generator_stop
import spacy
from spacy_arguing_lexicon import ArguingLexiconParser
from ibm_watson import ToneAnalyzerV3
from ibm_watson import ApiException
import json


nlp = spacy.load('en')

nlp.add_pipe(ArguingLexiconParser(lang=nlp.lang))


# argument_analyzer:
# Purpose: Extract argument labels, and sentences containing the argument
# Input: [String] text
# Output: [List] arg_result_list
def argument_analyzer(text):

    arg_result_list = []
    doc_analysis = nlp(text)

    for ext in doc_analysis._.arguments.get_argument_spans():
        arg_result = 'Argument: ' + ext.text + ', Label: ' + ext.label_ + ', Sentence: ' + ext.sent.text.strip()
        arg_result_list.append(arg_result)

    return arg_result_list


# argument_sentence_analyzer (Dumb version):
# Purpose: Extract sentences containing the argument
# Input: [String] text
# Output: [String] arg_result
def argument_sentence_analyzer(text):

    arg_result = ''
    doc_analysis = nlp(text)
    for ext in doc_analysis._.arguments.get_argument_spans():
        arg_result = str(ext.sent.text.strip())

    return arg_result


# tone_analyzer:
# Purpose: Extract emotional score from texts using IBM Tone Analysis
# Input: [String] text
# Output: [String] doc_result_list (originally a List)
def tone_analyzer(text):

    doc_result_list = []
    sent_result_list = ''
    tone_analysis = {}

    if text == '' or text == None or text == ' ':
        return ''

    try:
        tone_init = ToneAnalyzerV3(
            version = '2019-07-29',
            iam_apikey= 'Gwmh6uTwxSrtgPvWgIiCY1nN5zCjRulxbnS1VU1l-Xti',
            url = 'https://gateway-wdc.watsonplatform.net/tone-analyzer/api'
        )

        tone_analysis = tone_init.tone(
            {'text': text},
            content_type='application/json'
        ).get_result()

    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)

    json_result = json.dumps(tone_analysis, indent=2)
    json_result = json.loads(json_result)

    doc_tone_result = json_result.get('document_tone').get('tones')    #['document_tone']
    sent_tone_result = json_result.get('sentences_tone')

    if sent_tone_result != None:
        for info in sent_tone_result:
            tones = info['tones']
            text = info['text']
            tone_extract_list = tone_extraction(tones=tones)
            sent_result_list = str(text) + ': ' + str(tone_extract_list)
    else:
        pass

    if doc_tone_result != []:
        for info in doc_tone_result:
            tone_name = info['tone_name']
            score = info['score']
            doc_result_list.append(str(tone_name) + ': ' + str(score))
    else:
        pass

    # if trig == 'd':
    return str(doc_result_list)


# tone_extraction:
# Purpose: get score of the tone and tone name from review
# Input: [List] tones (list of tones categories)
# Output: [List] tone_extract_list (tone name and score)
def tone_extraction(tones):

    tone_extract_list = []
    if tones != []:
        for info in tones:
            tone_name = info['tone_name']
            score = info['score']
            tone_extract_list.append([tone_name, score])

    return tone_extract_list
