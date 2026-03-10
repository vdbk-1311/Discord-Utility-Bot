from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

messages = [
"free nitro",
"claim free nitro",
"buy cheap crypto",
"join my server"
]

labels = [1,1,1,1]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)

model = MultinomialNB()
model.fit(X, labels)

def predict(text):

    X = vectorizer.transform([text])
    return model.predict(X)[0]