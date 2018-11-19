# coding: utf-8

from gensim import corpora, models, similarities
from word_counter import main
import gensim, collections, sys

def document_wakati(text):
    """
    - For a doc.
    - text: Separated by every lines for a doc (Input is one file).
    """

    with open(text, "r") as f:
        sentences = f.read()
        splitted_document_WAKATIlist, _ = main(sentences)
        return splitted_document_WAKATIlist

def documents_wakati(text):
    """
    - For docs.
    - text: Separated by every doc for docs (Input is one file).
    """

    with open(text, "r") as f:
        sentences = f.read()
        splitted_document_WAKATIlist, _ = main(sentences, is_doc_or_docs = False)
        return splitted_document_WAKATIlist

def lda(input_file = sys.argv[1]):
    # List for remove stop words.
    slothlib_stopwords = []
    with open("./slothlib.txt", "r") as f:
        slothlib_stopwords = [line.decode("utf-8").strip() for line in f]

    separated_document_list = documents_wakati(input_file)
    separated_document_list_temp = []

    # Remove stop words.
    for l in separated_document_list:
        b_pivot = 0
        for i in xrange(len(l)):
            if l[b_pivot] in slothlib_stopwords:
                l.pop(b_pivot)
                continue
            b_pivot += 1
        separated_document_list_temp.append(l)

    separated_document_list = separated_document_list_temp
    separated_document_list_temp = None

    # Generate a corpora.
    dictionary = corpora.Dictionary(separated_document_list)
    dictionary.filter_extremes(no_below=5, no_above=0.5)  # (Provisional)
    dictionary.save_as_text('dict.txt')

    # Generate a Dictionary.
    corpus = [dictionary.doc2bow(text) for text in separated_document_list]
    corpora.MmCorpus.serialize('cop.mm', corpus)
    dictionary = gensim.corpora.Dictionary.load_from_text('dict.txt')
    corpus = corpora.MmCorpus('cop.mm')

    # Create a model by Hierarchical Dirichlet Process.
    model = gensim.models.hdpmodel.HdpModel(corpus=corpus, id2word=dictionary)

    # Create a model by Latent Dirichlet Allocation.
    #topic_N = 20
    #model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=topic_N, id2word=dictionary)

    # Topics(Max. 150), and words that construct a topic.
    print(model.print_topics(num_topics=-1, num_words=10))

    # Count topics that estimated above script.
    estimated_topicnum_list = []
    topics = [model[c] for c in corpus]

    for i in xrange(len(topics)):
        if len(topics[i]) == 0:
            continue
        else:
            print(i, u"番目の文書のトピックは, ", topics[i])  # [(topic_index, topic_weight), ...]
            for topic_and_prob_tuple in topics[i]:
                estimated_topicnum_list.append(topic_and_prob_tuple[0])

    estimated_topicnum_dict = collections.Counter(estimated_topicnum_list)
    print(u"推定されたトピックの数: ", len(estimated_topicnum_dict))

    # Calculate a occuerence probabilty of each words in topics that most represent a input document. 
    input_text_topics = topics[len(separated_document_list) -1]  # [(topic's index, occProb), ...]
    word_prob_in_topic = model.print_topics(num_topics=-1, num_words=len(dictionary))  # [(topic's index, u"'occProb*word', ..."), ...]
    word_prob_in_topic_dic = {}  # {"word": "prob", ...}
    
    for input_text_topic in input_text_topics:
        word_prob_in_topic_list = word_prob_in_topic[input_text_topic[0]][1].split(",")
        for factors in word_prob_in_topic_list:
            factor = factors.split("*")

            if len(factor) == 2:
                if factor[1] in word_prob_in_topic_dic:
                    word_prob_in_topic_dic[factor[1]] = str(float(word_prob_in_topic_dic[factor[1]]) + float(factor[0]))
                else:
                    word_prob_in_topic_dic[factor[1]] = factor[0]

    return word_prob_in_topic_dic


if __name__ == "__main__":
    print(lda(sys.argv[1]))
