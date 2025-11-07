"""
Base Agent Class for Home Assistant Agent System

This module provides the abstract base class that all HA agents inherit from.
It defines the common interface and shared functionality for all agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum
import logging


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"


class AgentPriority(Enum):
    """Agent recommendation priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AgentResult:
    """Standardized result object returned by all agents"""

    def __init__(
        self,
        success: bool,
        agent_name: str,
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
        recommendations: Optional[List[Dict[str, Any]]] = None,
        errors: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None
    ):
        self.success = success
        self.agent_name = agent_name
        self.message = message
        self.data = data or {}
        self.recommendations = recommendations or []
        self.errors = errors or []
        self.warnings = warnings or []

    def add_recommendation(
        self,
        description: str,
        priority: AgentPriority = AgentPriority.MEDIUM,
        action: Optional[str] = None
    ):
        """Add a recommendation to the result"""
        self.recommendations.append({
            "description": description,
            "priority": priority.value,
            "action": action
        })

    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(error)
        self.success = False

    def add_warning(self, warning: str):
        """Add a warning message"""
        self.warnings.append(warning)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "success": self.success,
            "agent_name": self.agent_name,
            "message": self.message,
            "data": self.data,
            "recommendations": self.recommendations,
            "errors": self.errors,
            "warnings": self.warnings
        }

    def __repr__(self) -> str:
        status = "✅" if self.success else "❌"
        return f"{status} {self.agent_name}: {self.message}"


class BaseAgent(ABC):
    """
    Abstract base class for all Home Assistant agents.

    All agents must implement the execute() method and can optionally
    override other methods for custom behavior.
    """

    def __init__(self, context: Optional['SharedContext'] = None):
        """
        Initialize the agent.

        Args:
            context: SharedContext object for accessing shared state
        """
        self.context = context
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the agent"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    @abstractmethod
    def execute(self, **kwargs) -> AgentResult:
        """
        Execute the agent's main functionality.

        Args:
            **kwargs: Agent-specific parameters

        Returns:
            AgentResult: Standardized result object
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent's display name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the agent does"""
        pass

    @property
    def capabilities(self) -> List[str]:
        """Return a list of agent capabilities"""
        return []

    def validate_inputs(self, **kwargs) -> tuple[bool, Optional[str]]:
        """
        Validate input parameters before execution.

        Args:
            **kwargs: Parameters to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        return True, None

    def can_execute(self) -> tuple[bool, Optional[str]]:
        """
        Check if the agent can execute in current context.

        Returns:
            tuple: (can_execute, reason_if_not)
        """
        if self.status == AgentStatus.RUNNING:
            return False, "Agent is already running"
        return True, None

    def run(self, **kwargs) -> AgentResult:
        """
        Main entry point that handles validation and execution.

        Args:
            **kwargs: Agent-specific parameters

        Returns:
            AgentResult: Execution result
        """
        # Check if agent can execute
        can_exec, reason = self.can_execute()
        if not can_exec:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Cannot execute: {reason}",
                errors=[reason]
            )

        # Validate inputs
        valid, error = self.validate_inputs(**kwargs)
        if not valid:
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Invalid inputs: {error}",
                errors=[error]
            )

        # Execute
        self.status = AgentStatus.RUNNING
        try:
            self.logger.info(f"{self.name} starting execution")
            result = self.execute(**kwargs)
            self.status = AgentStatus.SUCCESS if result.success else AgentStatus.FAILED
            self.logger.info(f"{self.name} finished: {result.message}")
            return result
        except Exception as e:
            self.status = AgentStatus.FAILED
            self.logger.error(f"{self.name} failed with exception: {e}", exc_info=True)
            return AgentResult(
                success=False,
                agent_name=self.name,
                message=f"Execution failed: {str(e)}",
                errors=[str(e)]
            )

    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return self.status

    def reset(self):
        """Reset agent to idle state"""
        self.status = AgentStatus.IDLE


class AgentCapability:
    """
    Decorator to mark agent capabilities.

    Usage:
        @AgentCapability("search_entities")
        def search(self, query: str):
            ...
    """

    def __init__(self, capability_name: str):
        self.capability_name = capability_name

    def __call__(self, func):
        func.is_capability = True
        func.capability_name = self.capability_name
        return func
