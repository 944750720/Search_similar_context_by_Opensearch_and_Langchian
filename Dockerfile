FROM opensearchproject/opensearch:2.11.1

# Copy data to /tmp/data
COPY similarity_test_data_set/ /tmp/data/similarity_test_data_set/
COPY unstructed_file_loader.py requirements.txt /var/task/

# Install dependencies
USER root
RUN dnf install -y python3.11 python3-pip
RUN python3.11 -m ensurepip --upgrade
RUN python3.11 -m pip install --upgrade pip setuptools
RUN pip3 install -r /var/task/requirements.txt
USER opensearch

# Run the loader
CMD ["python3.11", "/var/task/unstructed_file_loader.py"]