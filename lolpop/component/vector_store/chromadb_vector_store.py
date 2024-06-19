from lolpop.component.vector_store.base_vector_store import BaseVectorStore
from lolpop.utils import common_utils as utils
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class ChromaDBVectorStore(BaseVectorStore):
    __REQUIRED_CONF__ = {}

    __DEFAULT_CONF__ = {
        "config": {
            "CHROMADB_URI": "./.chromadb",
            "CHROMADB_CLIENT_MODE": "persistent",
            "embedding_function_class": "OpenAIEmbeddingFunction",
            "embedding_model_name": "text-embedding-ada-002",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client_mode = self._get_config("CHROMADB_CLIENT_MODE")

        if client_mode == "persistent": 
            self.uri = self._get_config("CHROMADB_URI")

            self.db = chromadb.PersistentClient(self.uri, **kwargs)
        elif client_mode == "client_server": 
            host = self._get_config("CHROMADB_HOST")
            port = self._get_config("CHROMA_DB_PORT")

            self.db = chromadb.HttpClient(host=host, port=port)
        else: 
            self.log("Unsupported chromadb client mode: %s" %client_mode)

    def create_table(self, name, data, ids, *args, **kwargs):
        embedding_function_class = self._get_config("embedding_function_class")
        model_name = self._get_config("embedding_model_name")
        fn = self._get_embedding_func(embedding_function_class, model_name, **kwargs)


        collection = self.db.create_collection(name=name, embedding_fn = fn, **kwargs)
        collection.add(documents=data, ids=ids)
        return collection 

    def get_table(self, name, *args, **kwargs):
        embedding_function_class = self._get_config("embedding_function_class")
        model_name = self._get_config("embedding_model_name")
        fn = self._get_embedding_func(embedding_function_class, model_name, **kwargs)
        return self.db.get_collection(name, embedding_fn = fn, **kwargs)

    def update_table(self, collection, data, ids, *args, **kwargs):
        return collection.update(documents=data, ids=ids, **kwargs)

    def query(
        self,
        collection,
        vector,
        num=10,
        *args,
        **kwargs,
    ):
        return (
            collection.query(query_embedding = vector, 
                             n_results = num, 
                             **kwargs)
        )
        

    def _list_tables(self, *args, **kwargs):
        return self.db.table_names()

           
    def _delete_docs(self, collection, ids, *args, **kwargs): 
        collection.delete(ids=ids, **kwargs)

    def _get_embedding_func(self, embedding_function_class, model_name, **kwargs): 
        #TODO: Allow custom embeddings which load embedding class from lolpop 

        embedding_func_cl = getattr(embedding_functions, embedding_function_class)
        if embedding_func_cl is not None: 
            embedding_fn = embedding_func_cl(model_name=model_name, **kwargs)
            return embedding_fn
        else: 
            self.log("Unable to find embedding function class %s" %embedding_function_class)
            return None 
