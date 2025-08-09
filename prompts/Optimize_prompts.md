#!/usr/bin/env python
# coding: utf-8

# # Optimize Prompts
#
# Crafting effective prompts is a critical skill when working with AI models. Even experienced users can inadvertently introduce contradictions, ambiguities, or inconsistencies that lead to suboptimal results. The system demonstrated here helps identify and fix common issues, resulting in more reliable and effective prompts.
#
# The optimization process uses a multi-agent approach with specialized AI agents collaborating to analyze and rewrite prompts. The system automatically identifies and addresses several types of common issues:
#
# - **Contradictions** in the prompt instructions
# - Missing or unclear **format specifications**
# - **Inconsistencies** between the prompt and few-shot examples
#
# ---
#
# **Objective**: This cookbook demonstrates best practices for using Agents SDK together with Evals to build an early version of OpenAI's prompt optimization system. You can optimize your prompt using this code or use the optimizer [in our playground!](https://platform.openai.com/playground/prompts)
#
#
#
#
#
#
#
#
# Ask ChatGPT
#
#
# **Cookbook Structure**
# This notebook follows this structure:
#
# - [Step 1. System Overview](#1-system-overview) - Learn how the prompt optimization system works
# - [Step 2. Data Models](#2-data-models) - Understand the data structures used by the system
# - [Step 3. Defining the Agents](#3-defining-the-agents) - Look at agents that analyze and improve prompts
# - [Step 4. Evaluations](#4-using-evaluations-to-arrive-at-these-agents) - Use Evals to verify our agent model choice and instructions
# - [Step 5. Run Optimization Workflow](#4-run-optimization-workflow) - See how the workflow hands off the prompts
# - [Step 6. Examples](#5-examples) - Explore real-world examples of prompt optimization
#
# **Prerequisites**
# - The `openai` Python package
# - The `openai-agents` package
# - An OpenAI API key set as `OPENAI_API_KEY` in your environment variables

# ## 1. System Overview
#
# The prompt optimization system uses a collaborative multi-agent approach to analyze and improve prompts. Each agent specializes in either detecting or rewriting a specific type of issue:
#
# 1. **Dev-Contradiction-Checker**: Scans the prompt for logical contradictions or impossible instructions, like "only use positive numbers" and "include negative examples" in the same prompt.
#
# 2. **Format-Checker**: Identifies when a prompt expects structured output (like JSON, CSV, or Markdown) but fails to clearly specify the exact format requirements. This agent ensures that all necessary fields, data types, and formatting rules are explicitly defined.
#
# 3. **Few-Shot-Consistency-Checker**: Examines example conversations to ensure that the assistant's responses actually follow the rules specified in the prompt. This catches mismatches between what the prompt requires and what the examples demonstrate.
#
# 4. **Dev-Rewriter**: After issues are identified, this agent rewrites the prompt to resolve contradictions and clarify format specifications while preserving the original intent.
#
# 5. **Few-Shot-Rewriter**: Updates inconsistent example responses to align with the rules in the prompt, ensuring all examples properly comply with the new developer prompt.
#
# By working together, these agents can systematically identify and fix issues in prompts.

# In[ ]:


# Import required modules
from openai import AsyncOpenAI
import asyncio
import json
import os
from enum import Enum
from typing import Any, List, Dict
from pydantic import BaseModel, Field
from agents import Agent, Runner, set_default_openai_client, trace

openai_client: AsyncOpenAI | None = None

def _get_openai_client() -> AsyncOpenAI:
    global openai_client
    if openai_client is None:
        openai_client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
        )
    return openai_client

set_default_openai_client(_get_openai_client())


# ## 2. Data Models
#
# To facilitate structured communication between agents, the system uses Pydantic models to define the expected format for inputs and outputs. These Pydantic models help validate data and ensure consistency throughout the workflow.
#
# The data models include:
#
# 1. **Role** - An enumeration for message roles (user/assistant)
# 2. **ChatMessage** - Represents a single message in a conversation
# 3. **Issues** - Base model for reporting detected issues
# 4. **FewShotIssues** - Extended model that adds rewrite suggestions for example messages
# 5. **MessagesOutput** - Contains optimized conversation messages
# 6. **DevRewriteOutput** - Contains the improved developer prompt
#
# Using Pydantic allows the system to validate that all data conforms to the expected format at each step of the process.

# In[32]:


class Role(str, Enum):
    """Role enum for chat messages."""
    user = "user"
    assistant = "assistant"

class ChatMessage(BaseModel):
    """Single chat message used in few-shot examples."""
    role: Role
    content: str

class Issues(BaseModel):
    """Structured output returned by checkers."""
    has_issues: bool
    issues: List[str]

    @classmethod
    def no_issues(cls) -> "Issues":
        return cls(has_issues=False, issues=[])

class FewShotIssues(Issues):
    """Output for few-shot contradiction detector including optional rewrite suggestions."""
    rewrite_suggestions: List[str] = Field(default_factory=list)

    @classmethod
    def no_issues(cls) -> "FewShotIssues":
        return cls(has_issues=False, issues=[], rewrite_suggestions=[])

class MessagesOutput(BaseModel):
    """Structured output returned by `rewrite_messages_agent`."""

    messages: list[ChatMessage]


class DevRewriteOutput(BaseModel):
    """Rewriter returns the cleaned-up developer prompt."""

    new_developer_message: str


# ## 3. Defining the Agents
#
# In this section, we create specialized AI agents using the `Agent` class from the `openai-agents` package. Looking at these agent definitions reveals several best practices for creating effective AI instructions:
#
# ### Best Practices in Agent Instructions
#
# 1. **Clear Scope Definition**: Each agent has a narrowly defined purpose with explicit boundaries. For example, the contradiction checker focuses only on "genuine self-contradictions" and explicitly states that "overlaps or redundancies are not contradictions."
#
# 2. **Step-by-Step Process**: Instructions provide a clear methodology, like how the format checker first categorizes the task before analyzing format requirements.
#
# 3. **Explicit Definitions**: Key terms are defined precisely to avoid ambiguity. The few-shot consistency checker includes a detailed "Compliance Rubric" explaining exactly what constitutes compliance.
#
# 4. **Boundary Setting**: Instructions specify what the agent should NOT do. The few-shot checker explicitly lists what's "Out-of-scope" to prevent over-flagging issues.
#
# 5. **Structured Output Requirements**: Each agent has a strictly defined output format with examples, ensuring consistency in the optimization pipeline.
#
# These principles create reliable, focused agents that work effectively together in the optimization system. Below we see the complete agent definitions with their detailed instructions.

# In[ ]:


dev_contradiction_checker = Agent(
    name="contradiction_detector",
    model="gpt-4.1",
    output_type=Issues,
    instructions="""
    You are **Dev-Contradiction-Checker**.

    Goal
    Detect *genuine* self-contradictions or impossibilities **inside** the developer prompt supplied in the variable `DEVELOPER_MESSAGE`.

    Definitions
    • A contradiction = two clauses that cannot both be followed.
    • Overlaps or redundancies in the DEVELOPER_MESSAGE are *not* contradictions.

    What you MUST do
    1. Compare every imperative / prohibition against all others.
    2. List at most FIVE contradictions (each as ONE bullet).
    3. If no contradiction exists, say so.

    Output format (**strict JSON**)
    Return **only** an object that matches the `Issues` schema:

    ```json
    {"has_issues": <bool>,
    "issues": [
        "<bullet 1>",
        "<bullet 2>"
    ]
    }
    - has_issues = true IFF the issues array is non-empty.
    - Do not add extra keys, comments or markdown.
""",
)
format_checker = Agent(
    name="format_checker",
    model="gpt-4.1",
    output_type=Issues,
    instructions="""
    You are Format-Checker.

    Task
    Decide whether the developer prompt requires a structured output (JSON/CSV/XML/Markdown table, etc.).
    If so, flag any missing or unclear aspects of that format.

    Steps
    Categorise the task as:
    a. "conversation_only", or
    b. "structured_output_required".

    For case (b):
    - Point out absent fields, ambiguous data types, unspecified ordering, or missing error-handling.

    Do NOT invent issues if unsure. be a little bit more conservative in flagging format issues

    Output format
    Return strictly-valid JSON following the Issues schema:

    {
    "has_issues": <bool>,
    "issues": ["<desc 1>", "..."]
    }
    Maximum five issues. No extra keys or text.
""",
)
fewshot_consistency_checker = Agent(
    name="fewshot_consistency_checker",
    model="gpt-4.1",
    output_type=FewShotIssues,
    instructions="""
    You are FewShot-Consistency-Checker.

    Goal
    Find conflicts between the DEVELOPER_MESSAGE rules and the accompanying **assistant** examples.

    USER_EXAMPLES:      <all user lines>          # context only
    ASSISTANT_EXAMPLES: <all assistant lines>     # to be evaluated

    Method
    Extract key constraints from DEVELOPER_MESSAGE:
    - Tone / style
    - Forbidden or mandated content
    - Output format requirements

    Compliance Rubric - read carefully
    Evaluate only what the developer message makes explicit.

    Objective constraints you must check when present:
    - Required output type syntax (e.g., "JSON object", "single sentence", "subject line").
    - Hard limits (length ≤ N chars, language required to be English, forbidden words, etc.).
    - Mandatory tokens or fields the developer explicitly names.

    Out-of-scope (DO NOT FLAG):
    - Whether the reply "sounds generic", "repeats the prompt", or "fully reflects the user's request" - unless the developer text explicitly demands those qualities.
    - Creative style, marketing quality, or depth of content unless stated.
    - Minor stylistic choices (capitalisation, punctuation) that do not violate an explicit rule.

    Pass/Fail rule
    - If an assistant reply satisfies all objective constraints, it is compliant, even if you personally find it bland or loosely related.
    - Only record an issue when a concrete, quoted rule is broken.

    Empty assistant list ⇒ immediately return has_issues=false.

    For each assistant example:
    - USER_EXAMPLES are for context only; never use them to judge compliance.
    - Judge each assistant reply solely against the explicit constraints you extracted from the developer message.
    - If a reply breaks a specific, quoted rule, add a line explaining which rule it breaks.
    - Optionally, suggest a rewrite in one short sentence (add to rewrite_suggestions).
    - If you are uncertain, do not flag an issue.
    - Be conservative—uncertain or ambiguous cases are not issues.

    be a little bit more conservative in flagging few shot contradiction issues
    Output format
    Return JSON matching FewShotIssues:

    {
    "has_issues": <bool>,
    "issues": ["<explanation 1>", "..."],
    "rewrite_suggestions": ["<suggestion 1>", "..."] // may be []
    }
    List max five items for both arrays.
    Provide empty arrays when none.
    No markdown, no extra keys.
    """,
)
dev_rewriter = Agent(
    name="dev_rewriter",
    model="gpt-4.1",
    output_type=DevRewriteOutput,
    instructions="""
    You are Dev-Rewriter.

    You receive:
    - ORIGINAL_DEVELOPER_MESSAGE
    - CONTRADICTION_ISSUES (may be empty)
    - FORMAT_ISSUES (may be empty)

    Rewrite rules
    Preserve the original intent and capabilities.

    Resolve each contradiction:
    - Keep the clause that preserves the message intent; remove/merge the conflicting one.

    If FORMAT_ISSUES is non-empty:
    - Append a new section titled ## Output Format that clearly defines the schema or gives an explicit example.

    Do NOT change few-shot examples.

    Do NOT add new policies or scope.

    Output format (strict JSON)
    {
    "new_developer_message": "<full rewritten text>"
    }
    No other keys, no markdown.
""",
)
fewshot_rewriter = Agent(
    name="fewshot_rewriter",
    model="gpt-4.1",
    output_type=MessagesOutput,
    instructions="""
    You are FewShot-Rewriter.

    Input payload
    - NEW_DEVELOPER_MESSAGE (already optimized)
    - ORIGINAL_MESSAGES (list of user/assistant dicts)
    - FEW_SHOT_ISSUES (non-empty)

    Task
    Regenerate only the assistant parts that were flagged.
    User messages must remain identical.
    Every regenerated assistant reply MUST comply with NEW_DEVELOPER_MESSAGE.

    After regenerating each assistant reply, verify:
    - It matches NEW_DEVELOPER_MESSAGE. ENSURE THAT THIS IS TRUE.

    Output format
    Return strict JSON that matches the MessagesOutput schema:

    {
    "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
        ]
    }
    Guidelines
    - Preserve original ordering and total count.
    - If a message was unproblematic, copy it unchanged.
    """,
)


# ## 4. Using Evaluations to Arrive at These Agents
#
# Let's see how we used OpenAI Evals to tune agent instructions and pick the correct model to use. In order to do so we constructed a set of golden examples: each one contains original messages (developer message + user/assistant message) and the changes our optimization workflow should make. Here are two example of golden pairs that we used:

# ```
# [
#   {
#     "focus": "contradiction_issues",
#     "input_payload": {
#       "developer_message": "Always answer in **English**.\nNunca respondas en inglés.",
#       "messages": [
#         {
#           "role": "user",
#           "content": "¿Qué hora es?"
#         }
#       ]
#     },
#     "golden_output": {
#       "changes": true,
#       "new_developer_message": "Always answer **in English**.",
#       "new_messages": [
#         {
#           "role": "user",
#           "content": "¿Qué hora es?"
#         }
#       ],
#       "contradiction_issues": "Developer message simultaneously insists on English and forbids it.",
#       "few_shot_contradiction_issues": "",
#       "format_issues": "",
#       "general_improvements": ""
#     }
#   },
#   {
#     "focus": "few_shot_contradiction_issues",
#     "input_payload": {
#       "developer_message": "Respond with **only 'yes' or 'no'** – no explanations.",
#       "messages": [
#         {
#           "role": "user",
#           "content": "Is the sky blue?"
#         },
#         {
#           "role": "assistant",
#           "content": "Yes, because wavelengths …"
#         },
#         {
#           "role": "user",
#           "content": "Is water wet?"
#         },
#         {
#           "role": "assistant",
#           "content": "Yes."
#         }
#       ]
#     },
#     "golden_output": {
#       "changes": true,
#       "new_developer_message": "Respond with **only** the single word \"yes\" or \"no\".",
#       "new_messages": [
#         {
#           "role": "user",
#           "content": "Is the sky blue?"
#         },
#         {
#           "role": "assistant",
#           "content": "yes"
#         },
#         {
#           "role": "user",
#           "content": "Is water wet?"
#         },
#         {
#           "role": "assistant",
#           "content": "yes"
#         }
#       ],
#       "contradiction_issues": "",
#       "few_shot_contradiction_issues": "Assistant examples include explanations despite instruction not to.",
#       "format_issues": "",
#       "general_improvements": ""
#     }
#   }
# ]
# ```

# From these 20 hand labelled golden outputs which cover a range of contradiction issues, few shot issues, format issues, no issues, or a combination of issues, we built a python string check grader to verify two things: whether an issue was detected for each golden pair and whether the detected issue matched the expected one. From this signal, we tuned the agent instructions and which model to use to maximize our accuracy across this evaluation. We landed on the 4.1 model as a balance between accuracy, cost, and speed. The specific prompts we used also follow the 4.1 prompting guide. As you can see, we achieve the correct labels on all 20 golden outputs: identifying the right issues and avoiding false positives.

# ![Accuracy for the golden set](../images/optimizepromptfig1.png)

# ![Evaluation for the golden set](../images/optimizepromptfig2.png)

# ## 5. Run Optimization Workflow
#
# Let's dive into how the optimization system actually works end to end. The core workflow consists of multiple runs of the agents in parallel to efficiently process and optimize prompts.

# In[ ]:


def _normalize_messages(messages: List[Any]) -> List[Dict[str, str]]:
    """Convert list of pydantic message models to JSON-serializable dicts."""
    result = []
    for m in messages:
        if hasattr(m, "model_dump"):
            result.append(m.model_dump())
        elif isinstance(m, dict) and "role" in m and "content" in m:
            result.append({"role": str(m["role"]), "content": str(m["content"])})
    return result

async def optimize_prompt_parallel(
    developer_message: str,
    messages: List["ChatMessage"],
) -> Dict[str, Any]:
    """
    Runs contradiction, format, and few-shot checkers in parallel,
    then rewrites the prompt/examples if needed.
    Returns a unified dict suitable for an API or endpoint.
    """

    with trace("optimize_prompt_workflow"):
        # 1. Run all checkers in parallel (contradiction, format, fewshot if there are examples)
        tasks = [
            Runner.run(dev_contradiction_checker, developer_message),
            Runner.run(format_checker, developer_message),
        ]
        if messages:
            fs_input = {
                "DEVELOPER_MESSAGE": developer_message,
                "USER_EXAMPLES": [m.content for m in messages if m.role == "user"],
                "ASSISTANT_EXAMPLES": [m.content for m in messages if m.role == "assistant"],
            }
            tasks.append(Runner.run(fewshot_consistency_checker, json.dumps(fs_input)))

        results = await asyncio.gather(*tasks)

        # Unpack results
        cd_issues: Issues = results[0].final_output
        fi_issues: Issues = results[1].final_output
        fs_issues: FewShotIssues = results[2].final_output if messages else FewShotIssues.no_issues()

        # 3. Rewrites as needed
        final_prompt = developer_message
        if cd_issues.has_issues or fi_issues.has_issues:
            pr_input = {
                "ORIGINAL_DEVELOPER_MESSAGE": developer_message,
                "CONTRADICTION_ISSUES": cd_issues.model_dump(),
                "FORMAT_ISSUES": fi_issues.model_dump(),
            }
            pr_res = await Runner.run(dev_rewriter, json.dumps(pr_input))
            final_prompt = pr_res.final_output.new_developer_message

        final_messages: list[ChatMessage] | list[dict[str, str]] = messages
        if fs_issues.has_issues:
            mr_input = {
                "NEW_DEVELOPER_MESSAGE": final_prompt,
                "ORIGINAL_MESSAGES": _normalize_messages(messages),
                "FEW_SHOT_ISSUES": fs_issues.model_dump(),
            }
            mr_res = await Runner.run(fewshot_rewriter, json.dumps(mr_input))
            final_messages = mr_res.final_output.messages

        return {
            "changes": True,
            "new_developer_message": final_prompt,
            "new_messages": _normalize_messages(final_messages),
            "contradiction_issues": "\n".join(cd_issues.issues),
            "few_shot_contradiction_issues": "\n".join(fs_issues.issues),
            "format_issues": "\n".join(fi_issues.issues),
        }


# ![Trace for the workflow](../images/optimizepromptfig3.png)

# ### Understanding the Optimization Workflow
#
# The `optimize_prompt_parallel` function implements a workflow to maximize efficiency through parallelization:
#
# 1. **Parallel Issue Detection**: The first phase runs all checker agents simultaneously:
#    - `dev_contradiction_checker` searches for logical contradictions in the prompt
#    - `format_checker` looks for unclear format specifications
#    - `fewshot_consistency_checker` (if examples exist) checks for mismatches between the prompt and examples
#
# After the parallel checking phase, the workflow handles dependencies carefully:
#
# 2. **Prompt Rewriting (Conditional)**: The `dev_rewriter` agent only runs if contradiction or format issues were detected. This agent depends on the outputs from:
#    - `dev_contradiction_checker` (the `cd_issues` variable)
#    - `format_checker` (the `fi_issues` variable)
#
# 3. **Example Rewriting (Conditional)**: The `fewshot_rewriter` agent only runs if example inconsistencies were detected. This agent depends on:
#    - The rewritten prompt (must be done after prompt rewriting)
#    - The original messages
#    - The few-shot issues (the `fs_issues` variable)
#

# ## 6. Examples
#
# Let's see the optimization system in action with some practical examples.

# ### Example 1: Fixing Contradictions

# In[28]:


async def example_contradiction():
    # A prompt with contradictory instructions
    prompt = """Quick-Start Card — Product Parser

Goal
Digest raw HTML of an e-commerce product detail page and emit **concise, minified JSON** describing the item.

**Required fields:**
name | brand | sku | price.value | price.currency | images[] | sizes[] | materials[] | care_instructions | features[]

**Extraction priority:**
1. schema.org/JSON-LD blocks
2. <meta> & microdata tags
3. Visible DOM fallback (class hints: "product-name", "price")

** Rules:**
- If *any* required field is missing, short-circuit with: `{"error": "FIELD_MISSING:<field>"}`.
- Prices: Numeric with dot decimal; strip non-digits (e.g., "1.299,00 EUR" → 1299.00 + "EUR").
- Deduplicate images differing only by query string. Keep ≤10 best-res.
- Sizes: Ensure unit tag ("EU", "US") and ascending sort.
- Materials: Title-case and collapse synonyms (e.g., "polyester 100%" → "Polyester").

**Sample skeleton (minified):**
```json
{"name":"","brand":"","sku":"","price":{"value":0,"currency":"USD"},"images":[""],"sizes":[],"materials":[],"care_instructions":"","features":[]}
Note: It is acceptable to output null for any missing field instead of an error ###"""

    result = await optimize_prompt_parallel(prompt, [])

    # Display the results
    if result["contradiction_issues"]:
        print("Contradiction issues:")
        print(result["contradiction_issues"])
        print()

    print("Optimized prompt:")
    print(result["new_developer_message"])

# Run the example
await example_contradiction()


# This demonstrates how the system can detect and resolve critical contradictions that could lead to inconsistent outputs or confusion for the model.

# ### Example 2: Fixing Inconsistencies Between Prompt and Few-Shot Examples
#

# In[29]:


async def example_fewshot_fix():
    prompt = "Respond **only** with JSON using keys `city` (string) and `population` (integer)."

    messages = [
        {"role": "user", "content": "Largest US city?"},
        {"role": "assistant", "content": "New York City"},
        {"role": "user", "content": "Largest UK city?"},
        {"role": "assistant", "content": "{\"city\":\"London\",\"population\":9541000}"}
    ]


    print("Few-shot examples before optimization:")
    print(f"User: {messages[0]['content']}")
    print(f"Assistant: {messages[1]['content']}")
    print(f"User: {messages[2]['content']}")
    print(f"Assistant: {messages[3]['content']}")
    print()

    # Call the optimization API
    result = await optimize_prompt_parallel(prompt, [ChatMessage(**m) for m in messages])

    # Display the results
    if result["few_shot_contradiction_issues"]:
        print("Inconsistency found:", result["few_shot_contradiction_issues"])
        print()

    # Show the optimized few-shot examples
    optimized_messages = result["new_messages"]
    print("Few-shot examples after optimization:")
    print(f"User: {optimized_messages[0]['content']}")
    print(f"Assistant: {optimized_messages[1]['content']}")
    print(f"User: {optimized_messages[2]['content']}")
    print(f"Assistant: {optimized_messages[3]['content']}")

# Run the example
await example_fewshot_fix()


# This is particularly important because few-shot examples have a strong influence on how models respond. If examples don't follow the stated rules, the model may learn to ignore those rules in favor of mimicking the examples. By ensuring consistency between the prompt instructions and examples, the optimization system creats a more reliable prompt.

# ### Example 3: Clarifying Formats in a Longer Prompt

# In[30]:


async def example_format_issue():
    # A prompt with unclear or inconsistent formatting instructions
    prompt = """Task → Translate dense patent claims into 200-word lay summaries with a glossary.

Operating Steps:
1. Split the claim at semicolons, "wherein", or numbered sub-clauses.
2. For each chunk:
   a) Identify its purpose.
   b) Replace technical nouns with everyday analogies.
   c) Keep quantitative limits intact (e.g., "≥150 C").
3. Flag uncommon science terms with asterisks, and later define them.
4. Re-assemble into a flowing paragraph; do **not** broaden or narrow the claim’s scope.
5. Omit boilerplate if its removal does not alter legal meaning.

Output should follow a Markdown template:
- A summary section.
- A glossary section with the marked terms and their definitions.

Corner Cases:
- If the claim is over 5 kB, respond with CLAIM_TOO_LARGE.
- If claim text is already plain English, skip glossary and state no complex terms detected.

Remember: You are *not* providing legal advice—this is for internal comprehension only."""

    # Call the optimization API to check for format issues
    result = await optimize_prompt_parallel(prompt, [])

    # Display the results
    if result.get("format_issues"):
        print("Format issues found:", result["format_issues"])
        print()

    print("Optimized prompt:")
    print(result["new_developer_message"])

# Run the example
await example_format_issue()


# This example highlights how the format checker identifies and resolves ambiguous format specifications. The prompt requested a Markdown output and the optimization flow significantly improved these format specifications.
