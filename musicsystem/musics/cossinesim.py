import numpy as np
import pandas as pd





def onehotencode(df, column, prefix='', sep='_'):
    if prefix == '':
        prefix = column
    
    df_ohe = pd.get_dummies(df[column])
    df_ohe.columns = [prefix + sep + str(col) for col in df_ohe.columns]
    df_ohe.reset_index(drop = True, inplace = True) 
    return df_ohe
    




def tfidf(df, column, prefix='', sep='_'):
    if prefix == '':
        prefix = column

    # get all unique genres 
    genres = df[column].str.split(',').explode().unique()
    
    # get term frequencies = term count / len of each document
    # (since each genre is repeated max once per document, term counts = one hot encoded (get_dummies))
    doc_len = df[column].str.split(',').str.len().values[:,None] # get length of each document
    tf = df[column].str.get_dummies(sep=',') / doc_len

    # get counts of each genre in all documents
    counts = df[column].str.get_dummies(sep=',').sum(axis=0)

    # get inverse document frequency
    # log( total num of documents / num of documents with term t in it(=counts)))
    idf = np.log(len(df) / counts+1) # add 1 to denominator to avoid division by 0 
    idf = np.expand_dims(idf, axis=0)

    # get tf-idf
    tfidf = tf * idf

    # convert to dataframe
    df_tfidf = pd.DataFrame(tfidf)
    df_tfidf.columns = [prefix + sep + i for i in genres]
    df_tfidf.reset_index(drop = True, inplace=True)

    return df_tfidf    



def cosine_similarity(vector1, vector2):
    # vector1 and vector2 are 2D numpy arrays
    # each row is a document, each column is a feature
    # returns a 1D numpy array of similarity scores
    # vector1.shape = (m, n)
    # vector2.shape = (m, n)
    # m = number of documents
    # n = number of features

    if (vector1.shape == vector2.shape ):
        cos_sim = np.dot(vector1, vector2) / (np.linalg.norm(vector1, axis=1) * np.linalg.norm(vector2, axis=1))
        
    elif (vector1.shape[1] == vector2.shape[1]): # return 1D array of similarity scores for each document
        cos_sim = np.dot(vector1, vector2.T) / (np.linalg.norm(vector1, axis=1) * np.linalg.norm(vector2, axis=1))
    else:
        raise ValueError("Vector shapes are not compatible")
    
    return cos_sim


def split_metadata_features(df):
    # get numerical columns
    num_cols = df.select_dtypes(include=np.number).columns

    # get featureset
    featureset = pd.concat([df['id'], df[num_cols]], axis=1) # id could be useful
    metadata = df.drop(num_cols, axis=1) # metadata is everything else
    return metadata, featureset



def get_similar_track_ids(df, track_id, n=10):
    # get metadata and featureset
    metadata, df = split_metadata_features(df)
    # get track features
    track_features = df[df['id'] == track_id].drop('id', axis=1)

    

    # drop track from featureset and metadata
    df.drop(df[df['id'] == track_id].index, inplace=True)
    metadata.drop(metadata[metadata['id'] == track_id].index, inplace=True)
    
    
    # get similarity scores
    metadata['sim_score'] = cosine_similarity(track_features, df.drop('id', axis=1)).T


    # get top n similar tracks
    top_n = metadata.sort_values('sim_score', ascending=False).head(n)

    return top_n






