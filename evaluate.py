from chatbot import Chatbot
import json
import time
from datetime import datetime

def evaluate_chatbot():
    # Initialize chatbot
    chatbot = Chatbot()
    
    # Test cases
    test_cases = [
        "What is VisaBridge?",
        "How many countries do you support?",
        "How do I get started with the process?",
        "Can you remember what VisaBridge is and tell me how to start?",  # Testing memory
    ]
    
    results = []
    
    for test_case in test_cases:
        # Record start time
        start_time = time.time()
        
        # Get response
        response = chatbot.get_response(test_case)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Store result
        results.append({
            "query": test_case,
            "response": response,
            "response_time": response_time
        })
    
    # Save evaluation results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    evaluation_file = f"evaluation_logs_{timestamp}.json"
    
    with open(evaluation_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "total_queries": len(test_cases),
            "average_response_time": sum(r["response_time"] for r in results) / len(results),
            "results": results
        }, f, indent=2)
    
    print(f"Evaluation completed. Results saved to {evaluation_file}")

if __name__ == "__main__":
    evaluate_chatbot() 