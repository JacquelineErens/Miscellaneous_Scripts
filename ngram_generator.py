import pandas as pd
from collections import Counter
import spacy
import os

nlp = spacy.load('en_core_web_lg')

### GLOBAL VARIABLES ###

#Set data file path
text_file = pd.read_csv('reddit data short.csv')
#Set ngram number
largest_n_to_check = 7
#initialize Counters
ngram_counters = {n: Counter() for n in range(1,largest_n_to_check+1)}

#Function to clean and tokenize text
def clean_and_tokenize_text(text, lemmatize = True):
  ''' cleans text by removing stopwords, punctuation, and extra spaces.
        inputs:
            text = your text to process (this can be run on multiple unit sizes, from cells in read in excel files to entire .txt files)
            lemmatize = whether or not to lemmatize (convert to lemma forms) the text. Default is true, set to false to keep lexeme form '''

  #convert text to spacy object form
  doc = nlp(text)

  #Remove punctuation, stopwords, and blank tokens. Lemmatizes if function set to True
  if lemmatize == True:
      clean_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
  else:
      clean_tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]

  return clean_tokens

def get_n_grams(tokens, n_gram_level, forward_only = True):

    #make list of ngrams looking in forward direction
    n_grams_list = list(zip(*[tokens[i:] for i in range(1,n_gram_level+1)]))

    #if you want backwards and forwards, combine those lists
    if forward_only == False:
        #print()
        n_grams_list = list(n_grams_list) + list(zip(*[tokens[::-1][i:] for i in range(1,n_gram_level+1)]))

    return n_grams_list

def count_ngrams(cleaned_tokens, number_of_ngrams, forward_only):
    for i in range(1, number_of_ngrams + 1):

        #update the ngram counter
        ngram_counters[i-1].update(get_n_grams(cleaned_tokens, i, forward_only = forward_only))

#write the output of the counters to the file
def save_counters_to_csv(ngram_counters):

    for n, counter in ngram_counters.items():
        ngrams_and_counts = pd.DataFrame(counter.items(), columns=['ngram', 'count'])
        ngrams_and_counts.head()
        ngrams_and_counts.sort_values(by='count', ascending=False, inplace=True)
        #write csvs
        ngrams_and_counts.to_csv(f'ngram_files/{n}-gram_counts.csv', index=False)


def main():

    #go down excel file text columns
    for text in df['text'].dropna():

        #process the text
        clean_and_tokenize_text(text, lemmatize = True)

        #generate the ngrams
        count_ngrams(tokens, n_gram_level, forward_only = True)

        #write csvs
        save_counters_to_csv(ngram_counters)

main()

print("Done :)")
