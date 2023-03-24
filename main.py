from modules.chatgpt import ChatGPT

def main() -> None:
    chatgpt = ChatGPT(open("config/chatgpt.conf", "r", encoding="utf-8"))
    try:
        while True:
            to_trans = str(input("輸入英文："))
            print(f"\n{chatgpt.post(to_trans)}\n")

    except Exception as e:
        print(e.with_traceback())

if __name__ == "__main__":
    main()