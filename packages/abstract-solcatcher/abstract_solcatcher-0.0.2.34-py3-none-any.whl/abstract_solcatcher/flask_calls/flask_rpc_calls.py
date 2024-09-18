from ..utils import get_async_response,getEndpointUrl,get_headers
from ..async_utils import asyncPostRequest
import json,requests,base58
from ..abstract_rate_limit import makeLimitedCall
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
async def get_solcatcher_endpoint(endpoint,*args,**kwargs):
    return await asyncPostRequest(url=getEndpointUrl(endpoint),data=kwargs,headers=get_headers())

# Helper function to get Solcatcher API responses
def get_solcatcher_api(endpoint, *args, **kwargs):
    return get_async_response(get_solcatcher_endpoint, endpoint=endpoint, *args, **kwargs)
  
def getTxnTypeFromMint(address):
    return get_async_response(get_solcatcher_endpoint,endpoint="getTxnTypeFromMint",address=address)

def sendTransaction(txn, payer_keypair , opts=None, skip_preflight=True):
  return get_async_response(get_solcatcher_endpoint,endpoint="sendTransaction",txn=txn, payer_keypair=payer_keypair, opts=opts)

def getGenesisSignature(address,before=None,limit=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getGenesisSignature",address=address,before=before,limit=limit)

def getSignaturesForAddress(address, limit=10, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
  return get_async_response(get_solcatcher_endpoint,endpoint="getSignaturesForAddress",address=address, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

def getTokenAccountBalance(account,mint=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountBalance",account=account,mint=mint,commitment=commitment)

def getTokenAccountsByOwner(account,mint=None,encoding=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getTokenAccountsByOwner",account=account,mint=mint,encoding=encoding)

def getMetaData(mint):
  return get_async_response(get_solcatcher_endpoint,endpoint="getMetaData",mint=mint)

def getTransaction(tx_sig=None,signature=None,commitment=None,maxSupportedTransactionVersion=None):
  tx_sig = tx_sig or signature
  return get_async_response(get_solcatcher_endpoint,endpoint="getTransaction",tx_sig=tx_sig,commitment=commitment,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

def getLatestBlockHash(commitment=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getLatestBlockhash",commitment=commitment)

def getAccountInfo(account,encoding=None,commitment=None):
  return get_async_response(get_solcatcher_endpoint,endpoint="getAccountInfo",account=account,encoding=encoding,commitment=commitment)

def getBlock(slot,encoding=None,maxSupportedTransactionVersion=None,transactionDetails= None,rewards=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="getBlock",slot=slot,encoding=encoding,maxSupportedTransactionVersion=maxSupportedTransactionVersion,transactionDetails=transactionDetails,rewards=rewards)

def getParsedTransaction(tx_sig=None,txnData=None,signature=None,programId=None,encoding=None,commitment=None,maxSupportedTransactionVersion=None):
    tx_sig = tx_sig or signature
    return get_async_response(get_solcatcher_endpoint,endpoint="getParsedTransaction",tx_sig=tx_sig,txnData=txnData,programId=programId,encoding=encoding,commitment=commitment,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

def quickBuyData(mint=None):
    return get_async_response(get_solcatcher_endpoint,endpoint="dbSearch",tableName="quickbuydata",searchValue=mint)

def getTxLog(tx_sig=None,signature=None):
    tx_sig = tx_sig or signature
    return get_async_response(get_solcatcher_endpoint,endpoint="getTxLog",tx_sig=tx_sig)

def insertTxLogs(txLogs):
    return get_async_response(get_solcatcher_endpoint,endpoint="insertTxLogs",txLogs=txLogs)

def sendTransaction(txn: Transaction, payer_keypair, opts=None,skip_preflight=None) -> dict:
    skip_preflight = skip_preflight or True
    opts = opts or TxOpts(skip_preflight=skip_preflight)
    # Sign the transaction
    txn.sign(payer_keypair)
    method="sendTransaction"
    # Serialize the transaction to a base64 string
    txn_base64 = base58.b58encode(txn.serialize()).decode('utf-8')
    params = [txn_base64, {"skipPreflight": opts.skip_preflight, "preflightCommitment": "finalized"}]
    # Prepare the RPC request payload
    # Send the transaction
    return makeLimitedCall(method,params)
