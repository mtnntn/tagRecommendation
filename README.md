# Docker Tag Recommendation
Docker installation for the Machine Learning Project Tag Recommendation.

## Database
We are going to work on documents, articles to be more precise, so the perfect choice for store this kind of data is MongoDB, a document-oriented NoSQL database.

### Setup MongoDB
This command will start a docker container with name `tagrec-mongodb`, will bind the host port `27017` to the container port `27017` and link the host folder `/home/ndonio/Desktop/tagRecommendation/tagRecommendation/datasource/db_data` to the container folder `/data/db` in order to access data easily from host pc.
(Obviously this path must be changed with your personal one).
```
/* pull docker image and start associated container. */
docker run -d -p 27017:27017 -v /home/ndonio/Desktop/tagRecommendation/tagRecommendation/datasource/db_data:/data/db --name tagrec-mongodb mongo

/* Add first user to the db */
docker exec -it tagrec-mongodb mongo admin

/* Add user to the database */
db.createUser({ user: 'admin', pwd: 'admin', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });

```
### Get Container Ip
Run `docker inspect tagrec-mongodb` and take note of the container ip listed under the key `IPAddres`:
```
...
"Network": {
	 ...
	 "IPAddress": "172.17.0.2"
	 ...
}
```

### Setup Admin-Mongo
Install `adicom/admin-mongo` in order to have a GUI tool for access MongoDB installations.
The admin-mongo instance is linked to the container port `1234` from host port `27018` and therefore accessible via `http://localhost:27018`.

```
docker run -d -p 27018:1234 --name admin-mongo adicom/admin-mongo
```

Visit `http://localhost:27018` and add a new
connection for specifying this URL: `mongodb://172.17.0.2:27017` where `172.17.0.2` must be substituted with the IP extracted previously.

## Setup Data-set
There are different data files, all under concession of CiteUlike.

We are interested in this data-file:

- item-tag.dat : tags corresponding to articles, one line corresponds to tags of one article (note that this is the version prior to preprocess thus would have more tags than used in the paper)
- raw-data.csv : raw data
- tags.dat : tags, sorted by tag-id's

### Import the original data in MongoDB

Original data-set is placed inside the file `tagRecommendation/datasource/raw_data/citeulike-a/raw-data.csv`.

The file follow this structure: `"doc.id","title","citeulike.id","raw.title","raw.abstract"`

Launching the Script `Top20.py` will initialize the database.
There are 2 database `raw_data`, `test_data`.

##### Database "raw_data"
The `raw_data` database contains 2 collections: `articles` and `tag`.

###### Collection "articles"

Document stored under `articles` contains the original dataset extracted from the file `tagRecommendation/datasource/raw_data/citeulike-a/raw-data.csv`.

The equivalent document object in our MongoDB instance is structured as follow:
```
{
	"_id": "10",
	"raw-title": "Early language acquisition: cracking the speech code.",
	"title": "early language acquisition cracking the speech code",
	"citeulike-id": "60",
	"raw-abstract": "Infants learn language with remarkable speed, but how they do it remains a mystery...",
	"tag-list": ["12", "18187", ..., "30698", "34995"],
}
```
Notice that the original **doc-id** became the document attribute **_id** in our MongoDB instance.

The `tag-list` attribute contains a list of tag-id extracted from the file `tagRecommendation/datasource/raw_data/citeulike-a/item-tag.dat`.
In this file, in fact, each line refers to a document with a 1:1 mapping between document_id-line, and each line contains a list of tag-id associated to the document.


###### Collection "tags"
The collection `tags` in the `raw_data` database contains all the available tags.

The documents were extracted from the file `tagRecommendation/datasource/raw_data/citeulike-a/tags.dat` and follows this structure:
```
{
    "_id": "4",
    "tag": "newsciencenetwork",
    "doc-list": [ "19", "22", "52", "81", "111", .... , "16784"]
}
```
The `_id` is the line number in which the tag was placed inside the document `tags.dat`, the `tag` attribute contains the text description of the tag and the `doc_list` attribute contains a list of documents from which the tag was extracted according to the file `tagRecommendation/datasource/raw_data/citeulike-a/item-tag.dat`.

##### Database "data_set"

The execution of the script `Top20.py` generate also a `data_set` database.
This database, as the previous one, contains 2 main collections : `articles` and `tags`.

###### Collection "tags"
In the `tags` collection are stored the "best" 20 tag documents where, for "best" tags, we intend the the 20 most frequent tags extracted from the documents.
The collection was populated sorting the collection `tags` in the `raw_data` database according to the length of the attribute `doc-list`.

###### Collection "articles"
In the `articles` collection are stored, instead, the article documents in which at least one of the tag of the best-tag list is present in the `tag-list` attribute.

A document in this collection maintain the main structure of a document stored in the `articles` collection of the `raw_data` database:
```
{
	"_id": "10",
	"raw-title": "Early language acquisition: cracking the speech code.",
	"title": "early language acquisition cracking the speech code",
	"citeulike-id": "60",
	"title_stemmed": "Earli languag acquisition: crack speech code.",
	"raw-abstract": "Infants learn language with remarkable speed, but how they do it remains a mystery...",
	"tag-list": ["12", "18187", ..., "30698", "34995"],
}
```
The attribute `title_stemmed` is the representation of the title after the pre-processing phase in which were applied tokenization, stop words removal and stemming.

For this phase has been used the python library `nltk`.
To use the library you need to download the material by running this script :
```
import nltk command
nltk.download ()
```

The details of the procedure that allow to obtain the stemmed title can be appreciated in the python class `SetupDataStore`:
```
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
```
For the stemming phase was used the Porter stemming algorithm.

###### Collection "articles_test_set"
###### Collection "articles_train_set"
