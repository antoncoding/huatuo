import logging
import os
import sys
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from app.tools.search_tool import search_documents
from app.tools.time_tool import get_time_and_season

# Configure logging
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppress HTTP logs
logging.getLogger("telegram").setLevel(logging.WARNING)  # Suppress Telegram logs

# Set up console handler for all logs
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

class ChatService:
    """Handles chat interactions using ReAct agent."""
    
    def __init__(self):
        # Initialize LLM
        self.llm = self._init_llm()
        logger.info("LLM initialized")
        
        # Initialize agent with search tool
        self.agent = self._create_agent()
        logger.info("ChatService fully initialized and ready")
    
    def _init_llm(self):
        """Initialize the Claude LLM."""
        try:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            
            llm = BaseChatOpenAI(
                model='deepseek-chat',
                openai_api_key=api_key,
                openai_api_base='https://api.deepseek.com/v1',
                max_tokens=4096
            )

            return llm
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise
    
    def _create_agent(self):
        """Create the ReAct agent with the search tool."""
        try:
            system_prompt = """你是個熟悉中醫理論的中醫師，請利用你的中醫知識，配合中文醫學典籍，回答使用者提出的問題。

                你依照用戶的使用語言回答問題，記得引用經典時，使用引號包起來。
                
                必要工具 (MUST USE Tools) -- ALWAYS use the following tools

                1. 非常重要：使用 search_documents 工具來從中醫典籍中查找相關信息。使用簡潔的搜尋關鍵字
                [This is very important, You MUST use this tool to find the relevant information, weather to do additional research or to double check the answer]
                
                2. 非常重要：使用 get_time_and_season 工具來獲取當前的節氣、時辰。 
                [This tool is very important], Must use this to give the advice that is accurate and suit the current environment. 

                """
            
            memory = MemorySaver()


            # Create the agent
            agent = create_react_agent(
                model=self.llm,
                tools=[search_documents, get_time_and_season],
                prompt=system_prompt,
                checkpointer=memory
            )
            
            logger.info("ReAct agent created successfully")
            return agent
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise
    
    async def answer_question(self, user_id: str, question: str) -> str:
        """Answer a question using the ReAct agent."""
        try:
            logger.info(f"🤔 Processing question: {question}")
            
            config = {"configurable": {"thread_id": user_id}}

            # Invoke the agent
            response = await self.agent.ainvoke({
                "messages": [HumanMessage(content=question)],
            }, config)

            logger.info(f"💡 All response: {response}")

            answer = response["messages"][-1].content
            
            logger.info(f"💡 Generated answer: {answer[:100]}...")
            return answer
        except Exception as e:
            logger.error(f"❌ Error answering question: {str(e)}")
            return "I encountered an error while processing your question. Please try again later." 