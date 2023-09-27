# AI-Powered-Analytics (AI Powered Python Kong Plugin)
## Overview
This is a AI Powered kong plugin developed using python which uses NLP and semantic analyzer to produce report form unformatted and ustructured data.
It uses open AI Key , NLP and Machine learning Algorithm to analyse the input data and produces human like response.

## Tested in Kong Release
Kong Enterprise 2.8.2.1

## Installation
### Install Kong Pdk and Python Packages 
```
$ apk update && apk add python3 py3-pip python3-dev musl-dev libffi-dev gcc g++ file make && PYTHONWARNINGS=ignore pip3 install kong-pdk
$ pip install llama-index==0.5.6
$ pip install langchain==0.0.148
$ pip install ipython
```
### Make the Below Changes in Kong.conf

```
$ pluginserver_names=python
$ pluginserver_python_socket=/usr/local/kong/python_pluginserver.sock
$ pluginserver_python_start_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> -v
$ pluginserver_python_query_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> --dump-all-plugins
```
After Installing the Plugin using any of the above steps . Add the Plugin Name in Kong.conf

```
plugins = bundled,AI-Powered-Analytics

```
### Restart Kong

```
kong restart

```
# Configuration Reference

## Enable the plugin on a Route

### Admin-API
For example, configure this plugin on a service by making the following request:
		
	curl -X POST http://{HOST}:8001/routes/{ROUTE}/plugins \
	--data "name=AI-Powered-Analytics"  \
	--data "config.OPENAI_API_KEY={OPENAI_API_KEY}"
	--data "config.model_name={MODEL_NAME}"

### Declarative(YAML)
For example, configure this plugin on a service by adding this section to your declarative configuration file:
			
	routes : 
	 name: {ROUTE}
	 plugins:
	 - name: AI-Powered-Analytics
	 config:
	   plugin_names: {OPENAI_API_KEY}
	   model_name : {MODEL_NAME}
	 enabled: true
	 protocols:
	 - grpc
	 - grpcs
	 - http
	 - https

ROUTE is the id or name of the route that this plugin configuration will target.
OPENAI_API_KEY is the openAI Key .
MODEL_NAME is the AI Model name


## Parameters

| FORM PARAMETER      | DESCRIPTION |
| ----------- | ----------- |
| ROUTE Type:string      | The name of the Route  the plugin targets.       |
| config.MODEL_NAME Type:string   | AI Model Name        |



## Contributors
Design & Developed By : Satyajit.Sial@VERIFONE.com ,Prema.Namasivayam@VERIFONE.com, dhaval.mavani@verifone.com
