import pandas as pd
from collections import Counter
import spacy
import time

nlp = spacy.load('en_core_web_lg')

### GLOBAL VARIABLES ###
START_TIME = time.time()
#Text column label in csv
TEXT_COL = 'text'
#Set data file path
TEXT_FILE = pd.read_csv('reddit_data4.csv')
#Set ngram number
LARGEST_N_TO_CHECK = 7
#initialize Counters
NGRAM_COUNTERS = {n: Counter() for n in range(1,LARGEST_N_TO_CHECK+1)}
#looking forward only or forwards and backwards?
DIRECTION = 'Forward Only' #change to 'Both if you want both forwards and backwards'

#Function to clean and tokenize text
def clean_and_tokenize_text(text, lemmatize = True, remove_stopwords = False):
  ''' cleans text by removing stopwords, punctuation, and extra spaces.
        inputs:
            text = your text to process (this can be run on multiple unit sizes, from cells in read in excel files to entire .txt files)
            lemmatize = whether or not to lemmatize (convert to lemma forms) the text. Default is true, set to false to keep lexeme form '''

  #convert text to spacy object form
  doc = nlp(text)

  #Remove punctuation, stopwords, and blank tokens. Lemmatizes if function set to True
  if lemmatize == True and remove_stopwords == True:
      clean_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
  elif lemmatize == True and remove_stopwords == False:
      clean_tokens = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
  elif lemmatize == False and remove_stopwords == True:
      clean_tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
  else:
      clean_tokens = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]

  return clean_tokens

def get_n_grams(tokens, n_gram_level, direction):

    #make list of ngrams looking in forward direction
    n_grams_list = list(zip(*[tokens[i:] for i in range(n_gram_level)]))

    #if you want backwards and forwards, combine those lists
    if direction != 'Forward Only':
        #print()
        n_grams_list = list(n_grams_list) + list(zip(*[tokens[::-1][i:] for i in range(n_gram_level)]))

    return n_grams_list

def count_ngrams(cleaned_tokens, number_of_ngrams, direction = DIRECTION):
    for i in range(1, number_of_ngrams + 1):

        #update the ngram counter
        NGRAM_COUNTERS[i].update(get_n_grams(cleaned_tokens, i, direction = direction))

#write the output of the counters to the file
def save_counters_to_csv(NGRAM_COUNTERS):

    for n, counter in NGRAM_COUNTERS.items():
        ngrams_and_counts = pd.DataFrame([(' '.join(ngram), count) for ngram, count in counter.items()], columns=['ngram', 'count'])
        ngrams_and_counts.head()
        ngrams_and_counts.sort_values(by='count', ascending=False, inplace=True)

        #write csvs
        ngrams_and_counts.to_csv(f'ngram_files/{n}-gram_counts.csv', index=False)


def main():

    #go down excel file text columns
    for text in TEXT_FILE[TEXT_COL].dropna():

        #process the text
        clean_tokens = clean_and_tokenize_text(text, lemmatize = False, remove_stopwords = False)

        #generate the ngrams
        count_ngrams(clean_tokens, number_of_ngrams = LARGEST_N_TO_CHECK, direction = DIRECTION)

    #write csvs
    save_counters_to_csv(NGRAM_COUNTERS)

main()

print("Done :)")
print("run time:", (time.time()-START_TIME)/60.0, "minutes")
