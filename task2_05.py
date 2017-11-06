
# tweeter data mining task1 one solution  date: 25 july 2017
# writer jay harer

import json

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string


# collecting text darta  from tweet 
def collect_text_data():
  tweet_list=[]   # collect text from all tweets
  data={}         # dictionary representation of json string
  with open("python.json","r") as f:
    try:
      while(True):
       s = f.readline()
       data = json.loads(s)              # convert json string into dictionary
       tweet_list.append(data['text'])   # collect text from tweet
    except  :
      print("reading file error file reach at end")

  print("tweet_list", tweet_list)
  return tweet_list


# removing noise from text and lemitization( obtain root form of word)
def remove_noise(tweet_list):
 stop = set(stopwords.words('english'))
 print("stopwords=",stop)
 exclude = set(string.punctuation)
 print("punctuation=",exclude)
 lemma = WordNetLemmatizer()
 def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

 doc_clean = [clean(doc).split() for doc in tweet_list] # collect all cleaned tweet
 print("clean dock",doc_clean)
 return doc_clean



# standardization of text data

def standarzied_tweet(doc_clean):
 lookup_dict = {'rt':'Retweet', 'dm':'direct message', "awsm" : "awesome", "luv" :"love"}
 def _lookup_words(input_text):
    words = input_text.split()
    new_words = []
    for word in words:
        if word in lookup_dict:
            word = lookup_dict[word]
        new_words.append(word)
    new_text = " ".join(new_words)
    return new_text
 doc_std =[" ".join(doc) for doc in doc_clean]
 print("doc_std",doc_std)
 doc_standard =[ _lookup_words(doc) for doc in doc_std ]

 print("doc_standard",doc_standard)
 return doc_standard


# decide tweet is actionable or not

def decide_actionable_tweet(doc_standard):
 actionable_tweet = []
 from textblob.classifiers import NaiveBayesClassifier as NBC
 from textblob import TextBlob
 training_corpus = [ ('naredra modi is good politician','not_actionable'),
                    ('how congress become good oppositor','actionable'),
                    ('python is popular language','not_actionable'),
                    ('here is new version of python available see it','actionable'),
                    ('retweet why india is poor country','actionable'),
                    ('Pro cubbadi startion on 1 august 2017 ','not_actionable'),
                    ('book ticket for goa at reasonable cost','actinable')]

 test_corpus = [('here is new version of motorola see it','actionable'),
               ('hellow friends how are you','not_actionable')]

 model = NBC(training_corpus)

 print("model",model)
 try:
  for doc in doc_standard:         # for testing use other list instead of doc_standard
    result = model.classify(doc)

    if result is 'actionable':
        actionable_tweet.append(doc)
 except:
    print("error in classify")

 print("actionable_tweet", actionable_tweet)
 return actionable_tweet



# extract topic from actionable tweet
def extract_topic_from_tweet(actionable_tweet):
 actionable_list =[doc.split() for doc in actionable_tweet]
 import gensim
 from gensim import corpora
 topic_list = []

 # Creating the term dictionary of our corpus, where every unique term is assigned an index.
 dictionary = corpora.Dictionary(actionable_list)

 # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
 doc_term_matrix = [dictionary.doc2bow(doc) for doc in actionable_list]

 # Creating the object for LDA model using gensim library
 Lda = gensim.models.ldamodel.LdaModel

 # Running and Training LDA model on the document term matrix
 ldamodel = Lda(doc_term_matrix, num_topics=len(actionable_tweet), id2word = dictionary, passes=50)

 # Results
 raw_topic_list = ldamodel.print_topics(num_topics=len(actionable_tweet), num_words=1)

 """ extract topic from raw_topic string  """
 try:
  print("raw_topic list :",raw_topic_list)
  for topic in raw_topic_list:
    x = (topic[1])
    topic_list.append((x[7:-1]))   # extract only topic word

  print("topic list:",topic_list)
 except:
    print("error in topic extractiong")
 return topic_list



# actionable_tweet grouped by topic wise using dictionary functionality of python

def group_by_topic_wise(topic_list,actionable_tweet):
 dict={}
 set_topic_list = set(topic_list)  # collect unique topic list
 temp_list =[]

 try:
  i=0
  for topic in set_topic_list:
    while(i<len(topic_list)):
        if topic is topic_list[i]:
          temp_list.append(actionable_tweet[i]) # collect all tweet associate single topic
        i=i+1
    print(temp_list)
    dict[topic]= str(temp_list) # store tweet associate single topic as key(topic) value(associate tweet)
    temp_list.clear()
    i=0
  print(dict)

 except:
    print("error in groping tweets")
 return dict



# store  topic:tweets dictionery format into json file

def store_into_file(dict):
 try:
  with open("result.json","w") as f:
    json_str = json.dumps(dict)
    f.write(json_str)
 except:
    print("error in writing")



def __main__():

    tweet_list  = collect_text_data()
    doc_clean   = remove_noise(tweet_list)
    doc_standard = standarzied_tweet(doc_clean)
    actionable_tweet = decide_actionable_tweet(doc_standard)
    topic_list = extract_topic_from_tweet(actionable_tweet)
    dict = group_by_topic_wise(topic_list,actionable_tweet)
    store_into_file(dict)
    print("ok")


__main__()  # call main function


