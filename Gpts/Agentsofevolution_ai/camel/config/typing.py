from enum import Enum


class TaskType(Enum):
    AI_SOCIETY = "ai_society"
    CODE = "code"
    MISALIGNMENT = "misalignment"
    TRANSLATION = "translation"
    EVALUATION = "evaluation"
    SOLUTION_EXTRACTION = "solution_extraction"
    AGENTSOFEVOLUTIONAI= "agentsofevolution_ai"
    DEFAULT = "default"


class RoleType(Enum):
    ASSISTANT = "assistant"
    USER = "user"
    CRITIC = "critic"
    EMBODIMENT = "embodiment"
    DEFAULT = "default"
    AGENTSOFEVOLUTIONAI= "AgentTech"
    AGENTSOFEVOLUTIONAI_COUNSELOR = "counselor"
    AGENTSOFEVOLUTIONAI_CEO = "chief executive officer (CEO)"
    AGENTSOFEVOLUTIONAI_CHRO = "chief human resource officer (CHRO)"
    AGENTSOFEVOLUTIONAI_CPO = "chief product officer (CPO)"
    AGENTSOFEVOLUTIONAI_CTO = "chief technology officer (CTO)"
    AGENTSOFEVOLUTIONAI_PROGRAMMER = "programmer"
    AGENTSOFEVOLUTIONAI_REVIEWER = "code reviewer"
    AGENTSOFEVOLUTIONAI_TESTER = "software test engineer"
    AGENTSOFEVOLUTIONAI_CCO = "chief creative officer (CCO)"


class ModelType(Enum):
    GPT_4 = "gpt-4-1106-preview"
    GPT_4_TURBO = "gpt-4-1106-preview"

    STUB = "stub"

    @property
    def value_for_tiktoken(self):
        return self.value if self.name != "STUB" else "gpt-4-1106-preview"


class PhaseType(Enum):
    REFLECTION = "reflection"
    RECRUITING_CHRO = "recruiting CHRO"
    RECRUITING_CPO = "recruiting CPO"
    RECRUITING_CTO = "recruiting CTO"
    DEMAND_ANALYSIS = "demand analysis"
    CHOOSING_LANGUAGE = "choosing language"
    RECRUITING_PROGRAMMER = "recruiting programmer"
    RECRUITING_REVIEWER = "recruiting reviewer"
    RECRUITING_TESTER = "recruiting software test engineer"
    RECRUITING_CCO = "recruiting chief creative officer"
    CODING = "coding"
    CODING_COMPLETION = "coding completion"
    CODING_AUTOMODE = "coding auto mode"
    REVIEWING_COMMENT = "review comment"
    REVIEWING_MODIFICATION = "code modification after reviewing"
    ERROR_SUMMARY = "error summary"
    MODIFICATION = "code modification"
    ART_ELEMENT_ABSTRACTION = "art element abstraction"
    ART_ELEMENT_INTEGRATION = "art element integration"
    CREATING_ENVIRONMENT_DOCUMENT = "environment document"
    CREATING_USER_MANUAL = "user manual"


__all__ = ["TaskType", "RoleType", "ModelType", "PhaseType"]
