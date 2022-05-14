import nltk
import string
import sklearn.metrics.pairwise
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from libreria import clip_parser
from gensim.models.doc2vec import Doc2Vec
from gensim.models import LdaModel
from ldamodel import corpus_extractor


# Quering Titles
def title_recognition(query = 'Zen brain beginner', data = clip_parser()): # I am not sure this makes sense
    my_clippings = data
    tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
    tfs = tfidf.fit_transform(my_clippings['titolo']).todense()

    query=query.lower()
    query = query.translate(string.punctuation)
    query_tfidf = tfidf.transform([query])

    # getting the distances
    eu_distances = sklearn.metrics.pairwise.euclidean_distances(tfs,query_tfidf)
    eu_distances = [row[0] for row in eu_distances]

    # filtering the table by the distances
    list = []
    eu_distances_sorted = np.array(list)

    k = np.argsort(eu_distances)[0]
    for i in np.argsort(eu_distances):
        if eu_distances[i] != eu_distances[k]:
            break
        eu_distances_sorted = np.append (eu_distances_sorted, i)
        k = i
    
    return(my_clippings.iloc[eu_distances_sorted])


# Quering Quotes
def quote_recognition(query = 'a man is in peace when', percentile = 10, data = clip_parser()): # I am not sure this makes sense
    my_clippings = data
    tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
    tfs = tfidf.fit_transform(my_clippings['citazione']).todense()

    ### adjust by the length of the sentence
    for index in range(len(my_clippings['citazione'])):
        tfs[index] = tfs[index]/len(my_clippings['citazione'][index].split(' '))

    query=query.lower()
    query = query.translate(string.punctuation)
    query_tfidf = tfidf.transform([query])

    # getting the distances
    eu_distances = sklearn.metrics.pairwise.euclidean_distances(tfs,query_tfidf)
    eu_distances = [row[0] for row in eu_distances]

    # filtering the table by the distances
    list = []
    eu_distances_sorted = np.array(list)

    k = np.argsort(eu_distances)[0]
    for i in np.argsort(eu_distances):
        if eu_distances[i] < np.percentile(eu_distances, [percentile]):
            eu_distances_sorted = np.append (eu_distances_sorted, i)

    my_clippings.iloc[eu_distances_sorted]
    # the best would be: get the top 100 quotes, and arrange them by topic
    
    return(my_clippings.iloc[eu_distances_sorted])

### Doc2vec to get quote similarity
def quote_similarity(quote = 'a man is morally free when', full_name = 'Costantino_Terranova'):
    model= Doc2Vec.load(f"tempDir/models/{full_name}_d2v.model")
    my_clippings = clip_parser()
    tokens = quote.split()

    new_vector = model.infer_vector(tokens)
    sims = model.dv.most_similar([new_vector])

    my_list = []
    for index in sims:
        my_list.append(int(index[0]))
    return(my_clippings.iloc[my_list])

### Get similar Authors based on Topic
def topic_author_match(full_name = 'Costantino_Terranova', quote = 'Freedom is never free'):
    corpus = corpus_extractor()
    lda= LdaModel.load(f"tempDir/models/{full_name}_lda.model")
    my_clippings = clip_parser()
    for index in range(len(my_clippings)):
        my_clippings['citazione'][index] = my_clippings['citazione'][index] + '. '
        my_clippings['titolo'][index] = my_clippings['titolo'][index] + '---'
    my_clippings = my_clippings.groupby(['autore']).sum()
    for index in range(len(my_clippings)):
        my_clippings['titolo'][index] = my_clippings['titolo'][index].split('---')[0]

    my_clippings = my_clippings.reset_index()
    index = my_clippings.index[my_clippings['citazione'].str.contains(quote)][0]
    #return(lda.print_topics(num_topics=10, num_words=20))
    topic = lda.get_document_topics(corpus)[index][0][0]
    my_list = []
    for tuple in lda.get_document_topics(corpus):
        my_list.append(tuple)
    for element in range(len(my_list)):
        if len(my_list[element]) == 2:
            if my_list[element][0][1] > my_list[element][1][1]:
                my_list[element] = my_list[element][0]
            else: 
                my_list[element] = my_list[element][1]
        else:
            my_list[element] = my_list[element][0]
    topic_candidates = list()
    index_author_candidates = list()
    for element in range(len(my_list)):
        if my_list[element][0] == topic:
            topic_candidates.append(my_list[element])
            index_author_candidates.append(element)

    zipped_lists = zip(topic_candidates, index_author_candidates)
    sorted_zipped_lists = sorted(zipped_lists, reverse = True)

    relevant_authors_index = [element for _, element in sorted_zipped_lists]

    return(my_clippings['autore'][relevant_authors_index].reset_index()['autore'])

