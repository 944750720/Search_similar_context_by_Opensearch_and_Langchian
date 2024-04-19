# Search_similar_context_by_Opensearch_and_Langchian

This project provides a Python script for loading unstructured text data, splitting it into chunks by Langchain, and processing it with OpenSearch to get a vector representation of each chunk. These vectors can then be used for various natural language processing tasks, such as text classification, semantic similarity comparison, or information retrieval. I also use OpenAI's GPT model to query so that I can get response for searching similar context, or other NLP tasks can be done by GPT model.

## Requirements

- Docker
- OpenSearch service
- OpenAI API key (You need to subscribe it from https://openai.com/)

## Preparation

1. Clone this repository:

    ```bash
    git clone https://github.com/944750720/Search_similar_context_by_Opensearch_and_Langchian.git

    cd Search_similar_context_by_Opensearch_and_Langchian
    ```

2. Set your OpenAI API key in `unstructed_file_loader.py`:

    ```python
   os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
    ```

## Usage

1. Build Docker image and run the container:

    ```bash
    docker-compose up --build
    ```

This script will load all text files from the `similarity_test_data_set` directory, split each file into chunks of 1000 characters, and process each chunk with OpenAI's GPT model in Docker container. The processed data will be stored in the `/usr/share/opensearch/data/` directory. (in Docker)

In this project, I asked GPT to find out top 3 documents with highest similarity score.
