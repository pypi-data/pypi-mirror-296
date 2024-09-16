"""
MockerDB is a python module that contains mock vector database like solution built around
python dictionary data type. It contains methods necessary to interact with this 'database',
embed, search and persist.
"""

import logging
import json
import time
import copy
import numpy as np #==1.26.0
import dill #==0.3.7
import attr #==23.2.0
import hashlib
import concurrent.futures
from gridlooper import GridLooper #==0.0.1
from difflib import get_close_matches
import requests
import httpx

__design_choices__ = {}

# Imports
## essential







## for making keys

## for search

#! import hnswlib #==0.8.0
#! import sentence_transformers #==2.2.2


## for connect to remote mocker and llm search




# Metadata for package creation
__package_metadata__ = {
    "author": "Kyrylo Mordan",
    "author_email": "parachute.repo@gmail.com",
    "description": "A mock handler for simulating a vector database.",
    'license' : 'mit'
    # Add other metadata as needed
}

__design_choices__ = {
    'similarity search' : ['similarity search is optional, mocker can be used as normal database',
                           'to perform similarity searches mocker need to embed selected field during input',
                           'on retrieval by not providing query similarity search is not performed, only filters are used']

}

class SentenceTransformerEmbedder:

    def __init__(self,tbatch_size = 32, processing_type = 'batch', max_workers = 2, *args, **kwargs):
        # Suppress SentenceTransformer logging

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("Please install `sentence_transformers` to use this feature.")

        logging.getLogger('sentence_transformers').setLevel(logging.ERROR)
        self.tbatch_size = tbatch_size
        self.processing_type = processing_type
        self.max_workers = max_workers
        self.model = SentenceTransformer(*args, **kwargs)

    def embed_sentence_transformer(self, text):

        """
        Embeds single query with sentence tranformer embedder.
        """

        return self.model.encode(text)

    def embed(self, text, processing_type : str = None):

        """
        Embeds single query with sentence with selected embedder.
        """

        if processing_type is None:
            processing_type = self.processing_type

        if processing_type == 'batch':
           return self.embed_texts_in_batches(texts = text)

        if processing_type == 'parallel':
           return self.embed_sentences_in_batches_parallel(texts = text)

        return self.embed_sentence_transformer(text = str(text))

    def embed_texts_in_batches(self, texts, batch_size : int = None):
        """
        Embeds a list of texts in batches.
        """
        if batch_size is None:
            batch_size = self.tbatch_size

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings)
        return embeddings

    def embed_sentences_in_batches_parallel(self, texts, batch_size: int = None, max_workers: int = None):
        """
        Embeds a list of texts in batches in parallel using processes.
        """

        if batch_size is None:
            batch_size = self.tbatch_size

        if max_workers is None:
            max_workers = self.max_workers

        batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]

        embeddings = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {executor.submit(self.embed_sentence_transformer, batch): batch for batch in batches}

            for future in concurrent.futures.as_completed(future_to_batch):
                embeddings.extend(future.result())

        return embeddings

@attr.s
class MockerSimilaritySearch:

    search_results_n = attr.ib(default=10000, type=int)
    similarity_params = attr.ib(default={'space':'cosine'}, type=dict)
    similarity_search_type = attr.ib(default='linear')

    # output
    hnsw_index = attr.ib(init=False)

    logger = attr.ib(default=None)
    logger_name = attr.ib(default='Similarity search')
    loggerLvl = attr.ib(default=logging.INFO)
    logger_format = attr.ib(default=None)


    def __attrs_post_init__(self):
        self._initialize_logger()

        if self.similarity_search_type == 'hnsw':
            try:
                from hnswlib import Index
            except ImportError:
                print("Please install `hnswlib` to use this feature.")

            self.hnsw_index = Index


    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    def hnsw_search(self, search_emb, doc_embs, k=1, space='cosine', ef_search=50, M=16, ef_construction=200):
        """
        Perform Hierarchical Navigable Small World search.

        Args:
        - search_emb (numpy array): The query embedding. Shape (1, dim).
        - doc_embs (numpy array): Array of reference embeddings. Shape (num_elements, dim).
        - k (int): Number of nearest neighbors to return.
        - space (str): Space type for the index ('cosine' or 'l2').
        - ef_search (int): Search parameter. Higher means more accurate but slower.
        - M (int): Index parameter.
        - ef_construction (int): Index construction parameter.

        Returns:
        - labels (numpy array): Indices of the k nearest embeddings from doc_embs to search_emb.
        - distances (numpy array): Distances of the k nearest embeddings.
        """

        # Declare index
        dim = len(search_emb)#.shape[1]
        p = self.hnsw_index(space=space, dim=dim)

        # Initialize the index using the data
        p.init_index(max_elements=len(doc_embs), ef_construction=ef_construction, M=M)

        # Add data to index
        p.add_items(doc_embs)

        # Set the query ef parameter
        p.set_ef(ef_search)

        #self.hnsw_index = p

        # Query the index
        labels, distances = p.knn_query(search_emb, k=k)

        return labels[0], distances[0]

    def linear_search(self, search_emb, doc_embs, k=1, space='cosine'):

        """
        Perform a linear (brute force) search.

        Args:
        - search_emb (numpy array): The query embedding. Shape (1, dim).
        - doc_embs (numpy array): Array of reference embeddings. Shape (num_elements, dim).
        - k (int): Number of nearest neighbors to return.
        - space (str): Space type for the distance calculation ('cosine' or 'l2').

        Returns:
        - labels (numpy array): Indices of the k nearest embeddings from doc_embs to search_emb.
        - distances (numpy array): Distances of the k nearest embeddings.
        """

        # Calculate distances from the query to all document embeddings
        if space == 'cosine':
            # Normalize embeddings for cosine similarity
            search_emb_norm = search_emb / np.linalg.norm(search_emb)
            doc_embs_norm = doc_embs / np.linalg.norm(doc_embs, axis=1)[:, np.newaxis]

            # Compute cosine distances
            distances = np.dot(doc_embs_norm, search_emb_norm.T).flatten()
        elif space == 'l2':
            # Compute L2 distances
            distances = np.linalg.norm(doc_embs - search_emb, axis=1)

        # Get the indices of the top k closest embeddings
        if space == 'cosine':
            # For cosine, larger values mean closer distance
            labels = np.argsort(-distances)[:k]
        else:
            # For L2, smaller values mean closer distance
            labels = np.argsort(distances)[:k]

        # Get the distances of the top k closest embeddings
        top_distances = distances[labels]

        return labels, top_distances

    def search(self,
               query_embedding,
               data_embeddings,
               k : int = None,
               similarity_search_type: str = None,
               similarity_params : dict = None):

        if k is None:
            k = self.search_results_n
        if similarity_search_type is None:
            similarity_search_type = self.similarity_search_type
        if similarity_params is None:
            similarity_params = self.similarity_params

        if similarity_search_type == 'linear':
            return self.linear_search(search_emb = query_embedding, doc_embs = data_embeddings, k=k, **similarity_params)
        if similarity_search_type == 'hnsw':
            return self.hnsw_search(search_emb = query_embedding, doc_embs = data_embeddings, k=k, **similarity_params)

@attr.s
class MockerConnector:

    base_url = attr.ib(default = "http://localhost:8000")


    def __attrs_post_init__(self):

        self.client = httpx.Client(base_url=self.base_url)

    def read_root(self):
        response = self.client.get("/")
        return response.text

    def show_handlers(self):

        """
        Show active handlers
        """

        response = self.client.get("/active_handlers")
        return response.json()

    def remove_handlers(self,
                        handler_names : list):

        """
        Remove active handlers
        """

        response = self.client.post("/remove_handlers", json={"handler_names": handler_names})
        if response.status_code == 404:
            raise Exception(response.json()['detail'])
        return response.json()

    def initialize_database(self,
                            database_name : str = None,
                            embedder_params : dict = None):

        """
        Initialize database handler.
        """

        params = {}

        if database_name is not None:
            params["database_name"] = database_name

        if embedder_params is not None:
            params["embedder_params"] = embedder_params

        response = self.client.post("/initialize", json=params)
        return response.json()

    def insert_data(self,
                    data : list,
                    database_name : str = None,
                    var_for_embedding_name : str = None,
                    embed=False):

        request_body = {"data": data,
                        "var_for_embedding_name" : "text"}

        if var_for_embedding_name is not None:
            request_body["var_for_embedding_name"] = var_for_embedding_name
        if database_name is not None:
            request_body["database_name"] = database_name
        if embed is not None:
            request_body["embed"] = embed

        response = self.client.post("/insert", json=request_body)
        return response.json()

    def search_data(self,
                    database_name : str,
                    query : str = None,
                    filter_criteria : dict = None,
                    return_keys_list : list = None,
                    search_results_n : int = None,
                    similarity_search_type : str = None,
                    similarity_params : dict = None,
                    perform_similarity_search : bool = None):

        """
        Search data in selected handler
        """

        request_body = {"database_name" : database_name}

        if query is not None:
            request_body["query"] = query
        if filter_criteria is not None:
            request_body["filter_criteria"] = filter_criteria
        if return_keys_list is not None:
            request_body["return_keys_list"] = return_keys_list
        if search_results_n is not None:
            request_body["search_results_n"] = search_results_n
        if similarity_search_type is not None:
            request_body["similarity_search_type"] = similarity_search_type
        if similarity_params is not None:
            request_body["similarity_params"] = similarity_params
        if perform_similarity_search is not None:
            request_body["perform_similarity_search"] = perform_similarity_search

        response = self.client.post("/search", json=request_body)
        return response.json()

    def delete_data(self,
                    database_name : str,
                    filter_criteria : dict = None):

        """
        Delete data from selected handler
        """

        request_body = {"database_name": database_name}

        if filter_criteria is not None:
            request_body["filter_criteria"] = filter_criteria

        response = self.client.post("/delete", json=request_body)
        return response.json()

    def embed_texts(self,
                    texts : list,
                    embedding_model : str = None):

        """
        Embed list of text
        """

        request_body = {"texts": texts}

        if embedding_model is not None:
            request_body["embedding_model"] = embedding_model

        response = self.client.post("/embed", json=request_body)
        return response.json()


@attr.s
class LlmFilterConnector:

    connection_string = attr.ib(default = "http://localhost:8000/prompt_chat_parallel")
    headers = attr.ib(default={})
    system_message = attr.ib(default = """You are an advanced language model designed to search for specific content within a text snippet. Your task is to determine whether the provided text snippet contains information relevant to a given query. Your response should be strictly "true" if the relevant information is present and "false" if it is not. Do not provide any additional information or explanation. Here is how you should proceed:

1. Carefully read the provided text snippet.
2. Analyze the given query.
3. Determine if the text snippet contains information relevant to the query.
4. Respond only with "true" or "false" based on your determination.""")

    template = attr.ib(default = "Query: Does the text mention {query}? \nText Snippet: '''\n {text} \n'''")



    def _make_inputs(self, query : str, inserts : list, search_key : str, system_message = None, template = None):

        if system_message is None:
            system_message = self.system_message

        if template is None:
            template = self.template

        return [[{'role' : 'system',
                'content' : system_message},
                {'role' : 'user',
                'content' : template.format(query = query, text = dd[search_key])}] for dd in inserts]

    def _call_sync_llm(self, messages : list):

        """
        Calls llm.
        """

        request_body = {
            "messages": messages
        }


        response = requests.post(self.connection_string,
                                 headers = self.headers,
                                 json=request_body)

        return response.json()


    def filter_data(self,
                    query : str,
                    data : list,
                    search_key : str,
                    system_message = None,
                    template = None):

        """
        Prompts chat for search.
        """

        inserts = [value for _, value in data.items()]

        messages = self._make_inputs(query = query,
                                     inserts = inserts,
                                     search_key = search_key,
                                     system_message = system_message,
                                     template = template)


        responses = self._call_sync_llm(messages = messages)

        outputs = [res['message']['content'] for res in responses]

        output_filter = ['true' in out.lower() for out in outputs]

        return {d : data[d] for d,b in zip(data,output_filter) if b}


@attr.s
class MockerDB:
    # pylint: disable=too-many-instance-attributes

    """
    The MockerDB class simulates a vector database environment, primarily for testing and development purposes.
    It integrates various functionalities such as text embedding, Hierarchical Navigable Small World (HNSW) search,
    and basic data management, mimicking operations in a real vector database.

    Parameters:
        file_path (str): Local file path for storing and simulating the database; defaults to "../mock_persist".
        persist (bool): Flag to persist data changes; defaults to False.
        embedder_error_tolerance (float): Tolerance level for embedding errors; defaults to 0.0.
        logger (logging.Logger): Logger instance for activity logging.
        logger_name (str): Name for the logger; defaults to 'Mock handler'.
        loggerLvl (int): Logging level, set to logging.INFO by default.
        return_keys_list (list): Fields to return in search results; defaults to an empty list.
        search_results_n (int): Number of results to return in searches; defaults to 3.
        similarity_search_type (str): Type of similarity search to use; defaults to 'hnsw'.
        similarity_params (dict): Parameters for similarity search; defaults to {'space':'cosine'}.

    Attributes:
        data (dict): In-memory representation of database contents.
        filtered_data (dict): Stores filtered database entries based on criteria.
        keys_list (list): List of keys in the database.
        results_keys (list): Keys matching specific search criteria.

    """

    ## for embeddings
    embedder_params = attr.ib(default={'model_name_or_path' : 'paraphrase-multilingual-mpnet-base-v2',
                                       'processing_type' : 'batch',
                                       'tbatch_size' : 500})
    use_embedder = attr.ib(default=True)
    embedder = attr.ib(default=SentenceTransformerEmbedder)

    ## for llm filter
    llm_filter_params = attr.ib(default={})
    llm_filter = attr.ib(default=LlmFilterConnector)


    ## for similarity search
    similarity_params = attr.ib(default={'space':'cosine'}, type = dict)
    similarity_search = attr.ib(default=MockerSimilaritySearch)


    ## activate dependencies
    llm_filter_h = attr.ib(default=None)
    embedder_h = attr.ib(default=None)
    similarity_search_h = attr.ib(default=None)

    ##
    return_keys_list = attr.ib(default=None, type = list)
    ignore_keys_list = attr.ib(default=["embedding", 
                                        "&distance", 
                                        "&id",
                                        "&embedded_field"], type = list)
    search_results_n = attr.ib(default=10000, type = int)
    similarity_search_type = attr.ib(default='linear', type = str)
    keyword_check_cutoff = attr.ib(default=1, type = float)

    ## inputs with defaults
    file_path = attr.ib(default="./mock_persist", type=str)
    embs_file_path = attr.ib(default="./mock_embs_persist", type=str)
    persist = attr.ib(default=False, type=bool)

    embedder_error_tolerance = attr.ib(default=0.0, type=float)

    logger = attr.ib(default=None)
    logger_name = attr.ib(default='Mock handler')
    loggerLvl = attr.ib(default=logging.INFO)
    logger_format = attr.ib(default=None)

    ## data
    data = attr.ib(default=None, init=False)
    embs = attr.ib(default=None, init=False)

    ## outputs
    filtered_data = attr.ib(default=None, init=False)
    keys_list = attr.ib(default=None, init = False)
    results_keys = attr.ib(default=None, init = False)
    results_dictances = attr.ib(default=None, init = False)

    def __attrs_post_init__(self):
        self._initialize_logger()
        self._initialize_llm_filter()
        self._initialize_embedder()
        self._initialize_sim_search()


        self.data = {}

    def _initialize_logger(self):

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        if self.logger is None:
            logging.basicConfig(level=self.loggerLvl, format=self.logger_format)
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.loggerLvl)

            self.logger = logger

    def _initialize_llm_filter(self):

        """
        Initializes llm_filter connector with provided parameters.
        """

        if self.llm_filter_h is None:
            self.llm_filter_h = self.llm_filter(**self.llm_filter_params)

    def _initialize_embedder(self):

        """
        Initializes embedder connector with provided parameters.
        """
        if self.use_embedder:

            if self.embedder_h is None:
                self.embedder_h = self.embedder(**self.embedder_params)

    def _initialize_sim_search(self):

        """
        Initializes embedder connector with provided parameters.
        """

        if self.similarity_search_h is None:
            self.similarity_search_h = self.similarity_search(similarity_search_type = self.similarity_search_type,
                                                            search_results_n = self.search_results_n,
                                                            similarity_params = self.similarity_params,
                                                            logger = self.logger)

    
    def _hash_string_sha256(self,input_string : str) -> str:
        return hashlib.sha256(input_string.encode()).hexdigest()

    def _make_key(self,
                  d : dict,
                  embed : bool) -> str:

        input_string = json.dumps(d) + str(embed)

        return self._hash_string_sha256(input_string)

    def _make_embs_key(self,
                       text : str,
                       model : str) -> str:

        input_string = str(text) + str(model)

        return self._hash_string_sha256(input_string)

    def _prep_filter_criterias(self, filter_criteria : dict) -> list:

        """
        Makes a list of filters based on provided filter.
        """

        filter_criteria = {key: value if isinstance(value, list) else [value] \
            for key, value in filter_criteria.items()}

        gl = GridLooper()
        gl.prepare_search_grid(experiments_settings=filter_criteria)

        filter_criterias = gl.experiment_configs

        filter_criterias = [{k: v for k, v in filter_dict.items() if k != 'config_id'} \
            for filter_dict in filter_criterias]

        return filter_criterias

    def _insert_values_dict(self,
                            values_dicts : dict,
                            var_for_embedding_name : str,
                            model_name : str = None,
                            embed : bool = True) -> None:

        """
        Simulates inserting key-value pair into the mock database.
        """


        if embed:

            if model_name is None:
                model_name = self.embedder_params['model_name_or_path']

            list_of_text_to_embed = [values_dicts[insd][var_for_embedding_name] \
                for insd in values_dicts]

            # generate list of hashes
            list_of_hash_for_embeddings = [self._make_embs_key(text = text,
                                                               model = model_name) \
                for text in list_of_text_to_embed]

            # check which embeddings are not present already
            if model_name not in list(self.embs.keys()):
                self.embs[model_name] = {}

            current_embs_keys = list(self.embs[model_name].keys())
            filtered_list_of_text_to_embed = []
            existing_list_of_embeddings = []

            for new_hash, new_text in zip(list_of_hash_for_embeddings, list_of_text_to_embed):
                if new_hash is not current_embs_keys:
                    filtered_list_of_text_to_embed.append(new_text)
                else:
                    existing_list_of_embeddings.append(self.embs[model_name][new_hash])

            # embed new with embedder
            if self.embedder_h.processing_type in ['parallel', 'batch']:
                new_embedded_list_of_text = self.embedder_h.embed(text = filtered_list_of_text_to_embed)
            else:
                new_embedded_list_of_text = [self.embedder_h.embed(text = text_to_embed) \
                    for text_to_embed in filtered_list_of_text_to_embed]

            embedded_list_of_text = []
            # construct embeddings list from new and stored
            for new_hash, new_text in zip(list_of_hash_for_embeddings, list_of_text_to_embed):
                if new_hash is not current_embs_keys:
                    new_embedding = new_embedded_list_of_text.pop(0)
                    embedded_list_of_text.append(new_embedding)
                    # update embeddigs in embeddings storage
                    self.embs[model_name][new_hash] = new_embedding
                else:
                    embedded_list_of_text.append(existing_list_of_embeddings.pop(0))

            # assing embeddings to data
            i = 0
            for insd in values_dicts:
                values_dicts[insd]['&embedded_field'] = var_for_embedding_name
                values_dicts[insd]['embedding'] = embedded_list_of_text[i]
                i = i + 1

        # update data with embeddings
        self.data.update(values_dicts)
        # apply persist strategy
        self.save_data()


    def _check_if_match(self, content : str, cutoff : float, keyword_set : list):
        words = set(content.split())
        match = any(get_close_matches(keyword, words, cutoff=cutoff) for keyword in keyword_set)
        return match

    def _get_close_matches_for_keywords(self,
                                        data_key : str,
                                        keywords : list,
                                        cutoff : float):
        # Preprocess keywords into a set for faster membership checking
        keyword_set = set(keywords)
        matched_keys = set()

        if cutoff < 1:

            keyword_set = [keyword.lower() for keyword in keyword_set]

            matched_data = {key: value for key, value in self.data.items() \
                if self._check_if_match(content = value[data_key].lower(),
                                        cutoff = cutoff,
                                        keyword_set = keyword_set)}
        else:
            matched_data = {key: value for key, value in self.data.items() \
                if self._check_if_match(content = value[data_key],
                                        cutoff = cutoff,
                                        keyword_set = keyword_set)}

        return matched_data

    def _filter_database(self,
                        filter_criteria : dict = None,
                        llm_search_keys : list = None,
                        keyword_check_keys : list = None,
                        keyword_check_cutoff : float = None):

        """
        Filters a dictionary based on multiple field criteria.
        """

        if keyword_check_cutoff is None:
            keyword_check_cutoff = self.keyword_check_cutoff

        if keyword_check_keys is None:
            keyword_check_keys = []

        if llm_search_keys is None:
            llm_search_keys = []

        keyword_check_dict = {}
        llm_search_check_dict = {}

        filter_criteria_list = []
        if filter_criteria:
            for key in keyword_check_keys:
                keyword_check_dict[key] = filter_criteria[key]
                del filter_criteria[key]

            for key in llm_search_keys:
                llm_search_check_dict[key] = filter_criteria[key]
                del filter_criteria[key]

            if filter_criteria:
                filter_criteria_list = self._prep_filter_criterias(
                    filter_criteria = filter_criteria)


        self.filtered_data = {}

        if keyword_check_keys:

            filtered_data = {}

            for key, keywords in keyword_check_dict.items():
                filtered_data = self._get_close_matches_for_keywords(
                    data_key = key,
                    keywords = keywords,
                    cutoff=keyword_check_cutoff
                )
                self.filtered_data.update(filtered_data)

        if filter_criteria_list:

            filtered_data = {}

            filtered_data = {
                key: value for key, value in self.data.items()
                if any(all(value.get(k) == v for k, v in filter_dict.items()) \
                    for filter_dict in filter_criteria_list)}

            self.filtered_data.update(filtered_data)

        if llm_search_keys:

            filtered_data = self.filtered_data
            if keyword_check_keys == [] and filter_criteria_list == []:
                filtered_data = self.data

            for key, queries in llm_search_check_dict.items():

                for query in queries:

                    filtered_data = self.llm_filter_h.filter_data(
                        data = filtered_data,
                        search_key = key,
                        query = query)

            self.filtered_data = filtered_data

        if len(self.filtered_data) == 0:
            self.logger.warning("No data was found with applied filters!")

    
    def _search_database_keys(self,
        query: str,
        search_results_n: int = None,
        similarity_search_type: str = None,
        similarity_params: dict = None,
        perform_similarity_search: bool = None):

        """
        Searches the mock database using embeddings and saves a list of entries that match the query.
        """

        if search_results_n is None:
            search_results_n = self.search_results_n

        if similarity_search_type is None:
            similarity_search_type = self.similarity_search_type

        if similarity_params is None:
            similarity_params = self.similarity_params

        if self.filtered_data is None:
            self.filtered_data = self.data

        if self.keys_list is None:
            self.keys_list = [key for key in self.filtered_data]

        if perform_similarity_search is None:
            perform_similarity_search = True

        if perform_similarity_search:


            try:
                model_name = self.embedder_params['model_name_or_path']
                query_hash = self._make_embs_key(text = query, model = model_name)

                if model_name in list(self.embs.keys()):

                    if query_hash not in list(self.embs[model_name].keys()):
                        query_embedding = self.embedder_h.embed(query, processing_type='single')
                    else:
                        query_embedding = self.embs[model_name][query_hash]
                else:
                    self.embs[model_name] = {}
                    query_embedding = self.embedder_h.embed(query, processing_type='single')
                    self.embs[model_name][query_hash] = query_embedding


            except Exception as e:
                self.logger.error("Problem during embedding search query!", e)

            try:
                data_embeddings = np.array([(self.filtered_data[d]['embedding']) \
                    for d in self.keys_list if 'embedding' in self.filtered_data[d].keys()])
            except Exception as e:
                self.logger.error("Problem during extracting search pool embeddings!", e)

            try:

                if len(data_embeddings) > 0:
                    labels, distances = self.similarity_search_h.search(query_embedding = query_embedding,
                                                                        data_embeddings = data_embeddings,
                                                                        k=search_results_n,
                                                                        similarity_search_type = similarity_search_type,
                                                                        similarity_params = similarity_params)

                    self.results_keys = [self.keys_list[i] for i in labels]
                    self.results_dictances = distances
                else:
                    self.results_keys = []
                    self.results_dictances = None

            except Exception as e:
                self.logger.error("Problem during extracting results from the mock database!", e)

        else:

            try:
                self.results_keys = [result_key for result_key in self.filtered_data]
                self.results_dictances = np.array([0 for _ in self.filtered_data])
            except Exception as e:
                self.logger.error("Problem during extracting search pool embeddings!", e)

    def _prepare_return_keys(self,
                            return_keys_list : list = None,
                            remove_list : list = None,
                            add_list : list = None):

        """
        Prepare return keys.
        """

        if return_keys_list is None:
            return_keys_list = self.return_keys_list
        if remove_list is None:
            remove_list = self.ignore_keys_list.copy()
        if add_list is None:
            add_list = []


        return_distance = 0

        if "&distance" in remove_list:
            return_distance = 0
            remove_list.remove("&distance")
        if "&distance" in add_list:
            return_distance = 1
            add_list.remove("&distance")


        if return_keys_list:

            ra_list = [s for s in return_keys_list \
                if s.startswith("+") or s.startswith("-")]

            if "embedding" in return_keys_list:
                if "embedding" in remove_list:
                    remove_list.remove("embedding")

            for el in ra_list:

                if el[1:] == "&distance":

                    if el.startswith("+"):
                        return_distance = 1
                    else:
                        return_distance = 0

                else:
                    if el.startswith("+"):
                        if el[1:] not in add_list:
                            add_list.append(el[1:])
                        if el[1:] in remove_list:
                            remove_list.remove(el[1:])
                    else:
                        if el[1:] not in remove_list:
                            remove_list.append(el[1:])
                        if el[1:] in add_list:
                            add_list.remove(el[1:])

                return_keys_list.remove(el)

            if "&distance" in return_keys_list:
                return_keys_list.remove("&distance")
                if return_keys_list:
                    return_distance = 1
                else:
                    return_distance = 2

        return add_list, remove_list, return_keys_list, return_distance

    def _extract_from_data(self,
                        data : dict,
                        distances : list,
                        results_keys : list,
                        return_keys_list : list,
                        add_list : list,
                        remove_list : list,
                        return_distance : int):
        """
        Process and filter dictionaries based on specified return and removal lists.
        """

        if return_keys_list:
            remove_set = set(remove_list)
            return_keys_set = set(return_keys_list + add_list) - remove_set
            results = []

            if return_distance >= 1:
                for searched_doc, distance in zip(results_keys, distances):
                    result = {key: data[searched_doc].get(key) \
                        for key in return_keys_set}
                    result['&distance'] = distance
                    results.append(result)
            else:
                for searched_doc in results_keys:
                    result = {key: data[searched_doc].get(key) \
                        for key in return_keys_set}
                    results.append(result)
        else:
            keys_to_remove_set = set(remove_list)
            results = []

            if return_distance == 1:
                for searched_doc, distance in zip(results_keys, distances):
                    filtered_dict = data[searched_doc].copy()
                    for key in keys_to_remove_set:
                        filtered_dict.pop(key, None)

                    filtered_dict['&distance'] = distance
                    results.append(filtered_dict)
            elif return_distance == 2:
                results = [{'&distance' : distance} for distance in distances]

            else:
                for searched_doc in results_keys:
                    filtered_dict = data[searched_doc].copy()
                    for key in keys_to_remove_set:
                        filtered_dict.pop(key, None)
                    results.append(filtered_dict)

        return results

    def _get_dict_results(self,
                         return_keys_list : list = None,
                         ignore_keys_list : list = None) -> list:

        """
        Retrieves specified fields from the search results in the mock database.
        """

        (add_list,
        remove_list,
        return_keys_list,
        return_distance) = self._prepare_return_keys(
            return_keys_list = return_keys_list,
            remove_list = ignore_keys_list
            )

        # This method mimics the behavior of the original 'get_dict_results' method
        return self._extract_from_data(
            data = self.data,
            distances = self.results_dictances,
            results_keys = self.results_keys,
            return_keys_list = return_keys_list,
            add_list = add_list,
            remove_list = remove_list,
            return_distance = return_distance
        )


### EXPOSED METHODS FOR INTERACTION

    def establish_connection(self, file_path : str = None, embs_file_path : str = None):

        """
        Simulates establishing a connection by loading data from a local file into the 'data' attribute.
        """

        if file_path is None:
            file_path = self.file_path

        if embs_file_path is None:
            embs_file_path = self.embs_file_path

        try:
            with open(file_path, 'rb') as file:
                self.data = dill.load(file)
        except FileNotFoundError:
            self.data = {}
        except Exception as e:
            self.logger.error("Error loading data from file: ", e)

        try:
            with open(embs_file_path, 'rb') as file:
                self.embs = dill.load(file)
        except FileNotFoundError:
            self.embs = {}
        except Exception as e:
            self.logger.error("Error loading embeddings storage from file: ", e)

    def save_data(self):

        """
        Saves the current state of 'data' back into a local file.
        """

        if self.persist:
            try:
                self.logger.debug("Persisting values")
                with open(self.file_path, 'wb') as file:
                    dill.dump(self.data, file)
                with open(self.embs_file_path, 'wb') as file:
                    dill.dump(self.embs, file)
            except Exception as e:
                self.logger.error("Error saving data to file: ", e)

    def insert_values(self,
                      values_dict_list : list,
                      var_for_embedding_name : str = None,
                      embed : bool = True) -> None:

        """
        Simulates inserting key-value pairs into the mock Redis database.
        """

        values_dict_list = copy.deepcopy(values_dict_list)

        try:
            self.logger.debug("Making unique keys")
            # make unique keys, taking embed parameter as a part of a key
            values_dict_all = {self._make_key(d = d, embed=embed) : d for d in values_dict_list}
            values_dict_all = {key : {**values_dict_all[key], "&id" : key} for key in values_dict_all}
        except Exception as e:
            self.logger.error("Problem during making unique keys foir insert dicts!", e)

        try:
            self.logger.debug("Remove values that already exist")
            # check if keys exist in data
            values_dict_filtered = {key : values_dict_all[key] for key in values_dict_all.keys() if key not in self.data.keys()}

        except Exception as e:
            self.logger.error("Problem during filtering out existing inserts!", e)

        if values_dict_filtered != {}:
            try:
                self.logger.debug("Inserting values")
                # insert new values
                self._insert_values_dict(values_dicts = values_dict_filtered,
                                                    var_for_embedding_name = var_for_embedding_name,
                                                    embed = embed)

            except Exception as e:
                self.logger.error("Problem during inserting list of key-values dictionaries into mock database!", e)

    def flush_database(self):

        """
        Clears all data in the mock database.
        """

        try:
            self.data = {}
            self.save_data()
        except Exception as e:
            self.logger.error("Problem during flushing mock database", e)

    def search_database(self,
                        query: str = None,
                        search_results_n: int = None,
                        llm_search_keys : list = None,
                        keyword_check_keys : list = None,
                        keyword_check_cutoff : float = None,
                        filter_criteria : dict = None,
                        similarity_search_type: str = None,
                        similarity_params: dict = None,
                        perform_similarity_search: bool = None,
                        return_keys_list : list = None) ->list:

        """
        Searches through keys and retrieves specified fields from the search results
        in the mock database for a given filter.
        """

        if query is None:
            perform_similarity_search = False

        if filter_criteria:
            self._filter_database(
                filter_criteria = filter_criteria,
                llm_search_keys = llm_search_keys,
                keyword_check_keys = keyword_check_keys,
                keyword_check_cutoff = keyword_check_cutoff
                )
        else:
            self.filtered_data = self.data

        self._search_database_keys(query = query,
                                    search_results_n = search_results_n,
                                    similarity_search_type = similarity_search_type,
                                    similarity_params = similarity_params,
                                    perform_similarity_search = perform_similarity_search)

        results = self._get_dict_results(return_keys_list = return_keys_list)

        # resetting search
        self.filtered_data = None
        self.keys_list = None
        self.results_keys = None

        return results

    def remove_from_database(self, filter_criteria : dict = None):
        """
        Removes key-value pairs from a dictionary based on filter criteria.
        """

        if filter_criteria is None:
            filter_criteria_list = []
        else:
            filter_criteria_list = self._prep_filter_criterias(filter_criteria = filter_criteria)

        self.data = {
            key: value
            for key, value in self.data.items()
            if not any(all(value.get(k) == v for k, v in filter_criteria.items()) \
                for filter_criteria in filter_criteria_list)
        }

        self.save_data()