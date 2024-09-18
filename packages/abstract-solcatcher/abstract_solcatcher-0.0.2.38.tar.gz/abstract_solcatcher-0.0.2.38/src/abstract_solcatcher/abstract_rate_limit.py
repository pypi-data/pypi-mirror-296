from .utils import getEndpointUrl,get_async_response
from abstract_apis import getRequest,requests,asyncPostRpcRequest,asyncPostRequest,asyncGetRequest,get_headers
from abstract_utilities import make_list
import json
async def asyncMakeLimitedDbCall(method=None, params=[],*args,**kwargs):
    response = getRequest(url=getEndpointUrl("dbSearch"), data={"method":method, "params":make_list(params)[0]},headers=get_headers())
    if response != None:
      print(f'search of {method}  successful')
      return response
    urls = await async_get_rate_limit_url(method)
    response = await asyncPostRpcRequest(
        url=urls.get('url'), method=method, params=params, status_code=True, response_result='result'
    )
    
    if response[1] == 429:
        response = await asyncPostRpcRequest(
            url=urls.get('url2'), method=method, params=params, response_result='result', status_code=True
        )
    response = response[0]
    await async_log_response(method,response)
    await asyncPostRequest(url=getEndpointUrl("dbInsert"), data={"method":method, "params":params,"result":response}, status_code=True)
    return response

def makeLimitedDbCall(method=None, params=[],*args,**kwargs):
    return get_async_response(asyncMakeLimitedDbCall, method, params)

async def asyncMakeLimitedCall(method=None, params=[]):
    urls = await async_get_rate_limit_url(method)
    response = await asyncPostRpcRequest(
        url=urls.get('url'), method=method, params=params, status_code=True, response_result='result'
    )
    
    if response[1] == 429:
        response = await asyncPostRpcRequest(
            url=urls.get('url2'), method=method, params=params, response_result='result', status_code=True
        )
    
    await async_log_response(method, response[0])
    return response[0]

def makeLimitedCall(method=None, params=[]):
    return get_async_response(asyncMakeLimitedCall, method, params)

async def async_get_rate_limit_url(method='default_method'):
    return await asyncGetRequest(url=getEndpointUrl("rate_limit"),data={"method":str(method)})

def get_rate_limit_url(method_name, *args, **kwargs):
    return get_async_response(async_get_rate_limit_url, method_name, *args, **kwargs)

async def async_log_response(method='default_method', response_data={}):
    return await asyncPostRequest(url=getEndpointUrl("log_response"),data={"method":str(method),"response_data":response_data})

def log_response(method_name, response_data, *args, **kwargs):
    return get_async_response(async_log_response, method_name, response_data, *args, **kwargs)
