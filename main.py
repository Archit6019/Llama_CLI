import argparse
import pyfiglet
from src.Chat_Base import ChatBase
from src.Chat_Doc import Chat_Documents
from src.Chat_image import Image_chat
import colorama
from colorama import Fore, Style
import os
import time
import warnings
warnings.filterwarnings('ignore')

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def print_banner():
    banner = pyfiglet.figlet_format("LLAMA AI Assistant")
    print(Fore.GREEN + banner + Style.RESET_ALL)

def print_menu():
    print(Fore.CYAN + "Please select an option:" + Style.RESET_ALL)
    print("1. Chat with AI (Base)")
    print("2. Chat with AI (Document)")
    print("3. Chat with AI (Image)")
    print("4. Exit application")

def main():
    parser = argparse.ArgumentParser(description="CLI Application for LLAMA AI Assistant")
    parser.add_argument("-k", "--key", required=True, help="GROQ Api key")
    args = parser.parse_args()

    print_banner()
    print_menu()
    choice = input(Fore.YELLOW + "Enter your choice (1/2/3/4): " + Style.RESET_ALL)

    context = []

    if choice == '2':
        print(Fore.GREEN + "Chat with DOC (currently supports .pdf)" + Style.RESET_ALL)
        file_path = input(Fore.YELLOW + "Please provide the file path: " + Style.RESET_ALL)
        ins = Chat_Documents(filepath=file_path, embedder_name="all-MiniLM-L6-v2", api_key=args.key)
        ins.preprocess()
        while True:
            try:
                user_input = input(Fore.BLUE + "USER: " + Style.RESET_ALL)
                response = ins.chat_doc(user_input)
                print(Fore.GREEN + "AI: " + Style.RESET_ALL + response)
            except KeyboardInterrupt:
                print(Fore.RED + "Exiting the Application" + Style.RESET_ALL)
                break

    elif choice == "1":
        print(Fore.GREEN + "AI Chat" + Style.RESET_ALL)
        while True:
            try:
                ins = ChatBase(api_key=args.key)
                response = ins.chat(context)
                print(Fore.GREEN + "AI: " + Style.RESET_ALL + response)
                print()
            except KeyboardInterrupt:
                print(Fore.RED + "Exiting the Application" + Style.RESET_ALL)
                break

    elif choice == "3":
        print(Fore.GREEN + "Chat with Image" + Style.RESET_ALL)
        api_key = input(Fore.YELLOW + "Please provide the OpenAI API Key: " + Style.RESET_ALL)
        image_url = input(Fore.YELLOW + "Please provide the image_url: " + Style.RESET_ALL)
        ins = Image_chat(api_key, image_url)
        while True:
            try:
                query = input(Fore.BLUE + "USER: " + Style.RESET_ALL)
                response = ins.chat_with_image(query=query)
                print(Fore.GREEN + "AI: " + Style.RESET_ALL + response)
            except KeyboardInterrupt:
                print(Fore.RED + "Exiting the Application" + Style.RESET_ALL)
                break

    elif choice == "4":
        print(Fore.RED + "Exiting the Application" + Style.RESET_ALL)
        exit()

    else:
        print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == '__main__':
    main()