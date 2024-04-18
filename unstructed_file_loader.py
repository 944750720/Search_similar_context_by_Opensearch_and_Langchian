import nltk
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_text_splitters import CharacterTextSplitter
from opensearchpy import OpenSearch
from elasticsearch import RequestsHttpConnection

os.environ["OPENAI_API_KEY"] = ""

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def test_unstructured_file_loader():
    all_texts = []
    folder_path = "/tmp/data/similarity_test_data_set/"
    file_names = os.listdir(folder_path)

    # Create a text splitter with chunk_size=1000
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    for file_name in file_names:
        # Create a file loader
        file_path = os.path.join(folder_path, file_name)
        loader = UnstructuredFileLoader(file_path)

        # Load the documents
        documents = loader.load()

        # Split the documents
        texts = text_splitter.split_documents(documents)
        all_texts.append(texts)

    # Create the OpenSearchVectorSearch object
    embeddings = OpenAIEmbeddings()
    docsearch = OpenSearchVectorSearch(
        index_name="similarity_test_data_set",
        embedding_function=embeddings,
        opensearch_url="http://localhost:9200",
        http_auth=("admin", "admin"),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        connection_class=RequestsHttpConnection
    )

    # Define the index mapping
    index_body = {
        "settings": {
            "index": {
                "knn": True,
                "number_of_shards": 4
            }
        },
        "mappings": {
            "properties": {
                "metadata": {
                    "properties": {
                        "source": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },
                "text": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "vector_field": {
                    "type": "knn_vector",
                    "dimension": 1536
                }
            }
        }
    }

    # Create the index
    docsearch.client.indices.create(index='similarity_test_data_set', body=index_body)

    # Add texts to the index
    for elem in all_texts:
        for doc in elem:
            docsearch.add_texts([doc.page_content], metadata=[doc.metadata])
    print('add texts complete')

    # Perform similarity search
    query = "search the top 3 documents with highest similarity score"
    kwargs = {"search_type": "script_scoring","space_type": "cosinesimil"}
    docs = docsearch.similarity_search_with_score(query, k=3, **kwargs)

    # Save the results to a file
    save_folder = "/usr/share/opensearch/data/"
    file_path = os.path.join(save_folder, 'top 3 documents with highest similarity score.txt')
    with open(file_path, 'w') as f:
        for doc in docs:
            f.write(doc[0].page_content)
            f.write('\n------------------------------------------------------------------\n')
    print('save complete')


test_unstructured_file_loader()