from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pipeline.state import AgentState
from pipeline.tools import get_local_macro_data
from pipeline.tools import get_fundamental_data
from pipeline.tools import get_price_history

llm = ChatOllama(
    model="mistral:7b", 
    temperature=0.1, 
    format="json"
)

macro_llm_with_tools = llm.bind_tools([get_local_macro_data])

def macro_agent_node(state: AgentState) -> dict:
    """
    Macro Analysis Agent: Reads historical data, retrieves data using the EVDS tool, and interprets market conditions.
    """
    print(f"--- MACRO AGENT IS RUNNING (Date: {state.current_date}) ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert macroeconomist.
        Your task is to retrieve the inflation, interest rate, and unemployment data for the specified date using the provided tool.
        Analyze this data to assess the current state of the market (bull/bear market, tightening/easing cycle, risk appetite).
        Your output must be concise, clear, and actionable for the portfolio manager."""),
        ("user", "Date to be analyzed: {current_date}. Please retrieve the macro data and summarize the situation.")
    ])
    
    chain = prompt | macro_llm_with_tools
    
    response = chain.invoke({"current_date": state.current_date})
    
    return {"macro_context": response.content}



fundamental_llm_with_tools = llm.bind_tools([get_fundamental_data])

def fundamental_agent_node(state: AgentState) -> dict:
    """
    Fundamental Analysis Agent: Reads the ticker symbol and date, retrieves the balance sheet, and analyzes the company's financial health.
    """
    print(f"--- FUNDAMENTAL ANALYSIS AGENT IS RUNNING (Asset: {state.ticker}, Date: {state.current_date}) ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior stock analyst (Value Investor).
        Your task is to retrieve the financial data for the asset (ticker) assigned to you as of the specified date using the provided tool.
        Analyze the company’s profitability, debt levels, and valuation metrics by reviewing the balance sheet, income statement, and cash flow data.
        Your output should be clear, data-driven, and summarized in a way that provides a basis for the portfolio manager’s buy/sell decision."""),
        ("user", "Asset to be analyzed: {ticker}. Analysis date: {current_date}. Please retrieve the fundamental data and assess the company's situation.")
    ])
    
    chain = prompt | fundamental_llm_with_tools
    
    response = chain.invoke({
        "current_date": state.current_date,
        "ticker": state.ticker
    })
    
    return {"fundamental_context": response.content}


technical_llm_with_tools = llm.bind_tools([get_price_history])

def technical_agent_node(state: AgentState) -> dict:
    """
    Technical Analysis Agent: Analyzes price and volume movements over the past 30 days and performs short-term trend analysis.
    """
    print(f"--- TECHNICAL ANALYSIS TOOL IS RUNNING ({state.ticker}) ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a quantitative technical analyst (Swing Trader).
        Your task is to use a tool to retrieve the historical price movements of the asset provided to you, starting from a specified date.
        Analyze the trend direction (upward/downward) in the price series, potential momentum breakouts, and changes in volume.
        Your output should be clear and objective, providing the portfolio manager with insights regarding “short-term timing.”"""),
        ("user", "Asset to be analyzed: {ticker}. Target Date: {current_date}. Please retrieve the price data for the last 30 days and summarize the technical outlook.")
    ])
    
    chain = prompt | technical_llm_with_tools
    response = chain.invoke({"current_date": state.current_date, "ticker": state.ticker})
    
    return {"technical_context": response.content}


from pipeline.tools import get_sentiment_data # En üste ekle

sentiment_llm_with_tools = llm.bind_tools([get_sentiment_data])

def sentiment_agent_node(state: AgentState) -> dict:
    """
    Sentiment Agent: Analyzes the news feed and market sentiment.    """
    print(f"--- SENTIMENT AGENT IS RUNNING ({state.ticker}) ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a financial sentiment analyst.
        Your job is to use the tool to monitor the news flow surrounding the asset and gauge market sentiment.
        Report any signs of panic, euphoria, or manipulation to the portfolio manager in a concise and clear manner."""),
        ("user", "Asset: {ticker}, Date: {current_date}. Please retrieve the sentiment data and summarize the situation.")
    ])
    
    chain = prompt | sentiment_llm_with_tools
    response = chain.invoke({"current_date": state.current_date, "ticker": state.ticker})
    
    return {"sentiment_context": response.content}


def portfolio_manager_node(state: AgentState) -> dict:
    """
    Decision Agent: Reads the reports generated by the Macro and Fundamental Analysis agents,
    and determines the final portfolio allocation and BUY/SELL/HOLD decision.
    Note: This agent does not connect directly to the database (it does not use a tool); it only reads the reports from other agents.
    """
    print(f"--- PORTFOLIO MANAGER MAKES A DECISION ({state.ticker}) ---")
    
    # Karar ajanının araca (tool) ihtiyacı yoktur, veriyi State'ten alır.
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the chief portfolio manager. Your job is to read the reports submitted to you by the specialist analysts (Macro and Fundamental) under your supervision and make the final investment decision.
        If the macroeconomic environment is very poor, you may choose to take a defensive stance even if the fundamental data is good.
        Take into account your current cash position and held assets.
        Your final decision (BUY, SELL, or HOLD) should include the trade size and a brief rationale."""),
        ("user", """
        Asset Under Analysis: {ticker}
        Date: {current_date}

        Current Portfolio: Cash={portfolio_cash}, Holdings={portfolio_holdings}

        Macroeconomic Analyst Report:
        {macro_context}

        Fundamental Analysis Report:
        {fundamental_context}

        Technical Analysis Report (Timing and Momentum):
        {technical_context}

        Please make your final investment decision:
        """)
    ])
    
    chain = prompt | llm 
    
    response = chain.invoke({
        "ticker": state.ticker,
        "current_date": state.current_date,
        "portfolio_cash": state.portfolio_cash,
        "portfolio_holdings": state.portfolio_holdings,
        "macro_context": state.macro_context,
        "fundamental_context": state.fundamental_context,
        "technical_context": state.technical_context
    })

    return {"final_decision": response.content}