import argparse
from src.CHAT_AI import ask_ai


def main():
    parser = argparse.ArgumentParser(description="CLI application for the LLAMA AI assistant \n")
    parser.add_argument("-k", "--key", required=True, help="GROQ API key")
    args = parser.parse_args()

    context = []
    print("Welcome to the LLAMA AI assistant! \n")

    while True:
        try:
            response = ask_ai(context, args.key)
            print(f"\n")
            print(f"AI: {response} \n")
        except KeyboardInterrupt:
            print("Exiting the application")
            break 

if __name__ == '__main__':
    main()

