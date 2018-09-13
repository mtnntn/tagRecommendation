echo "Phase 1/3: Download GloVe..."
wget --directory-prefix=tagRecommendation/datasource/raw_data/glove/ http://nlp.stanford.edu/data/glove.840B.300d.zip
echo "GloVe Download complete."

echo "Phase 2/3: Extracting glove files"
unzip tagRecommendation/datasource/raw_data/glove/glove.840B.300d.zip
echo "GloVe embeddings extracted."

echo "Phase 3/3: Setting up conda environment..."
conda env create -f tagRecommendation/environments/tagrec_py35.yml
echo "Environment setup complete."
