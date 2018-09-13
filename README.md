# Deep Learning for Tag Recommendation

This repository maintains the code for the final module assignment of the [Machine Learning]() and [Intelligent Systems for Internet](https://sites.google.com/site/sistemiintelligentiperinternet/) courses held at the University of Rome "Roma Tre" by the professors [Alessandro Micarelli](http://www.uniroma3.it/persone/Sjdza1hCU3JOWjBrTWxzWUNOcHd6a3BYMDBUSU5iUWhhY2V0cTE5N1RzMD0=/), [Giuseppe Sansonetti](http://www.dia.uniroma3.it/~ailab/?page_id=19) and [Fabio Gasparetti](http://www.dia.uniroma3.it/~ailab/?page_id=17).
The project was supervised by the PhD student [Hebatallah Mohamed](http://www.dia.uniroma3.it/~ailab/?page_id=670)

## Aim of the project
The aim of the project is to explore the performance of deep neural network models on text classification problems with respect of the literature models.

In order to compare the results of the neural network models, were developed three classifier based on Logistic Regression, Support Vector Machine and Naive Bayes.

Two different neural network models were developed. The two models share the same architecture, except for one of the hidden layer: in the first one is used an LSTM cell while in the other one a GRU cell is used.

## Environment Requirements
All the libraries used in order to run the project are exported in a Conda environment in order to maximize portability.
The necessaries files are under the folder `tagRecommendation/environments`.

In order to import the environment run the command `conda env create -f tagrec_py35.yml`

## Install and Resource Download.
<!-- In order to download the dataset and setting up the environment use the automated script `install.sh`.
This script will perform the following actions: -->

- Download the [GloVe680b300d](http://nlp.stanford.edu/data/glove.840B.300d.zip) embeddings.
- Import the conda environment.

## Project Structure

The structure of the project is the following:

``` bash
├── README.md
└── tagRecommendation
    ├── datasource # In this folder all the data items are stored
    │   │
    │   ├── model_checkpoints # In this folder all the checkpoints of the developed NN are saved.
    │   │   ├── first_model_weights.hdf5
    │   │   ├── fourth_model_weights.hdf5
    │   │   ├── gru_model_1_weights.hdf5
    │   │   ├── gru_model_2_weights.hdf5
    │   │   ├── gru_model_3_weights.hdf5
    │   │   ├── gru_model_4_weights.hdf5
    │   │   ├── second_model_weights.hdf5
    │   │   └── third_model_weights.hdf5
    │   │
    │   └── raw_data # This folder contains the original data
    │       ├── citeulike-a # This folder contains the CiteULike dataset
    │       │   ├── citations.dat
    │       │   ├── item-tag.dat
    │       │   ├── mult.dat
    │       │   ├── raw-data.csv
    │       │   ├── README.txt
    │       │   ├── tags.dat
    │       │   ├── users.dat
    │       │   └── vocabulary.dat
    │       │
    │       ├── export_missing_words # This folder contains an export of the articles words not found in GloVe
    │       │   ├── missing_words_g840b_title.dat
    │       │   ├── missing_words_g840b_titleraw.dat
    │       │   └── missing_words_g840b_title_titleraw_vocdat.dat
    │       │
    │       └── glove # This folders will contains the GloVe embeddings 
    │
    ├── environments # This folders contains all the conda environments.
    │   ├── spec_ubuntu64.txt
    │   └── tagrec_py35.yml
    │
    └── tag_recommendation.ipynb  # This is the main notebook 

```
