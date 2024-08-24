from annoy import AnnoyIndex
import numpy as np

# Function to create and save the search index
def create_search_index(embeds, index_path='test.ann', num_trees=1000):
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])
    search_index.build(num_trees)
    search_index.save(index_path)
    return search_index

# Function to load the search index
def load_search_index(index_path, vector_size):
    search_index = AnnoyIndex(vector_size, 'angular')
    search_index.load(index_path)
    return search_index

# Function to search the text in the search index
def search_text(search_index, query_embed, texts, top_n=1000):
    similar_item_ids = search_index.get_nns_by_vector(query_embed[0], top_n, include_distances=True)
    return texts[similar_item_ids[0]]
