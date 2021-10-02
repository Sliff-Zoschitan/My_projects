from nltk.corpus import PlaintextCorpusReader
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams
from nltk import pos_tag
from collections import OrderedDict
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from multiprocessing import Pool
import numpy as np
from scipy.sparse import csr_matrix
from collections import OrderedDict, defaultdict
import pickle
from joblib import dump, load
import json

def lower_pos_tag(words):
    lower_words = []
    for i in words:
        lower_words.append(i.lower())
    pos_words = pos_tag(lower_words, lang='rus')
    return pos_words

def clean(words):
    stemmer = SnowballStemmer("russian")
    cleaned_words = []
    for i in words:
        if i[1] in ['S', 'A', 'V', 'ADV']:
            cleaned_words.append(stemmer.stem(i[0]))
    return cleaned_words
"""
corpus_root = "C:/dtst"
def process(label):
    # Wordmatrix - список документов с лексемами
    # All words - список всех слов
    data = {'Word_matrix': [], 'All_words': []}
    # Промежуточный список для удаления гапаксов
    templist_allwords = []
    # Определение пути к папке с определенным лейблом
    corpus = PlaintextCorpusReader(corpus_root + '//' + label, '.*', encoding='utf-8')
    # Получение списка имен файлов в корпусе
    names = corpus.fileids()
    # Создание токенайзера
    tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
    for i in range(len(names)): # Обработка корпуса
        bag_words = tokenizer.tokenize(corpus.raw(names[i]))
        lower_words = lower_pos_tag(bag_words)
        cleaned_words = clean(lower_words)
        final_words = list(bigrams(cleaned_words)) + cleaned_words
        data['Word_matrix'].append(final_words)
        templist_allwords.extend(cleaned_words)
    # Определение гапаксов
    templistfreq = FreqDist(templist_allwords)
    hapaxes = templistfreq.hapaxes()
    # Фильтрация от гапаксов
    for word in templist_allwords:
        if word not in hapaxes:
            data['All_words'].append(word)
    return {label: data}

data = {}
label = 'neutral'
result = process(label)
data.update(result)
label = 'bad'
result = process(label)
data.update(result)
label = 'good'
result = process(label)
data.update(result)

# Создание помеченный данных со структурой:
# [([список слов отзыва], метка_класса)]
labels = ['neutral', 'bad', 'good']
labeled_data = []
for label in labels:
    for document in data[label]['Word_matrix']:
        labeled_data.append((document, label))

# Создание вокабуляра с уникальными лексемами
all_words = []
for label in labels:
    frequency = FreqDist(data[label]['All_words'])
    common_words = frequency.most_common(10000)
    words = [i[0] for i in common_words]
    all_words.extend(words)
# Извлечение уникальных лексем
unique_words = list(OrderedDict.fromkeys(all_words))

# Частотное кодирование для классификаторов nltk со структурой:
# # [({уникальный термин: кол-во вхождений в документ}, метка класса)]
prepared_data = []
for x in labeled_data:
    d = defaultdict(int)
    for word in unique_words:
        if word in x[0]:
            d[word] += 1
        if word not in x[0]:
            d[word] = 0
    prepared_data.append((d, x[1]))
# Частотное кодирование для классификаторов scikit-learn
# Разреженная матрица для признаков
matrix_vec = csr_matrix((len(labeled_data), len(unique_words)), dtype=np.int8).toarray()
# Массив для меток классов
target = np.zeros(len(labeled_data), 'str')
for index_doc, document in enumerate(labeled_data):
    for index_word, word in enumerate(unique_words):
        # Подсчет кол-ва вхождения слова в отзыв
        matrix_vec[index_doc, index_word] = document[0].count(word)
    target[index_doc] = document[1]
# Перемешиваем датасет
X, Y = shuffle(matrix_vec, target)

parameter = [1, 0, 0.1, 0.01, 0.001, 0.0001]
param_grid = {'alpha': parameter}
grid_search = GridSearchCV(MultinomialNB(), param_grid, cv=5)
grid_search.fit(X, Y)
Alpha, best_score = grid_search.best_params_, grid_search.best_score_

model = MultinomialNB(0.1)
model.fit(X, Y)



# X_control, Y_control обработаны так же, как и X и Y
# Однако для векторизации использовался вокабуляр обучающего датасета
#predicted = model.predict(X_control)
predicted = model.predict(X)
#stringgg = 'ну ты и тупой'
#perdict = model.predict(np.fromstring('НУ ты и тупой').reshape(1,4))
print(predicted)

# Точность на контрольном датасете
#score_test = accuracy_score(Y_control, predicted)
score_test = accuracy_score(Y, predicted)
print(score_test)
# Классификационный отчет
#report = classification_report(Y_control, predicted)
report = classification_report(Y, predicted)
print(report)
"""
#вывод наших данных

test_otzivi = [
    "Ага и разговаривать не хотим? Значит прокуратура",
    "Ну вот совсем другое дело",
    "Как только я заинтересовался распечаткой движения средств на счёте так и деньги появились да? Может в прокуратуру обратиться?",
    "Всё тот же, сколько раз вы меня успели обмануть пока я не заметил отсутствие средств на счёте хотя по истории они уже там должны быть",
    "Удачного дня До встречи",
    "Я всегда исправно плачу а тут вы мне хотите испортить кредитную историю ! Я тогда вынужден обратиться в суд!",
    "Ясно, увы вы опять меня разочаровали, это последнее наше сотрудничество",
    "Оценка консультации - 1 из 5",
    "говно"
]
model = load('filename.joblib')
with open('unique_words.txt', 'r') as fr:
    # читаем из файла
    unique_words = json.load(fr)
#print("Сколько сообщений хотите ввести? Введите число")
#print(">> ", end="")
#soobshenieCount = int(input())



#for item in range(soobshenieCount):
soobshenie = ""
print("Введите сообщение")
print(">> ", end="")
soobshenie = input()
test_dataset = []
tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
bag_words = tokenizer.tokenize(soobshenie)
lower_words = lower_pos_tag(bag_words)
cleaned_words = clean(lower_words)
final_words = list(bigrams(cleaned_words)) + cleaned_words
test_dataset.append(final_words)
test_matrix = csr_matrix((1, len(unique_words)), dtype=np.int8).toarray()
i = 0
for index_word, word in enumerate(unique_words):
    # Подсчет кол-ва вхождения слова в отзыв
    test_matrix[0, index_word] = final_words[0].count(word)

predicted = model.predict(test_matrix)
print(soobshenie)
if predicted[0] == 'b':
    print("Отрицательно")
if predicted[0] == 'g':
    print("Положительно")
if predicted[0] == 'n':
    print("Нейтрально")

print(predicted)


"""
with open('unique_words.txt', 'w') as fw:
    # записываем
    json.dump(unique_words, fw)

dump(model, 'filename.joblib')
"""