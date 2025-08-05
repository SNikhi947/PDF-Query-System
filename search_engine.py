import cohere

co = cohere.Client("korv6munGd0a3gPtoheXu3uHR6vw8xvhucrKYWae")

def get_embeddings(text_list):
    response = co.embed(
        texts=text_list,
        model="embed-english-v3.0",
        input_type="search_document"  
    )
    return response.embeddings

def cosine_similarity(vec1, vec2):
    from numpy import dot
    from numpy.linalg import norm
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def find_most_relevant_chunk(query, chunks):
    chunk_embeddings = get_embeddings(chunks)
    query_embedding = get_embeddings([query])[0]

    similarities = [cosine_similarity(query_embedding, emb) for emb in chunk_embeddings]
    
  
    top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:3]
    top_chunks = [chunks[i] for i in top_indices]
    top_scores = [similarities[i] for i in top_indices]
    
    return top_chunks, top_scores