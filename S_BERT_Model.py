from sentence_transformers import SentenceTransformer, util

def sentence_bert(resume, job_des): # way 1
    # Load SBERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    job_embedding = model.encode(job_des, convert_to_tensor=True)
    resume_embedding = model.encode(resume, convert_to_tensor=True)

    # Calculate cosine similarity
    similarity = util.cos_sim(job_embedding, resume_embedding).item()

    return similarity
