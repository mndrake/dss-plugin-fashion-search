from dataiku.customwebapp import *
import dataiku
dataiku.use_plugin_libs("fashion-search")
from elasticsearch import Elasticsearch
#from search import FashionSearch
from flask import jsonify, request

# Load Model
model_folder = dataiku.core.managed_folder.Folder(get_webapp_config()["model_folder"])

# Get Image Folder
image_folder = dataiku.core.managed_folder.Folder(get_webapp_config()["image_folder"])

# Get ES Index Name
es_index = get_webapp_config()["es_index"] #TODO: Use specified es_index

# #TODO: Use connection based on specified ES index
# # Initialize Elasticsearch connection
# es = Elasticsearch()

# # Initialize Fashion Search main class
# fs = FashionSearch(es, model_folder, image_folder)


# @app.route('/semantic_search', methods=['POST'])
# def semantic_search():
#     data = request.json
#     result = fs.semantic_search(**data)
#     return jsonify(result)


# @app.route('/es_match', methods=['POST'])
# def es_match():
#     data = request.json
#     result = fs.match_query(**data)
#     return jsonify(result)