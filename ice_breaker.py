from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from dotenv import load_dotenv

language = "Spanish"

def ice_breaker_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(profile_url=linkedin_username, mock=True)

    summary_template = """
        Given likedin information {information} a person that i want you to create in language {language}:
        1. A short summary.
        2. Two interesting facts about them.
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "language"],
        template=summary_template,
    )

    #llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    llm = ChatOllama(model="deepseek-r1:14b")

    chain = summary_prompt_template | llm | StrOutputParser()

    res= chain.invoke(input={"information": linkedin_data, "language": language})

    print(res)

if __name__ == '__main__':
    load_dotenv()
    print("Ice Breaker Enter: ")
    ice_breaker_with(name="Eden Marco")