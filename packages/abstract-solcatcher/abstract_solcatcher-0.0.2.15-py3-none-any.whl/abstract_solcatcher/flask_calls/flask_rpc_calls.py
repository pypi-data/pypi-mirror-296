from abstract_solcatcher.utils import get_async_response,getEndpointUrl,get_headers
from abstract_solcatcher.async_utils import asyncPostRequest
import json,requests
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
async def get_solcatcher_endpoint(endpoint,*args,**kwargs):
    return await asyncPostRequest(url=getEndpointUrl(endpoint),data=kwargs,headers=get_headers())

# Helper function to get Solcatcher API responses
def get_solcatcher_api(endpoint, *args, **kwargs):
    return get_async_response(get_solcatcher_endpoint, endpoint=endpoint, *args, **kwargs)
  
def getTxnTypeFromMint(address):
    return get_async_response(get_solcatcher_endpoint,endpoint="getTxnTypeFromMint",address=address)

def sendTransaction(txn, payer_keypair, opts=None,skip_preflight=None,preflightCommitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="sendTransaction",txn=txn, payer_keypair=payer_keypair, opts=opts,skip_preflight=skip_preflight,preflightCommitment=preflightCommitment)

def getGenesisSignature(address,before=None,limit=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getGenesisSignature",address=address,before=before,limit=limit)

def getSignaturesForAddress(address, limit=10, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
  return get_async_response(get_solcatcher_endpoint,endpoint="getSignaturesForAddress",address=address, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

def getTokenAccountBalance(account,mint=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountBalance",account=account,mint=mint,commitment=commitment)

def getTokenAccountsByOwner(account,mint=None,encoding=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountsByOwner",account=account,mint=mint,encoding=encoding)

def getMetaData(address):
  return get_async_response(get_solcatcher_endpoint,endpoint="getMetaData",address=address)

def getTransaction(signature,maxSupportedTransactionVersion=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTransaction",signature=signature,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

def getLatestBlockHash(commitment=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getLatestBlockhash",commitment=commitment)

def getAccountInfo(account,encoding=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getAccountInfo",account=account,encoding=encoding,commitment=commitment)

def getBlock(slot,encoding=None,maxSupportedTransactionVersion=None,transactionDetails= None,rewards=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getBlock",slot=slot,encoding=encoding,maxSupportedTransactionVersion=maxSupportedTransactionVersion,transactionDetails=transactionDetails,rewards=rewards)


