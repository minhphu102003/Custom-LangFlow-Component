"""
Agent Component Wrapper for Langflow Custom Components.

This module provides a wrapper for AgentComponent that can be used in custom components
to process queries with MCP server tools via SSE.
"""

from typing import List, Dict, Any, Optional
import asyncio
import concurrent.futures
from langflow.field_typing import Tool


class AgentComponentWrapper:
    """
    Wrapper for AgentComponent that can process queries with MCP tools.
    
    This class provides a simplified interface for using AgentComponent instances
    in custom processors, particularly for parallel processing scenarios.
    """
    
    def __init__(self, agent_component_class, mcp_server: Optional[Tool] = None, **agent_kwargs):
        """
        Initialize the AgentComponentWrapper.
        
        Args:
            agent_component_class: The AgentComponent class to instantiate
            mcp_server: MCP server tool to connect to the agent
            **agent_kwargs: Additional arguments to pass to the agent component
        """
        self.agent_component_class = agent_component_class
        self.mcp_server = mcp_server
        self.agent_kwargs = agent_kwargs
        self.agent_instance = None
    
    def _initialize_agent(self):
        """
        Initialize an AgentComponent instance with MCP server tools.
        
        Returns:
            AgentComponent: Initialized agent instance
        """
        # Create a new instance of the agent component
        agent = self.agent_component_class()
        
        # Set agent parameters
        for key, value in self.agent_kwargs.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        # Connect MCP server tools if provided
        if self.mcp_server:
            # Add MCP tools to the agent
            if not hasattr(agent, 'tools') or agent.tools is None:
                agent.tools = []
            
            # Add the MCP server tool to the agent's tools
            if isinstance(agent.tools, list):
                agent.tools.append(self.mcp_server)
            else:
                agent.tools = [self.mcp_server]
        
        return agent
    
    async def process_query_async(self, query: str) -> Dict[str, Any]:
        """
        Process a query using an AgentComponent instance with MCP tools asynchronously.
        
        Args:
            query (str): The query to process
            
        Returns:
            Dict[str, Any]: Result from processing the query
        """
        try:
            # Initialize agent for this query
            agent = self._initialize_agent()
            
            # Set the input value for the agent
            agent.input_value = query
            
            # Process the query using the agent
            response = await agent.message_response()
            
            return {
                "query": query,
                "response": response.text if hasattr(response, 'text') else str(response),
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "query": query,
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a query using an AgentComponent instance with MCP tools.
        
        Args:
            query (str): The query to process
            
        Returns:
            Dict[str, Any]: Result from processing the query
        """
        try:
            # Initialize agent for this query
            agent = self._initialize_agent()
            
            # Set the input value for the agent
            agent.input_value = query
            
            # Process the query using the agent
            # For synchronous processing, we need to handle the async method
            import asyncio
            
            # Try to get the current event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # If no event loop exists, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async method in the event loop
            response = loop.run_until_complete(agent.message_response())
            
            return {
                "query": query,
                "response": response.text if hasattr(response, 'text') else str(response),
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "query": query,
                "response": None,
                "success": False,
                "error": str(e)
            }


def process_queries_with_agents_parallel(
    queries: List[str], 
    agent_component_class, 
    mcp_server: Optional[Tool] = None, 
    max_workers: int = 4,
    **agent_kwargs
) -> List[Dict[str, Any]]:
    """
    Process multiple queries in parallel using AgentComponent instances with MCP tools.
    
    Args:
        queries (List[str]): List of queries to process
        agent_component_class: The AgentComponent class to use
        mcp_server: MCP server tool to connect to agents
        max_workers (int): Maximum number of parallel workers
        **agent_kwargs: Additional arguments to pass to agent components
        
    Returns:
        List[Dict[str, Any]]: List of results from processing queries
    """
    results = []
    
    # Use ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create futures for each query
        future_to_query = {
            executor.submit(
                _process_single_query_with_agent, 
                query, 
                agent_component_class, 
                mcp_server, 
                **agent_kwargs
            ): query 
            for query in queries
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "query": query,
                    "response": None,
                    "success": False,
                    "error": str(e)
                })
    
    return results


def _process_single_query_with_agent(
    query: str, 
    agent_component_class, 
    mcp_server: Optional[Tool] = None, 
    **agent_kwargs
) -> Dict[str, Any]:
    """
    Process a single query using an AgentComponent instance with MCP tools.
    
    Args:
        query (str): The query to process
        agent_component_class: The AgentComponent class to use
        mcp_server: MCP server tool to connect to the agent
        **agent_kwargs: Additional arguments to pass to the agent component
        
    Returns:
        Dict[str, Any]: Result from processing the query
    """
    # Create agent wrapper
    agent_wrapper = AgentComponentWrapper(
        agent_component_class, 
        mcp_server=mcp_server, 
        **agent_kwargs
    )
    
    # Process the query
    return agent_wrapper.process_query(query)