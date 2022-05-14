from libreria import clip_parser
import nltk
import gensim
import string
import numpy as np
from gensim.test.utils import datapath

def tok_quot_ev_extractor():
    my_clippings = clip_parser()

    # grouping data by author
    for index in range(len(my_clippings)):
        my_clippings['citazione'][index] = my_clippings['citazione'][index] + '. '
        my_clippings['titolo'][index] = my_clippings['titolo'][index] + '---'
    my_clippings = my_clippings.groupby(['autore']).sum()
    # if you need to add title split at ---
    for index in range(len(my_clippings)):
        my_clippings['titolo'][index] = my_clippings['titolo'][index].split('---')[0]
    quotes = my_clippings['citazione']

    # all useful preloop stuff
    all_words = list()
    tokenized_quote = list()
    stopwords_list = nltk.corpus.stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)

    # loop to clean and tokenize
    for quote in quotes:
        sentences = nltk.sent_tokenize(quote)
        sentences = [sentence.replace("\n","") for sentence in sentences ]
        tokenized_sentence = list()
        for sentence in sentences:
                sentence = sentence.strip()
                sent_words = nltk.word_tokenize(sentence)
                sent_words = [word for word in sent_words if ((len(word) > 3)) and (word not in stopwords_list)] 

                for word in sent_words:
                    word = word.lower()
                    word=word.translate(translator) 
                    all_words.append(word)
                    tokenized_sentence.append(word) 

        tokenized_quote.append(tokenized_sentence)   
        
    # creating effective vocabulary   
    frequency_count = nltk.FreqDist(all_words)
    words =np.array([word for word in frequency_count.keys()])
    word_freq=np.array([word for word in frequency_count.values()])
    freq_sort = np.argsort(word_freq)[::-1]
    #word_freq_sort =word_freq[freq_sort]
    words_sorted = words[freq_sort]
    rank=1
    effective_vocab=list()
    for object in words_sorted:
        if (rank>=50):
            fc = frequency_count[object]
            if (fc>1):
                effective_vocab.append(object)
        rank+=1
    # filtering by effective vocabulary
    tok_quote_ev = list()
    for quote in tokenized_quote:
        quote_words_ev = [word for word in quote if word in effective_vocab]
        tok_quote_ev.append(quote_words_ev)
    dictionary = gensim.corpora.Dictionary(tok_quote_ev)
    corpus = [dictionary.doc2bow(doc) for doc in tok_quote_ev]
    return (tok_quote_ev)

def corpus_extractor():
    tok_quote_ev = tok_quot_ev_extractor()
    dictionary = gensim.corpora.Dictionary(tok_quote_ev)
    corpus = [dictionary.doc2bow(doc) for doc in tok_quote_ev]
    return(corpus)



def lda_model(full_name = 'Costa'):
    tok_quote_ev = tok_quot_ev_extractor()
    # BUILDING THE MODEL
    dictionary = gensim.corpora.Dictionary(tok_quote_ev)
    corpus = [dictionary.doc2bow(doc) for doc in tok_quote_ev]
    num_topics = 10
    passes = 50
    iterations = 400
    eval_every = None
    update_every = 0
    lda = gensim.models.LdaModel(
        corpus=corpus,
        id2word=dictionary, 
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every,
    update_every = update_every)

    # saving the model
    temp_file = datapath(f"/Users/Apple/Desktop/LIFE/Present/EDU/BOOKS/MODEL/tempDir/models/{full_name}_lda.model")
    lda.save(temp_file)

