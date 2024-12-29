import json
import time
from query_data import query_rag

def process_questions(input_file, output_file):
    
    # Start the timer
    start_time = time.time()
    
    # Load the question set
    with open(input_file, "r") as file:
        question_set = json.load(file)

    # Prepare results
    results = []

    for qa in question_set:
        question = qa["question"]
        print(f"Processing question: {question}")

        # Query the RAG pipeline
        response = query_rag(question)
        
        # Add response to the result
        results.append({
            "question": question,
            "expected_answer": qa["answer"],
            "response": response
        })

    # Save results to a new JSON file
    with open(output_file, "w") as output:
        json.dump(results, output, indent=4)
        
        
    # End the timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Processing complete. Results saved to '{output_file}'.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


