"""
main.py — запуск чат-бота колл-центра
"""

from colorama import Fore, Style, init
from rag_agent import RAGAgent

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║     🤖  Чат-бот колл-центра (RAG)        ║
║  Введи вопрос или 'выход' для выхода     ║
║  Введи 'сброс' чтобы начать новый диалог ║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
"""


def main():
    print(BANNER)
    agent = RAGAgent()

    while True:
        try:
            user_input = input(f"{Fore.GREEN}Вы:{Style.RESET_ALL} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("выход", "exit", "quit"):
            print("До свидания!")
            break

        if user_input.lower() in ("сброс", "reset", "новый"):
            agent.reset()
            print(f"{Fore.YELLOW}[Диалог сброшен.]{Style.RESET_ALL}")
            continue

        print(f"{Fore.YELLOW}[Ищу в базе знаний...]{Style.RESET_ALL}")
        try:
            answer = agent.chat(user_input)
            print(f"\n{Fore.CYAN}Бот:{Style.RESET_ALL} {answer}\n")
        except Exception as e:
            print(f"{Fore.RED}[Ошибка]: {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
