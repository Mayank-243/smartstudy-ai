# chat_with_agent.py

from src.agents.agent import agent
from src.memory.conversation import ConversationMemory


def main():
    memory = ConversationMemory(max_messages=10)
    
    print("=" * 60)
    print("SmartStudy AI — Chat with Memory")
    print("Type 'exit' to quit, 'clear' to clear history")
    print("=" * 60)
    
    while True:
        user_input = input("\n🙋 You: ").strip()
        
        if user_input.lower() == "exit":
            print("Bye!")
            break
        
        if user_input.lower() == "clear":
            memory.clear()
            print("🧹 History cleared!")
            continue
        
        if not user_input:
            continue
        
        memory.add_user_message(user_input)
        
        result = agent.invoke({
            "messages": memory.get_messages()
        })
        
        ai_response = result["messages"][-1].content
        
        memory.add_ai_message(ai_response)
        
        print(f"\n🤖 AI: {ai_response}")


if __name__ == "__main__":
    main()