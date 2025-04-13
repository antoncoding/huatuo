import requests

def chat_with_bot(question: str) -> str:
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": question}
    )
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return f"Error: {response.text}"

def main():
    print("Chat with your documents (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        question = input("\nYour question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        print("\nThinking...")
        answer = chat_with_bot(question)
        print("\nAnswer:", answer)
        print("-" * 50)

if __name__ == "__main__":
    main() 