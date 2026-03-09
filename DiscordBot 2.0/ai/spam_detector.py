from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

messages = [
"buy cheap nitro",
"free discord nitro",
"hello how are you",
"join my server",
"spam link here"
]

labels = [1,1,0,1,1]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(messages)

model = MultinomialNB()

model.fit(X,labels)

def is_spam(text):

    vec = vectorizer.transform([text])

    result = model.predict(vec)

    return result[0] == 1