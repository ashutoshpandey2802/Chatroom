import cohere

# Initialize Cohere client
def get_cohere_client(api_key: str):
    return cohere.Client(api_key)

# def get_cohere_client(api_key: "SkWcFdTpyIwsVAAoCIgW9b6vdnssYMgViMpI7AJg"):
#     return cohere.Client(api_key)
