import os
import re
from abc import ABC, abstractmethod
from knowledge import RolePlaying, ChatMessage, TaskType
from chatdev.chat_env import ChatEnv
from chatdev.statistics import get_info

class Phase(ABC):
    def __init__(self, assistant_role_name, user_role_name, phase_prompt, role_prompts, phase_name, model_type):
        """
        Initialize a phase of the chat chain.

        Args:
            assistant_role_name (str): Role name of the assistant in this phase.
            user_role_name (str): Role name of the user starting the chat in this phase.
            phase_prompt (str): The prompt for this phase.
            role_prompts (dict): Prompts for all roles involved in the phase.
            phase_name (str): The name of this phase.
            model_type (ModelType): The model type to be used in this phase.
        """
        self.assistant_role_name = assistant_role_name
        self.user_role_name = user_role_name
        self.phase_prompt = phase_prompt
        self.phase_name = phase_name
        self.model_type = model_type
        self.assistant_role_prompt = role_prompts.get(assistant_role_name, "")
        self.user_role_prompt = role_prompts.get(user_role_name, "")
        self.phase_env = {}
        self.seminar_conclusion = None
        self.max_retries = 3
        self.reflection_prompt = (
            "Here is a conversation between {assistant_role_name} and {user_role_name}: "
            "{conversations} {question}"
        )

    @abstractmethod
    def update_phase_env(self, chat_env):
        """
        Updates the phase-specific environment settings.

        Args:
            chat_env (ChatEnv): The global chat environment.
        """
        pass

    @abstractmethod
    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment based on phase conclusions.

        Args:
            chat_env (ChatEnv): The global chat environment.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        pass

    def execute(self, chat_env, chat_turn_limit, need_reflect) -> ChatEnv:
        """
        Executes the chatting in this phase.

        Args:
            chat_env (ChatEnv): The global chat environment.
            chat_turn_limit (int): The turn limit for each chat.
            need_reflect (bool): Indicates if reflection is needed.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        self.update_phase_env(chat_env)
        # Chatting logic and environment updates will be covered in the next segments.
        return chat_env

    def chatting(self, chat_env, task_prompt, assistant_role_name, user_role_name, phase_prompt, phase_name,
                 assistant_role_prompt, user_role_prompt, task_type=TaskType.AGENTSOFEVOLUTION_AI, need_reflect=False,
                 with_task_specify=False, memory=None, placeholders=None, chat_turn_limit=10) -> str:
        """
        Facilitates the chatting interaction within the phase.

        Args:
            chat_env (ChatEnv): The global chat environment.
            task_prompt (str): The task prompt for building the software.
            assistant_role_name (str): The role receiving the chat.
            user_role_name (str): The role starting the chat.
            phase_prompt (str): The prompt of the phase.
            phase_name (str): The name of the phase.
            assistant_role_prompt (str): The prompt of the assistant role.
            user_role_prompt (str): The prompt of the user role.
            task_type (TaskType): The type of task.
            need_reflect (bool): Indicates if reflection is needed.
            with_task_specify (bool): Specifies if task details should be included.
        memory (dict): The chat memory for continuity.
        placeholders (dict): Placeholders for dynamic prompt content.
        chat_turn_limit (int): The maximum number of chat turns.

    Returns:
        str: The conclusion of the chat phase.
    """
    if placeholders is None:
        placeholders = {}
    assert 1 <= chat_turn_limit <= 100, "Chat turn limit must be between 1 and 100."

    if not chat_env.exist_employee(assistant_role_name) or not chat_env.exist_employee(user_role_name):
        raise ValueError(f"Either {assistant_role_name} or {user_role_name} is not recruited in ChatEnv.")

    role_play_session = RolePlaying(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        assistant_role_prompt=assistant_role_prompt,
        user_role_prompt=user_role_prompt,
        task_prompt=task_prompt,
        task_type=task_type,
        with_task_specify=with_task_specify,
        memory=memory,
        model_type=self.model_type,
        background_prompt=chat_env.config.background_prompt
    )

    seminar_conclusion = ""
    for i in range(chat_turn_limit):
        assistant_response, user_response = role_play_session.step()
        if assistant_response.info or user_response.info:
            seminar_conclusion = "<INFO> " + (assistant_response.content or user_response.content)
            break
        if assistant_response.terminated or user_response.terminated:
            break

    if need_reflect and not seminar_conclusion:
        seminar_conclusion = self.self_reflection(role_play_session, chat_env)

    return seminar_conclusion

def self_reflection(self, role_play_session, chat_env):
    """
    Conducts a reflection based on the chat session.

    Args:
        role_play_session (RolePlaying): The session of role play.
        chat_env (ChatEnv): The global chat environment.

    Returns:
        str: The conclusion derived from reflecting on the chat session.
    """
    # Reflection logic based on the role_play_session and chat_env.
    # Implementation specifics depend on phase requirements.
    return "Reflection content based on the phase and interactions."

def self_reflection(self, role_play_session, chat_env):
    """
    Conducts a self-reflection based on the chat session, generating a conclusion or actionable insight.

    Args:
        role_play_session (RolePlaying): The session of role play containing the chat history.
        chat_env (ChatEnv): The global chat environment providing context for the reflection.

    Returns:
        str: The conclusion derived from the reflection, specific to the phase's context.
    """
    # Compile messages from the role play session for reflection
    messages = self.compile_messages_for_reflection(role_play_session)

    # Generate a reflection question based on the phase's context
    question = self.generate_reflection_question(self.phase_name)

    # Conduct the reflection using a tailored prompt
    reflected_content = self.conduct_reflection(
        chat_env=chat_env,
        conversations=messages,
        question=question,
        role_play_session=role_play_session
    )

    # Process the reflected content based on phase-specific logic
    return self.process_reflected_content(reflected_content, self.phase_name)

def compile_messages_for_reflection(self, role_play_session):
    """
    Compiles messages from the role play session for reflection.

    Args:
        role_play_session (RolePlaying): The role play session to compile messages from.

    Returns:
        str: Compiled messages formatted for reflection.
    """
    messages = role_play_session.assistant_agent.stored_messages if len(
        role_play_session.assistant_agent.stored_messages) >= len(
        role_play_session.user_agent.stored_messages) else role_play_session.user_agent.stored_messages
    return "\n\n".join(f"{message.role_name}: {message.content.replace('\n\n', '\n')}" for message in messages)

def generate_reflection_question(self, phase_name):
    """
    Generates a reflection question based on the phase's context.

    Args:
        phase_name (str): The name of the phase to generate a question for.

    Returns:
        str: A reflection question tailored to the phase's context.
    """
    if "recruiting" in phase_name:
        return "Answer their final discussed conclusion (Yes or No)."
    elif phase_name == "DemandAnalysis":
        return "Answer their final product modality."
    elif phase_name == "LanguageChoose":
        return "Conclude the programming language being discussed."
    elif phase_name == "EnvironmentDoc":
        return "Write a requirements.txt file based on the discussed codes."
    else:
        raise ValueError(f"Reflection for phase '{phase_name}' is not defined.")

def conduct_reflection(self, chat_env, conversations, question, role_play_session):
    """
    Conducts the reflection using a tailored prompt, incorporating the compiled messages and generated question.

    Args:
        chat_env (ChatEnv): The global chat environment.
        conversations (str): Compiled messages for reflection.
        question (str): The generated reflection question.
        role_play_session (RolePlaying): The role play session for context.

    Returns:
        str: The content derived from conducting the reflection.
    """
    reflection_prompt = self.reflection_prompt.format(conversations=conversations, question=question)
    # Reflection logic to process the prompt and derive a conclusion.
    # This might involve further interaction or analysis.
    return "Reflected content based on analysis."

def process_reflected_content(self, reflected_content, phase_name):
    """
    Processes the reflected content based on phase-specific logic.

    Args:
        reflected_content (str): The content derived from the reflection.
        phase_name (str): The name of the phase for context.

    Returns:
        str: Processed reflection content or decision based on the phase's context.
    """
    if "recruiting" in phase_name:
        return "Yes" if "Yes".lower() in reflected_content.lower() else "No"
    return reflected_content = \
                          self.chatting(chat_env=chat_env,
                          task_prompt=task_prompt,
                          assistant_role_name="Chief Executive Officer",
                          user_role_name="Counselor",
                          phase_prompt=self.reflection_prompt,
                          phase_name="Reflection",
                          assistant_role_prompt=self.ceo_prompt,
                          user_role_prompt=self.counselor_prompt,
                          placeholders={"conversations": messages, "question": question},
                          need_reflect=False,
                          memory=chat_env.memory,
                          chat_turn_limit=1,

        if "recruiting" in phase_name:
            if "Yes".lower() in reflected_content.lower():
                return "Yes"
            return "No"
        else:
            return reflected_content

    @abstractmethod
    def update_phase_env(self, chat_env):
        """
        update self.phase_env (if needed) using chat_env, then the chatting will use self.phase_env to follow the context and fill placeholders in phase prompt
        must be implemented in customized phase
        the usual format is just like:
        ```
            self.phase_env.update({key:chat_env[key]})
        ```
        Args:
            chat_env: global chat chain environment

        Returns: None

        """
        pass

    @abstractmethod
    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        update chan_env based on the results of self.execute, which is self.seminar_conclusion
        must be implemented in customized phase
        the usual format is just like:
        ```
            chat_env.xxx = some_func_for_postprocess(self.seminar_conclusion)
        ```
        Args:
            chat_env:global chat chain environment

        Returns:
            chat_env: updated global chat chain environment

        """
        pass

    def execute_reflection(self, chat_env):
        """
        Executes the reflection process for the phase, extracting and processing
        the reflected content based on the phase's context.

        Args:
            chat_env (ChatEnv): The global chat environment.

        Returns:
            The processed reflected content or decision based on the phase's context.
        """
        # Compile messages for reflection and generate reflection question
        messages = self.compile_messages_for_reflection()
        question = self.generate_reflection_question(self.phase_name)

        # Conduct reflection and process the outcome
        reflected_content = self.conduct_reflection(
            chat_env=chat_env,
            conversations=messages,
            question=question
        )

        # Handle special cases for "recruiting" phase or return general reflected content
        if "recruiting" in self.phase_name:
            return "Yes" if "Yes".lower() in reflected_content.lower() else "No"
        else:
            return reflected_content

    # Implementation of other methods (compile_messages_for_reflection, generate_reflection_question, conduct_reflection)...
Implementing LanguageChoose Phase:
After concluding the reflection process, the LanguageChoose phase specifically deals with selecting the programming language for the project.

class LanguageChoose(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # This method prepares the phase environment for the language choice interaction.
        # It can utilize outcomes from previous phases, like `DemandAnalysis`, reflected in `chat_env`.
        super().update_phase_env(chat_env)  # Calls the base implementation if any generic setup is needed.

    def update_chat_env(self, chat_env) -> ChatEnv:
        # After concluding the language choice, this method updates the global chat environment
        # with the selected programming language.
        if self.seminar_conclusion:
            # Extracting and updating the programming language choice.
            language = self.seminar_conclusion.split("<INFO>")[-1].strip()
            chat_env.env_dict['programming_language'] = language
        return chat_env

class DemandAnalysis(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        """
        Prepares the phase environment specific to Demand Analysis.

        For DemandAnalysis, the environment preparation could involve setting up initial
        conditions or parameters that reflect the user's requirements and the project's scope
        as understood at this early stage.

        Args:
            chat_env (ChatEnv): The global chat environment providing context.
        """
        # Example: Prepare environment variables specific to demand analysis
        # This could include setting up initial ideas, project scope, or any
        # other relevant information extracted from `chat_env`.
        self.phase_env.update({
            "initial_ideas": chat_env.env_dict.get('ideas', 'Discuss project ideas'),
            "project_scope": chat_env.env_dict.get('scope', 'Define the scope of the project')
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment based on the conclusions from the Demand Analysis phase.

        This typically involves capturing and formalizing the user's demands, such as the desired
        product modality, and any specific requirements identified during this phase.

        Args:
            chat_env (ChatEnv): The global chat environment to be updated.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        if self.seminar_conclusion:
            # Extract the product modality or any key conclusions made during this phase
            modality = self.seminar_conclusion.split("<INFO>")[-1].strip().lower()
            chat_env.env_dict['product_modality'] = modality

            # Additional processing or updates based on phase outcomes can be handled here
            # For example, setting flags or counters based on the analysis or decisions made
            chat_env.env_dict['demand_analysis_completed'] = True

        return chat_env

class LanguageChoose(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        """
        Prepares the environment for the language choice phase by extracting relevant
        information from the global chat environment to be used in making the language decision.

        Args:
            chat_env (ChatEnv): The global chat environment containing project details.
        """
        # Update the phase-specific environment with details needed for language selection.
        # This includes the task description, project modality, and any specific ideas that
        # might influence the choice of programming language.
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "description": chat_env.env_dict.get('task_description', 'No description provided.'),
            "modality": chat_env.env_dict.get('modality', 'default'),  # Default to a generic modality if not specified
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.')
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment with the chosen programming language based on the
        discussions and conclusions of this phase.

        Args:
            chat_env (ChatEnv): The global chat environment to be updated.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        # Extract the programming language from the seminar conclusion.
        # If a specific language is identified with "<INFO>", use that;
        # otherwise, default to Python if no explicit choice is made.
        language = "Python"  # Default to Python if no language is specified or concluded.
        if "<INFO>" in self.seminar_conclusion:
            language = self.seminar_conclusion.split("<INFO>")[-1].strip().lower()
        elif self.seminar_conclusion:
            language = self.seminar_conclusion.strip().lower()

        chat_env.env_dict['language'] = language
        return chat_env

class Coding(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        """
        Prepares the environment for the coding phase, considering the project's requirements
        for a GUI and the selected programming language.

        Args:
            chat_env (ChatEnv): The global chat environment containing details about the project.
        """
        # Determine the need for a GUI and prepare guidance for selecting a GUI framework.
        gui_description = ("The software should be equipped with a graphical user interface (GUI). "
                           "Please choose a GUI framework appropriate for the selected programming language, "
                           f"{chat_env.env_dict.get('language', 'Python')}.")
        if not chat_env.config.get('gui_design', False):
            gui_description = ""

        # Update the phase environment with project details and GUI requirements.
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "description": chat_env.env_dict.get('task_description', 'No description provided.'),
            "modality": chat_env.env_dict.get('modality', 'default_modality'),
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Default to Python if not specified
            "gui_description": gui_description
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment after the coding phase, incorporating the developed code
        and any GUI components into the project's documentation.

        Args:
            chat_env (ChatEnv): The global chat environment to be updated.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        # Process and validate the coding outcomes, including code and potential GUI components.
        if self.seminar_conclusion:
            # Here, `update_codes` is a placeholder for the actual logic that processes the coding outcomes.
            chat_env.update_codes(self.seminar_conclusion)
            if len(chat_env.codes.codebooks.keys()) == 0:
                raise ValueError("Coding phase concluded without valid code outputs.")

            # If coding is successfully concluded, update the project documentation accordingly.
            chat_env.rewrite_codes("Finish Coding")
            chat_env.env_dict['coding_status'] = "Completed"
            # Optionally, provide a summary of the software's current state.
            chat_env.env_dict['software_info'] = get_info(chat_env.env_dict['directory'])

        return chat_env


class ArtDesign(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env = {"task": chat_env.env_dict['task_prompt'],
                          "description": chat_env.env_dict['task_description'],
                          "language": chat_env.env_dict['language'],
                          "codes": chat_env.get_codes()}

    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.proposed_images = chat_env.get_proposed_images_from_message(self.seminar_conclusion)

            "**[Software Info]**:\n\n {}".format(get_info(chat_env.env_dict['directory'], self.log_filepath))
        return chat_env

class ArtIntegration(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        """
        Prepares the environment for integrating art and GUI components into the software,
        pulling necessary information from the global chat environment.

        Args:
            chat_env (ChatEnv): The global chat environment containing project details and art assets.
        """
        # Aggregate information about the codes and proposed images for integration.
        self.phase_env = {
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Defaulting to Python if not specified
            "codes": chat_env.get_codes(),  # Assuming this method retrieves all relevant code snippets for integration
            "images": "\n".join(f"{filename}: {description}"
                                for filename, description in sorted(chat_env.proposed_images.items()))
        }

    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment to reflect the integration of art assets into the project,
        including updating codes and potentially generating image assets from codes.

        Args:
            chat_env (ChatEnv): The global chat environment to be updated.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        # Process the outcomes of the art integration phase, updating codes and handling image assets.
        if self.seminar_conclusion:
            # Here, `update_codes` processes the updated code snippets that include art integration.
            chat_env.update_codes(self.seminar_conclusion)
            # Optionally, generate image assets based on codes if the project requires.
            # Assuming `generate_images_from_codes` is a method that handles this process.
            # chat_env.generate_images_from_codes()

            # Update the project documentation to reflect the completion of art integration.
            chat_env.rewrite_codes("Finish Art Integration")
            chat_env.env_dict['art_integration_status'] = "Completed"
            # Provide a summary of the software's current state, including integrated art assets.
            chat_env.env_dict['software_info'] = get_info(chat_env.env_dict['directory'])

        return chat_env

class CodeComplete(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        """
        Identifies any unimplemented files or functionalities within the project's codebase,
        preparing for a comprehensive review to ensure code completeness.

        Args:
            chat_env (ChatEnv): The global chat environment containing project details and code snippets.
        """
        # Initialize or update the phase environment with project-specific details.
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "modality": chat_env.env_dict.get('modality', 'default_modality'),
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Default to Python if not specified
            "codes": chat_env.get_codes(),  # Retrieves all code snippets for review
            "unimplemented_file": ""  # Placeholder for identifying unimplemented parts
        })

        # Example logic to identify an unimplemented file (simplified for illustration purposes).
        for filename, code_details in self.phase_env["codes"].items():
            if "pass" in code_details['content']:  # Simplified check for unimplemented parts
                self.phase_env["unimplemented_file"] = filename
                break

    def update_chat_env(self, chat_env) -> ChatEnv:
        """
        Updates the global chat environment following the code completion review,
        ensuring that the project's codebase is fully implemented and functional.

        Args:
            chat_env (ChatEnv): The global chat environment to be updated.

        Returns:
            ChatEnv: The updated global chat environment.
        """
        # Update the code snippets based on the review outcomes from this phase.
        if self.seminar_conclusion:
            chat_env.update_codes(self.seminar_conclusion)
            if len(chat_env.codes.codebooks.keys()) == 0:
                raise ValueError("CodeComplete phase concluded without valid code outputs.")

            # Mark the coding phase as complete and update the project documentation.
            chat_env.rewrite_codes("Code Complete")
            chat_env.env_dict['coding_status'] = "Completed"
            chat_env.env_dict['software_info'] = get_info(chat_env.env_dict['directory'])

        return chat_env



class CodeReviewComment(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update(
            {"task": chat_env.env_dict['task_prompt'],
             "modality": chat_env.env_dict['modality'],
             "ideas": chat_env.env_dict['ideas'],
             "language": chat_env.env_dict['language'],
             "codes": chat_env.get_codes(),
             "images": ", ".join(chat_env.incorporated_images)})

    def update_chat_env(self, chat_env) -> ChatEnv:
        chat_env.env_dict['review_comments'] = self.seminar_conclusion
        return chat_env


class CodeReviewModification(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "ideas": chat_env.env_dict['ideas'],
                               "language": chat_env.env_dict['language'],
                               "codes": chat_env.get_codes(),
                               "comments": chat_env.env_dict['review_comments']})

def update_chat_env(self, chat_env) -> ChatEnv:
        # Process the code modifications and validate them.
        chat_env.update_codes(self.seminar_conclusion)

        # Ensure the modifications address the feedback adequately.
        if "```".lower() in self.seminar_conclusion.lower():
            chat_env.rewrite_codes("Review Modification Completed")
        else:
            raise ValueError("Modifications did not address all review comments adequately.")

        return chat_env

class CodeReviewHuman(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"task": chat_env.env_dict['task_prompt'],
                               "modality": chat_env.env_dict['modality'],
                               "ideas": chat_env.env_dict['ideas'],
                               "language": chat_env.env_dict['language'],
                               "codes": chat_env.get_codes()})

    def update_chat_env(self, chat_env) -> ChatEnv:
        if "```".lower() in self.seminar_conclusion.lower():
            chat_env.update_codes(self.seminar_conclusion)
            chat_env.rewrite_codes("Human Review #" + str(self.phase_env["cycle_index"]) + " Finished")
                "**[Software Info]**:\n\n {}".format(get_info(chat_env.env_dict['directory'], self.log_filepath))
        return chat_env

    def execute(self, chat_env, chat_turn_limit, need_reflect):
    # Update the phase-specific environment with details from the global environment.
    self.update_phase_env(chat_env)

    print(f"**[Human-Agent-Interaction]**\n\n"
          f"Now you can participate in the development of the software!\n"
          f"The task is: {chat_env.env_dict['task_prompt']}\n"
          f"Please input your feedback (in multiple lines). It can be a bug report or a new feature requirement.\n"
          f"You are currently in the #{self.phase_env['cycle_index']} human feedback with a total of {self.phase_env['cycle_num']} feedbacks\n"
          f"Type 'end' on a separate line to submit.\n"
          f"You can type \"Exit\" to quit this mode at any time.")

    provided_comments = []
    while True:
        user_input = input(">>>>>> ")
        if user_input.strip().lower() == "end":
            break
        if user_input.strip().lower() == "exit":
            provided_comments = ["exit"]
            break
        provided_comments.append(user_input)

        # Compile the collected comments into a single string.
    self.phase_env["comments"] = '\n'.join(provided_comments)
    print(f"**[User Provided Comments]**\n\n"
          f"In the #{self.phase_env['cycle_index']} of total {self.phase_env['cycle_num']} feedback cycles: \n\n"
          f"{self.phase_env['comments']}")

    if self.phase_env["comments"].strip().lower() == "exit":
        # If the user decides to exit, return the current state of chat_env without changes.
        return chat_env

        # Process the feedback and integrate it into the project.
    # This is a placeholder for actual logic that might involve parsing the feedback,
    # identifying actionable items, and updating the project's code or documentation accordingly.
    self.seminar_conclusion = self.process_feedback(chat_env, self.phase_env["comments"])

    # Update the global environment with changes made during this phase.
    chat_env = self.update_chat_env(chat_env)
    return chat_env


def process_feedback(self, chat_env, feedback):
    """
    Processes the provided feedback and integrates it into the project.

    Args:
        chat_env (ChatEnv): The global chat environment.
        feedback (str): The compiled feedback from the user.

    Returns:
        The outcome of processing the feedback, which could be a conclusion or summary.
    """
    # Placeholder for feedback processing logic. This might involve updating code, tasks,
    # or project documentation based on the feedback.
    # Example:
    # outcome = update_project_based_on_feedback(chat_env, feedback)
    outcome = "Feedback processed successfully."
    return outcome

class TestErrorSummary(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # Simulate the generation of images from codes if applicable
        chat_env.generate_images_from_codes()
        # Simulate checking for existing bugs in the codebase
        exist_bugs_flag, test_reports = chat_env.exist_bugs()
        # Update the phase environment with the test reports and bug flags
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "modality": chat_env.env_dict.get('modality', 'default_modality'),
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Default to Python if not specified
            "codes": chat_env.get_codes(),
            "test_reports": test_reports,
            "exist_bugs_flag": exist_bugs_flag
        })
        print(f"**[Test Reports]**:\n\n{test_reports}")

    def update_chat_env(self, chat_env) -> ChatEnv:
        # Update the global chat environment with the error summary and test reports
        chat_env.env_dict['error_summary'] = self.seminar_conclusion
        chat_env.env_dict['test_reports'] = self.phase_env['test_reports']
        return chat_env

class TestModification(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # Update the phase environment with details required for making test modifications
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt'),
            "modality": chat_env.env_dict.get('modality'),
            "ideas": chat_env.env_dict.get('ideas'),
            "language": chat_env.env_dict.get('language'),
            "codes": chat_env.get_codes(),  # Assuming this retrieves all relevant code snippets
            "test_reports": chat_env.env_dict.get('test_reports'),
            "error_summary": chat_env.env_dict.get('error_summary')
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        # Update the codes based on modifications and validate them
        chat_env.update_codes(self.seminar_conclusion)
        # If modifications were successful, rewrite the codes and update the software info
        chat_env.rewrite_codes(f"Test Modification Completed: Cycle #{self.phase_env['cycle_index']}")
        print(f"**[Software Info]**:\n\n{get_info(chat_env.env_dict['directory'])}")
        return chat_env

class EnvironmentDoc(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # Update the phase environment with project details and codes for documentation
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt'),
            "modality": chat_env.env_dict.get('modality'),
            "ideas": chat_env.env_dict.get('ideas'),
            "language": chat_env.env_dict.get('language'),
            "codes": chat_env.get_codes()
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        # Document the project requirements based on the environment setup and codes
        chat_env._update_requirements(self.seminar_conclusion)
        chat_env.rewrite_requirements()
        print(f"**[Software Info]**:\n\n{get_info(chat_env.env_dict['directory'])}")
        return chat_env

class EnvironmentDoc(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # Gather necessary information from the global environment for documenting.
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "modality": chat_env.env_dict.get('modality', 'default_modality'),
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Default to Python if not specified
            "codes": chat_env.get_codes()  # Retrieves code snippets for documentation reference
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        # Document the environment setup and requirements based on the current project state.
        chat_env._update_requirements(self.seminar_conclusion)
        chat_env.rewrite_requirements()
        print(f"**[Software Info]**:\n\n{get_info(chat_env.env_dict['directory'])}")
        return chat_env

class Manual(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        # Prepare the environment with all necessary details for manual documentation.
        self.phase_env.update({
            "task": chat_env.env_dict.get('task_prompt', 'No task prompt provided.'),
            "modality": chat_env.env_dict.get('modality', 'default_modality'),
            "ideas": chat_env.env_dict.get('ideas', 'No specific ideas provided.'),
            "language": chat_env.env_dict.get('language', 'Python'),  # Assuming Python as a default
            "codes": chat_env.get_codes(),  # Code snippets for reference
            "requirements": chat_env.get_requirements()  # Project requirements for setup
        })

    def update_chat_env(self, chat_env) -> ChatEnv:
        # Update the project documentation with the user manual.
        chat_env._update_manuals(self.seminar_conclusion)
        chat_env.rewrite_manuals()
        return chat_env
