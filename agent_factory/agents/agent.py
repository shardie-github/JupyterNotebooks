"""
Agent class - Core primitive for creating and running AI agents.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

from agent_factory.tools.base import Tool
from agent_factory.runtime.memory import MemoryStore
from agent_factory.core.guardrails import Guardrails
from agent_factory.promptlog import Run, SQLiteStorage
from agent_factory.knowledge import KnowledgePack
import uuid
import time


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AgentConfig:
    """Configuration for an Agent."""
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30  # seconds
    retry_attempts: int = 3
    enable_memory: bool = True
    enable_guardrails: bool = True


@dataclass
class AgentResult:
    """Result from agent execution."""
    output: str
    status: AgentStatus
    tokens_used: int = 0
    execution_time: float = 0.0
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    run_id: Optional[str] = None


@dataclass
class Handoff:
    """Represents a handoff to another agent."""
    to: "Agent"
    context: Dict[str, Any] = field(default_factory=dict)
    reason: Optional[str] = None


class Agent:
    """
    Core Agent class for creating and running AI agents.
    
    Example:
        >>> agent = Agent(
        ...     id="research-assistant",
        ...     name="Research Assistant",
        ...     instructions="You are a research assistant...",
        ...     tools=[web_search_tool, read_file_tool]
        ... )
        >>> result = agent.run("Find information about Python async")
        >>> print(result.output)
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        instructions: str,
        tools: Optional[List[Tool]] = None,
        model: str = "gpt-4o",
        memory: Optional[MemoryStore] = None,
        guardrails: Optional[Guardrails] = None,
        config: Optional[AgentConfig] = None,
        metadata: Optional[Dict[str, Any]] = None,
        knowledge_packs: Optional[List[KnowledgePack]] = None,
        prompt_log_storage: Optional[SQLiteStorage] = None,
    ):
        """
        Initialize an Agent.
        
        Args:
            id: Unique identifier for the agent
            name: Human-readable name
            instructions: System instructions for the agent
            tools: List of tools the agent can use
            model: LLM model to use (default: gpt-4o)
            memory: Memory store for conversation history
            guardrails: Guardrails for safety and validation
            config: Agent configuration
            metadata: Additional metadata
            knowledge_packs: Optional knowledge packs for RAG
            prompt_log_storage: Optional prompt log storage
        """
        self.id = id
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = model
        self.memory = memory
        self.guardrails = guardrails
        self.config = config or AgentConfig()
        self.metadata = metadata or {}
        self.knowledge_packs = knowledge_packs or []
        self.prompt_log_storage = prompt_log_storage
        self._status = AgentStatus.IDLE
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent."""
        if tool not in self.tools:
            self.tools.append(tool)
    
    def remove_tool(self, tool_id: str) -> None:
        """Remove a tool by ID."""
        self.tools = [t for t in self.tools if t.id != tool_id]
    
    def attach_knowledge_pack(self, pack: KnowledgePack) -> None:
        """Attach a knowledge pack to the agent."""
        if pack not in self.knowledge_packs:
            self.knowledge_packs.append(pack)
    
    def update_instructions(self, instructions: str) -> None:
        """Update agent instructions."""
        self.instructions = instructions
    
    def run(
        self,
        input_text: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Run the agent with given input.
        
        Args:
            input_text: User input/question
            session_id: Optional session ID for memory
            context: Optional context dictionary
            
        Returns:
            AgentResult with output and metadata
        """
        start_time = time.time()
        run_id = str(uuid.uuid4())
        
        try:
            self._status = AgentStatus.RUNNING
            
            # Apply guardrails if enabled
            if self.guardrails:
                guardrail_result = self.guardrails.validate_input(input_text)
                if not guardrail_result.allowed:
                    result = AgentResult(
                        output="",
                        status=AgentStatus.ERROR,
                        error=f"Input blocked by guardrails: {guardrail_result.reason}",
                        run_id=run_id,
                    )
                    self._log_run(run_id, input_text, result, start_time)
                    return result
            
            # Load memory if available
            memory_context = {}
            if self.memory and session_id:
                memory_context = self.memory.get_context(session_id)
            
            # Load knowledge pack context if available
            knowledge_context = {}
            if self.knowledge_packs:
                knowledge_context = self._get_knowledge_context(input_text)
            
            # Prepare context
            full_context = {
                **(context or {}),
                **memory_context,
                **knowledge_context,
            }
            
            # Execute agent (this would integrate with OpenAI SDK)
            output = self._execute_agent(input_text, full_context)
            
            # Apply output guardrails
            if self.guardrails:
                guardrail_result = self.guardrails.validate_output(output)
                if not guardrail_result.allowed:
                    output = f"[Output modified by guardrails: {guardrail_result.reason}]"
            
            # Save to memory
            if self.memory and session_id:
                self.memory.save_interaction(session_id, input_text, output)
            
            execution_time = time.time() - start_time
            
            self._status = AgentStatus.COMPLETED
            
            result = AgentResult(
                output=output,
                status=AgentStatus.COMPLETED,
                execution_time=execution_time,
                metadata={"model": self.model},
                run_id=run_id,
            )
            
            # Log to prompt log
            self._log_run(run_id, input_text, result, start_time)
            
            return result
            
        except Exception as e:
            self._status = AgentStatus.ERROR
            result = AgentResult(
                output="",
                status=AgentStatus.ERROR,
                error=str(e),
                run_id=run_id,
            )
            self._log_run(run_id, input_text, result, start_time)
            return result
    
    def _get_knowledge_context(self, query: str) -> Dict[str, Any]:
        """Get context from knowledge packs."""
        context = {}
        for pack in self.knowledge_packs:
            # TODO: Implement actual retrieval from knowledge packs
            # For now, placeholder
            context[f"{pack.id}_context"] = f"Knowledge from {pack.name}"
        return context
    
    def _log_run(
        self,
        run_id: str,
        input_text: str,
        result: AgentResult,
        start_time: float,
    ) -> None:
        """Log run to prompt log storage."""
        if not self.prompt_log_storage:
            return
        
        try:
            from agent_factory.promptlog.model import Run as RunModel
            
            run = RunModel(
                run_id=run_id,
                agent_id=self.id,
                inputs={"input": input_text},
                outputs={"output": result.output},
                status="success" if result.status == AgentStatus.COMPLETED else "error",
                execution_time=result.execution_time,
                tokens_used=result.tokens_used,
                cost_estimate=0.0,  # Would calculate from tokens
            )
            self.prompt_log_storage.save_run(run)
        except Exception:
            # Silently fail if logging fails
            pass
    
    def _execute_agent(self, input_text: str, context: Dict[str, Any]) -> str:
        """
        Execute the agent using the underlying LLM SDK.
        
        Args:
            input_text: User input text
            context: Context dictionary
            
        Returns:
            Agent output text
            
        Raises:
            RuntimeError: If execution fails
        """
        try:
            from agent_factory.integrations.openai_client import OpenAIAgentClient
            
            client = OpenAIAgentClient()
            result = client.run_agent(
                instructions=self.instructions,
                input_text=input_text,
                model=self.model,
                tools=self.tools,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                context=context,
            )
            
            return result.get("output", "")
        except ImportError:
            # Fallback if OpenAI SDK not available
            return f"[Agent {self.name} would process: {input_text}]"
        except Exception as e:
            from agent_factory.core.exceptions import AgentExecutionError
            raise AgentExecutionError(f"Agent execution failed: {str(e)}") from e
    
    def handoff(
        self,
        to: "Agent",
        context: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None,
    ) -> Handoff:
        """
        Create a handoff to another agent.
        
        Args:
            to: Target agent
            context: Context to pass to target agent
            reason: Reason for handoff
            
        Returns:
            Handoff object
        """
        return Handoff(
            to=to,
            context=context or {},
            reason=reason,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize agent to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "instructions": self.instructions,
            "model": self.model,
            "tools": [tool.id for tool in self.tools],
            "knowledge_packs": [pack.id for pack in self.knowledge_packs],
            "config": {
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
            },
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], tools_registry: Optional[Dict[str, Tool]] = None) -> "Agent":
        """Deserialize agent from dictionary."""
        tools = []
        if tools_registry:
            tools = [tools_registry[tid] for tid in data.get("tools", []) if tid in tools_registry]
        
        config = AgentConfig(**data.get("config", {}))
        
        return cls(
            id=data["id"],
            name=data["name"],
            instructions=data["instructions"],
            tools=tools,
            model=data.get("model", "gpt-4o"),
            config=config,
            metadata=data.get("metadata", {}),
        )
