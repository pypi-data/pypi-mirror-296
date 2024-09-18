import asyncio
from abstract_apis import get_url,make_endpoint,get_headers
def getSolcatcherUrl():
  return 'https://solcatcher.io'
def getEndpointUrl(endpoint=None,url=None):
  url = url or getSolcatcherUrl()
  endpoint = make_endpoint(endpoint or '/')
  return get_url(url,endpoint)
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
def ifListGetSection(listObj,section=0):
    if isinstance(listObj,list):
        if len(listObj)>section:
            return listObj[section]
    return listObj
def get_async_response(async_function, *args, **kwargs):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if not loop.is_running():
        # Only run the loop if it's not already running
        return loop.run_until_complete(async_function(*args, **kwargs))
    else:
        # If the loop is already running, directly run the coroutine
        return asyncio.ensure_future(async_function(*args, **kwargs))
