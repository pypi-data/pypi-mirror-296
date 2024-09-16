from faiss_vector_aggregator import aggregate_embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import faiss
import os
import numpy as np

# Aggregate embeddings
input_folder = "../../../Indices/foncier_ar_index/"
output_folder = "../../../Indices/foncier_ar_index/foncier_agg_index/"
column_name = "id"  # The metadata column to aggregate by

aggregate_embeddings(input_folder, column_name, output_folder)

os.environ["OPENAI_API_KEY"] = "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"
# Load the aggregated index
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
aggregated_index = FAISS.load_local(output_folder, embeddings, allow_dangerous_deserialization=True)

# Perform a similarity search
query = "هل يستوجب الحصول على رخصة من الوالي لبعض العمليات العقارية"
query_embedding = embeddings.embed_query(query)


# Convert the list to a NumPy array
query_embedding = np.array(query_embedding, dtype='float32')

# Reshape the query embedding to match expected dimensions
query_embedding = query_embedding.reshape(1, -1)

# Normalize the query embedding if needed
faiss.normalize_L2(query_embedding)

# Perform similarity search
results = aggregated_index.similarity_search_by_vector(query_embedding[0], k=5)

# Print out the IDs or metadata of the results
for doc in results:
    print(doc.metadata['name'])

