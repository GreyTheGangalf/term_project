from langgraph.graph import StateGraph, END
from pipeline.state import AgentState
from pipeline.agents import macro_agent_node, fundamental_agent_node,technical_agent_node, portfolio_manager_node

workflow = StateGraph(AgentState)

workflow.add_node("macro_agent", macro_agent_node)
workflow.add_node("fundamental_agent", fundamental_agent_node)
workflow.add_node("technical_agent", technical_agent_node)
workflow.add_node("portfolio_manager", portfolio_manager_node)

workflow.set_entry_point("macro_agent") 
workflow.add_edge("macro_agent", "fundamental_agent") 
workflow.add_edge("fundamental_agent", "technical_agent")
workflow.add_edge("technical_agent", "sentiment_agent")
workflow.add_edge("sentiment_agent", "portfolio_manager")
workflow.add_edge("portfolio_manager", END) 

app = workflow.compile()

if __name__ == "__main__":
    print("=== LANGGRAPH PIPELINE TEST IS STARTING ===")
    
    initial_state = {
        "current_date": "2026-05-15",
        "ticker": "THYAO.IS",
        "portfolio_cash": 10000.0,
        "portfolio_holdings": {"THYAO.IS": 0}
    }
    
    final_state = app.invoke(initial_state)
    
    print("\n=== FINAL DECISION ===")
    print(final_state["final_decision"])