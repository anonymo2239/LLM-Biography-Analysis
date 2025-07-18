from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1)


messages = [
    SystemMessage(content="Translate the following sentence to English and German:"),
    HumanMessage(content="Benim adım Emirhan. Benimle tanışmak ister misin?")
]

if __name__ == "__main__":
    response = model.invoke(messages)
    print(response.content)
