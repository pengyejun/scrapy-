from snownlp import SnowNLP
from snownlp import sentiment


def caclu_sentiment(title,content):
    s = SnowNLP(content)
    sm = s.summary(limit=20)
    sm = '\t'.join(sm)
    r_smry = sentiment.classify(sm)
    r_title = sentiment.classify(title)
    return r_title*0.7+0.3*r_smry