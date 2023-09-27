#!/usr/bin/env python3
import os
import sys
import kong_pdk.pdk.kong as kong
from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
from IPython.display import Markdown, display
# from flask import Flask, request, jsonify

Schema = (
    {"OPENAI_API_KEY": {"type": "string"}},
    {"model_name": {"type": "string"}},
)

version = '0.1.0'
priority = 0

# This is an example plugin that uses Python Geocoding

class Plugin(object):
    def __init__(self, config):
        self.config = config

    def access(self, kong: kong.kong):
        kong.log.info("##########################  Inside Access Phase ######################################")
        os.environ["OPENAI_API_KEY"] = self.config['OPENAI_API_KEY']
        directory_path = "/tmp/analytics"
        max_input_size = 4096
        # set number of output tokens
        num_outputs = 2000
        # set maximum chunk overlap
        max_chunk_overlap = 20
        # set chunk size limit
        chunk_size_limit = 600


        # define prompt helper
        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        kong.log.info("########################## prompt_helper ##########################")
        
        # define LLM
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name=self.config['model_name'], max_tokens=num_outputs))
        kong.log.info("########################## llm_predictor ##########################")
        File_object = open("/tmp/analytics/file.txt", "w+")
        kong.log.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Prompt Query : ",kong.request.get_header("prompt"))
        File_object.write(kong.request.get_raw_body().replace('\r', ''))
        documents = SimpleDirectoryReader(directory_path).load_data()
        kong.log.info("documents")

        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        kong.log.info("########################## service_context ##########################")
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        kong.log.info("########################## index ##########################")
        index.save_to_disk('/tmp/file_index.json')
        print("Saved to disk")


        index = GPTSimpleVectorIndex.load_from_disk('/tmp/file_index.json')
        query = kong.request.get_header("prompt")
        response = index.query(query)
        display(Markdown(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Response: <b>{response.response}</b>"))
        return kong.response.exit(200, {"message":response.response} )


# add below section to allow this plugin optionally be running in a dedicated process
if __name__ == "__main__":
    from kong_pdk.cli import start_dedicated_server
    start_dedicated_server("AI-Powered-Analytics", Plugin, version, priority, Schema)