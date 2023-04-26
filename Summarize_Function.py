#Summarizing article content


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest



def summarize(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    
    # Remove stop words from the words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Calculate the frequency distribution of the words
    word_freq = {}
    for word in words:
        if word not in word_freq:
            word_freq[word] = 0
        word_freq[word] += 1
    
    # Determine the most frequent words and use them to create a summary
    num_sentences = int(len(sentences) * 0.2)
    if num_sentences == 0:
        num_sentences = 1
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_words = word_tokenize(sentence.lower())
        sentence_score = 0
        for word in sentence_words:
            if word in word_freq:
                sentence_score += word_freq[word]
        sentence_scores[i] = sentence_score
    top_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join([sentences[i] for i in sorted(top_sentences)])
    
    # Format the summary into appropriate paragraphs
    summary_sentences = sent_tokenize(summary)
    summary_paragraphs = []
    paragraph = ''
    for sentence in summary_sentences:
        if len(paragraph) + len(sentence) > 120:
            summary_paragraphs.append(paragraph)
            paragraph = ''
        paragraph += ' ' + sentence
    if paragraph:
        summary_paragraphs.append(paragraph)
    formatted_summary = '\n\n'.join(summary_paragraphs)
    
    return formatted_summary
