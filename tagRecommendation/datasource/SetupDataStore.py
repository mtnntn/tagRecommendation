import csv as csv
from pymongo import MongoClient

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from numpy import random
from math import floor


class SetupDataStore:

    def __init__(self, max_tag_to_analyze=20, train_set_perc_size=90):
        self.client = MongoClient("mongodb://localhost:27017")
        self.raw_db = self.client["raw_data"]
        self.articles_coll = self.raw_db["articles"]
        self.tags_coll = self.raw_db["tags"]
        self.data_set_db = self.client["data_set"]
        self.tags_coll_ds = self.data_set_db["tags"]
        self.articles_coll_ds = self.data_set_db["articles"]
        self.articles_coll_train = self.data_set_db["articles_train"]
        self.articles_coll_test = self.data_set_db["articles_test"]

        self.__import_articles()
        self.__import_tags()
        self.__bidirectional_reference()
        self.__initialize_data_set(max_tag_to_analyze)
        self.__tokenize_stopwords_stem_titles()
        self.__split_test_train_set(train_set_perc_size)

    def __import_articles(self):
        print("Importing articles . . .")
        with open("raw_data/citeulike-a/raw-data.csv", "r", encoding="iso-8859-15") as f:
            reader = csv.reader(f)
            for row in reader:
                doc = {
                    "_id": str(row[0]),
                    "title": row[1],
                    "citeulike-id": row[2],
                    "raw-title": row[3],
                    "raw-abstract": row[4],
                    "tag-list": []
                }
                self.articles_coll.insert_one(doc)
        print("---> added " + str(self.articles_coll.count()) + " articles")

    def __import_tags(self):
        print("Importing tags . . .")
        with open("raw_data/citeulike-a/tags.dat", "r") as f:
            reader = csv.reader(f)
            i = 1
            for row in reader:
                doc = {
                    "_id": str(i),
                    "tag": row[0],
                    "doc-list": []
                }
                i += 1
                self.tags_coll.insert_one(doc)
            print("---> added " + str(self.tags_coll.count()) + " tags")

    def __bidirectional_reference(self):
        print("Creating reference article-tags . . .")
        with open("raw_data/citeulike-a/item-tag.dat", "r") as f:
            reader = csv.reader(f)
            i = 1  # line = document id.
            for row in reader:
                doc_id = str(i)
                if row[0] != 0:  # tags are available for the i-th document
                    adjacency_list = row[0].split(" ")  # get the list of tag for the i-th document
                    for tag_id in adjacency_list:
                        tag_id = str(tag_id)
                        # doc-list is the set of document in which the tag can be applied.
                        # add the i-th doc to the current tag's doc list
                        # tag-list is the set of tag for the current document.
                        # add to the i-th document the list of tags.
                        self.tags_coll.update_one({"_id": tag_id}, {"$addToSet": {"doc-list": doc_id}})
                        self.articles_coll.update_one({"_id": doc_id}, {"$addToSet": {"tag-list": tag_id}})
                i += 1
        print("---> mapped reference doc-tags and tag-docs")

    def __initialize_data_set(self, max_tag_to_analyze):
        print("Initializing Dataset . . .")
        tags = list(self.tags_coll.find())  # get all tags
        tags.sort(key=lambda t: len(t['doc-list']), reverse=True)  # sort tags on doc-list length
        tags = tags[0:max_tag_to_analyze]
        articles_with_best_tag = []  # holds the ids of the docs that contains at least one of the best 20 tag.
        for tag in tags:  # iterate over the best MAX_TAG_LIST_SIZE tags
            for docId in tag["doc-list"]:
                if docId not in articles_with_best_tag:
                    articles_with_best_tag.append(docId)
        self.tags_coll_ds.insert_many(tags)  # persist the most frequent tags
        for article_id in articles_with_best_tag:  # persist the articles with at least one occurrence of a best tag.
            self.articles_coll_ds.insert(self.articles_coll.find_one({"_id": article_id}))
        print("---> Added " + str(self.tags_coll_ds.count()) + " tags to the data set")
        print("---> Added " + str(self.articles_coll_ds.count()) + " articles to the data set")

    def __tokenize_stopwords_stem_titles(self):
        print("Tokenize, remove stop words and stem phase . . .")
        docs = list(self.articles_coll_ds.find())
        for doc in docs:
            raw_title = doc["raw-title"]

            # TOKENIZE TITLE
            title_tokenized = sent_tokenize(raw_title)

            # REMOVE STOP WORDS AND STEMMING
            stop_words = set(stopwords.words('english'))
            # words_filtered = []
            stems = []
            ps = PorterStemmer()

            title_tokenized = " ".join([str(s) for s in title_tokenized])
            words_in_sentence = title_tokenized.split(" ")
            for w in words_in_sentence:
                if w not in stop_words:
                    # words_filtered.append(w)
                    stems.append(ps.stem(w))  # STEMMING

            # title_no_stop = " ".join([str(w) for w in words_filtered])
            title_stem = " ".join([str(w) for w in stems])

            doc["title_stemmed"] = title_stem
            self.articles_coll_ds.replace_one({"_id": doc["_id"]}, doc)

        print("---> done.")

    def __split_test_train_set(self, train_set_perc_size):
        tsps_str = str(train_set_perc_size)
        print("Extracting train-set and test-set with ratio "+tsps_str+":"+str(100-train_set_perc_size))

        if train_set_perc_size > 100 or train_set_perc_size <= 0:
            error = 'Invalid ratio between train-set and test-set: ' + \
                    'training set percentage size is not in the range [1-99], found ' +\
                    train_set_perc_size
            raise Exception(error)

        articles = list(self.articles_coll_ds.find())  # get all articles
        total_articles = len(articles)

        train_set_size = int(floor((total_articles * train_set_perc_size)/100))
        test_set_size = total_articles - train_set_size

        random.shuffle(articles)
        test_set = articles[0:test_set_size]
        train_set = articles[test_set_size:total_articles]

        self.articles_coll_test.insert_many(test_set)
        self.articles_coll_train.insert_many(train_set)

        print("-------> Total Documents: " + str(total_articles) + "\n" +
              "------- - Added " + str(self.articles_coll_train.count()) + " documents to Training-Set \n" +
              "------- - Added " + str(self.articles_coll_test.count()) + " documents to Test-Set \n")
