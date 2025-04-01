from dotenv import load_dotenv


load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub
from langchain_ollama import ChatOllama
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.tools import get_profile_tavily_url

def lookup(name: str) -> str:
    #llm = ChatOllama(model="deepseek-r1:14b")
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """ Given the full name of a person {name_of_person} I want you to get it me a link to their LinkedIn profile page.
                Your answer should contain only a URL."""
    
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template=template,
    )

    tools_for_agent = [
        Tool(
            name="LinkedIn Lookup profile page",
            func=get_profile_tavily_url,
            description="Useful to get the LinkedIn profile URL of a person given their name. it returns more than one, order by score accurate.",
        )
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
        )
    
    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    name = "Eden Marco"
    linkedin_url = lookup(name)
    print(linkedin_url)
    
    