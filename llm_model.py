from search_index import search_text


def ask_llm(co, search_index, texts, question, num_generations=1):
    # Get the query's embedding
    query_embed = co.embed(texts=[question]).embeddings
    
    # Search the text archive
    results = search_text(search_index, query_embed, texts)

    # Get the top result
    context = "\n".join(results)

    # Prepare the prompt
    prompt = f"""
    Here is some information about Sydney beaches: 
    {context}
    
    Based on the information provided, answer the following question:
    Question: {question}

    If the text doesn't contain the answer, 
    reply with a relevant answer using the information provided.
    """

    prediction = co.generate(
        prompt=prompt,
        max_tokens=700,
        model="command-nightly",
        temperature=0.5,
        num_generations=num_generations
    )

    return prediction.generations
