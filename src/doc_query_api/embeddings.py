from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text:str)->list[float]:
    result=model.encode(text)
    return result.tolist()
    
