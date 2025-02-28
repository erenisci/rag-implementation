from rag import ask_question


if __name__ == "__main__":
    while True:
        question = input("Enter your question: ")
        if question.lower() == "exit":
            print("Exiting... Have a great day!")
            break

        answer = ask_question(question)
        print("AI Answer:", answer, "\n")
