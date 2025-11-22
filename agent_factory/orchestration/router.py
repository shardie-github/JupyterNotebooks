"""
Message routing logic for multi-agent orchestration.
"""

from typing import Dict, Any, Optional

from agent_factory.orchestration.graph import AgentGraph, RoutingEdge


class AgentRouter:
    """Route messages between agents in a graph."""
    
    def route(
        self,
        message: Dict[str, Any],
        current_agent_id: str,
        graph: AgentGraph,
    ) -> Optional[str]:
        """
        Determine next agent to route to.
        
        Args:
            message: Current message/context
            current_agent_id: Current agent ID
            graph: Agent graph
        
        Returns:
            Next agent ID, or None if routing should stop
        """
        outgoing_edges = graph.get_outgoing_edges(current_agent_id)
        
        if not outgoing_edges:
            return None
        
        # Simple routing: take first edge if no conditions
        # In production, would evaluate conditions
        for edge in outgoing_edges:
            if not edge.condition:
                return edge.to_agent
            
            # TODO: Evaluate condition expression
            # For now, return first edge
            return edge.to_agent
        
        return None
