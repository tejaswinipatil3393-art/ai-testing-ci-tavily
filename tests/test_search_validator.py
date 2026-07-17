import pytest 

from app.search_validator import validate_search_results, validate_extracted_content 

@pytest.mark.integration 
def test_valid_search_response_should_pass():    
    response = {
            "results": [
                    {                
                            "title": "pytest documentation",                
                            "url": "https://docs.pytest.org/en/stable/",                
                            "content": "pytest is a Python testing framework."            
                        
                    }        
            ]    
    }    
    
    assert validate_search_results(
        response,        
        min_results=1,        
        required_terms=["pytest"]    
    ) is True 
    
    @pytest.mark.safety 
    def test_missing_results_should_fail():
           response = {"answer": "No search results returned"}    
           
           assert validate_search_results(response) is False 
           
    @pytest.mark.safety 
    def test_result_without_url_should_fail():    
        response = {        
             "results": [            
                {                
                       "title": "pytest documentation",               
                        "content": "pytest is a Python testing framework."            
                }        
            ]    
        }    
        
        assert validate_search_results(response) is False 
        
    @pytest.mark.integration 
    def test_valid_extract_response_should_pass():    
        response = {        
            "results": [
                {                
                    "url": "https://docs.pytest.org/en/stable/",
                    "raw_content": "pytest is a Python testing framework. " * 30            
                }        
            ]    
                    
        }    

        assert validate_extracted_content(response, min_chars=200) is True 
    
    @pytest.mark.safety 
    def test_short_extract_response_should_fail():    
        response = {        
            "results": [            
                {                
                       "url": "https://example.com",                
                       "raw_content": "too short"            
                }        
            ]    
        }    
        
        assert validate_extracted_content(response, min_chars=200) is False