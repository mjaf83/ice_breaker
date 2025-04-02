from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from typing import List, Dict, Any
from typing import Tuple

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

language = "Spanish"

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="Interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
        }

summary_parser = PydanticOutputParser(pydantic_object=Summary)

def ice_breaker_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(profile_url=linkedin_username, mock=True)

    summary_template = """
        Given likedin information {information} a person that i want you to create in language {language}:
        1. A short summary.
        2. Three interesting facts about them.
        \n{format_instructions}
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "language"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
            }
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    #llm = ChatOllama(model="deepseek-r1:14b")

    chain = summary_prompt_template | llm | summary_parser

    res:Summary= chain.invoke(input={"information": linkedin_data, "language": language})

    return res, linkedin_data["photoUrl"]

if __name__ == '__main__':
    load_dotenv()
    print("Ice Breaker Enter: ")
    ice_breaker_with(name="Eden Marco")