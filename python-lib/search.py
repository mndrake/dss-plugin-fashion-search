import dataiku
from elasticsearch import Elasticsearch
import encoder

class FashionSearch(object):
    def __init__(self, es: Elasticsearch, model_folder:dataiku.Folder, image_folder:dataiku.Folder):
        self.es = es
        # initialize model
        self.model = encoder.model_fn(model_folder.get_path())
        # set project key and object ID of image folder
        self.project_key = image_folder.project_key
        self.image_object_id = image_folder.get_id()

    def generate_image_url(self, image_name):
        return f'/dip/api/managedfolder/preview-image?projectKey={self.project_key}&odbId={self.image_object_id}&itemPath={image_name}&contentType=image/jpeg'

    def semantic_search(self, query, k):
        feature_vector = encoder.predict_fn(query, self.model)
        search_query = {
            "size": k,
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'zalando_nlu_vector') + 1.0",
                        "params": {
                            "queryVector": feature_vector
                        }
                    }
                }
            }
        }
        response = self.es.search(index='idx_zalando', **search_query)
        results = [r['_source']['image'] for r in response['hits']['hits']]
        image_urls = [self.generate_image_url(i) for i in results]
        search = {'images': image_urls}
        return search
    
    def match_query(self, query, k):
        idx_name = 'idx_zalando'
        search_body = {
            "_source": {
                "excludes": ["zalando_nlu_vector"]
            },
            "highlight": {
                "fields": {
                    "description": {}
                }
            },
            "query": {
                "match": {
                    "description": {
                        "query": query
                    }
                }
            }
        }

        search_response = self.es.search(request_timeout=30, index=idx_name,
                                         body=search_body)['hits']['hits'][:k]

        search = [{'image': x['_source']['image'], 'description': x['highlight']['description']} for x in search_response]

        for i in range(len(search)):
            search[i]['presigned_url'] = self.generate_image_url([search[i]['image']][0])
            search[i]['description'] = " ".join(search[i]['description'])
            search[i]['description'] = search[i]['description'].replace("<em>",'<em style="background-color:#f18973;">')        

        return search
