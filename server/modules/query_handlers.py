from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        
        result = chain.invoke({"query": user_input})
        raw_sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        unique_sources = list(set(raw_sources))
        
        response = {
            "response": result["result"],
            "sources": unique_sources
        }
        
        logger.debug(f"Chain response: {response}")
        return response
        
    except Exception as e:
        logger.exception(f"Error in query_chain: {e}")
        raise