from lolpop.component.vector_store.base_vector_store import BaseVectorStore
from lolpop.utils import common_utils as utils
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry


@utils.decorate_all_methods([utils.error_handler, utils.log_execution()])
class LanceDBVectorStore(BaseVectorStore):
    __REQUIRED_CONF__ = {}

    __DEFAULT_CONF__ = {
        "config": {
            "LANCEDB_URI": "./.lancedb",
            "embedding_provider": "openai",
            "embedding_model_name": "text-embedding-ada-002",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = self._get_config("LANCEDB_URI")
        self.db = lancedb.connect(self.uri, **kwargs)


    def create_table(self, name, data, *args, **kwargs): 
        embedding_provider = self._get_config("embedding_provider")
        model_name = self._get_config("embedding_model_name")
        schema = self._get_schema(embedding_provider, model_name, **kwargs)
        return self.db.create_table(name, data,schema=schema,**kwargs)
    
    def get_table(self, name, *args, **kwargs): 
        return self.db.open_table(name, **kwargs)
    
    def update_table(self, table, data, *args, **kwargs): 
        return table.add(data, **kwargs)
    

    def query(self, table, vector, metric="l2", num=10, n_probes=10,refine_factor=None, *args, **kwargs):
        return table.search(vector, **kwargs).metric(metric).limit(num).nprobes(n_probes).refine_factor(refine_factor)
        #todo: if using hybrid search, implement rerankers
    
    def _list_tables(self, *args, **kwargs): 
        return self.db.table_names()
    
    def _build_index(self, table, index_type="IVF_PQ", num_partitions=256, num_sub_vectors=96, distance_type="L2", *args, **kwargs):
        if index_type == "IVF_PQ":
            return table.create_index(num_partitions=num_partitions, num_sub_vectors=num_sub_vectors, distance_type=distance_type,**kwargs)
        elif index_type == "FTS": 
            return table.create_fts_index(**kwargs)
        
    def _get_schema(self, embedding_provider, model_name, **kwargs): 
        #TODO: check if embedding_provider is custom and load in the lolpop class. 
        # i.e. embedding_provider is "custom" and "embedding_model_name" is a lolpop class that 
        # implements BaseEmbedding 

        func = get_registry().get(embedding_provider).create(name=model_name)

        class TextModel(LanceModel): 
            text: str = func.SourceField()
            vector: Vector(func.ndims()) = func.VectorField() 

        return TextModel
