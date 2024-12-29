import json
import time
from query_data import query_rag
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

GRADER_PROMPT_TEMPLATE = """
You are an expert evaluator. Grade the response based on the following criteria:
1. Groundedness: Does the response fully address the question using the provided context?
2. Answer Relevance: Is the response relevant and directly answering the question?
3. Context Relevance: Is the response actually correct based on the context?

Context:
{context}

Question:
{question}

Response:
{response}

---

Provide a float score from 0 to 1 for each criteria and a short explanation for the score.
"""

class Grader:
    def __init__(self):
        """
        Initializes the Grader class to evaluate the responses.
        """
        self.model = OllamaLLM(model="llama3")  # Grading LLM

    def grade(self, context: str, question: str, response: str) -> str:
        """
        Grades the response based on the context and question using a prompt template.

        Args:
            context (str): The retrieved context from the database.
            question (str): The input query text.
            response (str): The generated response to evaluate.

        Returns:
            str: The grading result with a score and an explanation.
        """
        # Prepare the grading prompt
        prompt_template = ChatPromptTemplate.from_template(GRADER_PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context, question=question, response=response
        )

        # Invoke the grading model
        grading_result = self.model.invoke(prompt)
        return grading_result

def main():
    input_file = "question_set.json"
    output_file = "processed_questions.json"
    
    # Start the timer
    start_time = time.time()
    
    # Load the question set
    with open(input_file, "r") as file:
        question_set = json.load(file)

    processed_questions = []

    # Process each question and store the response
    for qa in question_set:
        question = qa["question"]
        expected_answer = qa.get("answer", "N/A")
        print(f"Processing question: {question}")

        # Query the RAG pipeline
        llm_answer = query_rag(question)
        
        # Grade the response
        grader = Grader()
        grading_result = grader.grade(expected_answer, question, llm_answer)
        
        # Store the result
        processed_questions.append({
            "question": question,
            "expected_answer": expected_answer,
            "llm_answer": llm_answer,
            "grading_result": grading_result
        })

    # Write the processed questions to the output file
    with open(output_file, "w") as file:
        json.dump(processed_questions, file, indent=4)
        
     # End the timer
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Processing complete. Results saved to '{output_file}'.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()