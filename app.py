"""
LexIntel Legal AI Chatbot
Terminal interface
"""

from src.chatbot import ask_chatbot


def main():

    print("\nLexIntel Legal AI Chatbot is ready.")
    print("Ask any legal question.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("Your question: ")

        if question.lower() == "exit":
            print("Goodbye.")
            break

        answer = ask_chatbot(question)

        print("\nLegal Answer:\n")
        print(answer)
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()