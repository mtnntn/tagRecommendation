# Docker Tag Recommendation
Docker installation for the Machine Learning Project Tag Recomendation.

## Database
We are going to work on documents, articles to be more precise, so the perfect choice for store this kind of data is MongoDB a document-oriented noSQL database.

### Setup MongoDB
This command will start a docker container with name `tagrec-mongodb`, will bind the host port `27017` to the container port `27017` and link the host folder `/home/ndonio/Desktop/tagRecommendation/tagRecommendation/datasource/db_data` to the container folder `/data/db` in order to access data easely from host pc.

Obviously this path must be changed with your personal one.


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
Install `adicom/admin-mongo` in order to have a GUI tool for access mongodb installations.
The admin-mongo istance is linked to the container port `1234` from host port `27018` and therfore accessible via `http://localhost:27018`.

```
docker run -d -p 27018:1234 --name admin-mongo adicom/admin-mongo
```

Visit `http://localhost:27018` and add a new
connection for specifying this url: `mongodb://172.17.0.2:27017` where `172.17.0.2` must be substituted with the IP extracted previously.

## Data-set
There are different data files, all under concession of CiteUlike.

We are interested in this data-file:

- item-tag.dat : tags corresponding to articles, one line corresponds to tags of one article (note that this is the version prior to preprocess thus would have more tags than used in the paper)
- raw-data.csv : raw data
- tags.dat : tags, sorted by tag-id's

### Import the original data in MongoDB

Original data-set is placed inside the file `tagRecommendation/datasource/raw_data/citeulike-a/raw-data.csv`.

The file follow this structure: `"doc.id","title","citeulike.id","raw.title","raw.abstract"`

So the equivalent document object in our mongodb istance is structured as follow:

```
{
	_id : doc-id 
	title : ...
	citeulike-id : ...
	raw-title : ...
	raw-abstract : ...
}
```
Notice that the original **doc-id** became the document attribute **_id** in our MongoDB istance.
