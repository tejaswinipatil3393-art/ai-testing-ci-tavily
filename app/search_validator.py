def validate_search_results(response, min_results=1, required_terms=None): 
    """    Validates a Tavily-style search response.   
    
      We check predictable properties:    
      1. Response must be a dictionary.    
      2. It must contain a non-empty results list.    
      3. Each important result should have a URL.    
      4. Each important result should have title or content.    
      5. Optional required terms should appear somewhere in results.    """   
    
    if not isinstance(response, dict):
              return False    
    
    results = response.get("results")   

    if not isinstance(results, list):        
        return False    
    
    if len(results) < min_results:        
          return False   
    
    for item in results[:min_results]:
      if not isinstance(item, dict):
          return False
                              
      url = item.get("url", "")
      title = item.get("title", "")       
      content = item.get("content", "")        
    
    if not isinstance(url, str) or not url.startswith("http"):            
      return False    
    
    if not title and not content:           
      return False    

    if required_terms:        
        combined_text = " ".join(            [                
            str(item.get("title", "")) + " " +                
            str(item.get("content", "")) + " " +                
            str(item.get("url", ""))                
            for item in results            
            ]        
            ).lower()        
        
    for term in required_terms:            
      if term.lower() not in combined_text:                
        return False   
                
    return True


def validate_extracted_content(response, min_chars=200):
     """   
       Validates a Tavily Extract response.    
     
     Tavily Extract usually returns:    
     {        
        "results": [            
            {"url": "...", "raw_content": "..."}        
            ]    
            }    """    
     if not isinstance(response, dict):        
        return False    
     results = response.get("results")    
     
     if not isinstance(results, list) or len(results) == 0:        
        return False    
     
     combined_content = " ".join(        
         [str(item.get("raw_content", "")) for item in results if isinstance(item, dict)] 
       )    
     
     return len(combined_content.strip()) >= min_chars