## **API Phase Directive**

### **Objective**:
The goal is to follow a systematic, phase-based progression for API development, with strict standards for code quality, reproducibility, and error minimization. Each phase requires approval before proceeding to the next, ensuring that tasks are thoroughly reviewed and enhanced.

---

### **Systematic Progression**:

---

### **Phase 1: API List**

- **Objective**: Create an organized API list to guide the development process, with tasks associated with functions and their statuses.

#### API List:
1. **Version 1.0**: Write a comprehensive API list for all functions in the script in a Markdown table format. The list serves as the foundation for systematic enhancement and refinement.
   
   **Example API List Format**:
   | **API Name** | **Function**  | **Task Description**        | **Version** | **Status**   |
   |--------------|---------------|-----------------------------|-------------|--------------|
   | API Function | Function Name  | Description of function task| 1.0         | Planned      |

#### Task IDs (TIDs):
2. **Required Format**: Each function task must be associated with a Task ID (TID). The TID tracking system will be used to maintain clarity and status progression for each task. This table must contain:
   - **Task ID**: A unique identifier.
   - **Description**: Detailed explanation of the task.
   - **Associated Function**: The function to which the task relates.
   - **Status**: The status of the task (Planned, In Progress, Completed).

---

### **Phase 2: Project Plan**

#### Integrity Guidelines:
1. **Feedback Audit**: Once the initial API list is presented, you will receive feedback based on an audit. The feedback will include Task IDs (TIDs) and a description of the issues identified.
   
2. **Task Iteration**: Based on the feedback, engage in iterative feedback loops to update the project plan. The status of the corresponding TIDs will be adjusted as necessary (Planned, In Progress, or Completed).

#### Example Task Update Process:
- TID status will be updated according to the audit findings, ensuring that each issue is addressed before proceeding.

---

### **Phase 3: Procedure**

#### Systematic Implementation:
1. **Refactoring and Task Resolution**: Address each TID point-by-point, ensuring all tasks are resolved accurately and comprehensively.
   - Refactor code to meet task objectives.
   - Implement solutions based on the audit findings.

2. **Real-Time Task Updates**: Keep the API list updated as tasks are completed. Ensure all changes are reflected in real-time, maintaining task synchronization. This helps track progress and maintain transparency in the project.

#### Example:
   - **Task Status Change**: Update tasks from "In Progress" to "Completed" as they are resolved, keeping a detailed log for approval.

---

### **Phase 4: Submission 1**

#### Requirements for Approval:
1. **Comparative Analysis**: Once all TIDs are marked as "Completed", prepare the revised submission in a Markdown table. Present the changes made side by side with the current function to enhance clarity.
   - Include a column for the benefits and improvements made during revision.

2. **Proposal for Changes**: Present a detailed explanation of the changes made, explaining how the revisions improved the code, along with potential use cases for each update.
   - **Intended Use Cases**: Explain how the revision enhances functionality and aligns with user requirements.

3. **Decision**: The feedback provided will either approve the proposal or highlight discrepancies in the form of additional TIDs with correlating issue descriptions. Use this feedback to update the API list and begin work on **Version 1.1** of the API list.

---

### **Phase 5: Refinement**

#### Execution Post-Submission 1:
1. **TID Resolution and Refinement**: Make adjustments based on the feedback provided. Ensure that each new TID is carefully tracked and resolved.
   - Update the API list in real-time to reflect the current state of tasks, keeping the project synchronized with any changes made.
   - Refine the API and ensure completeness by the end of this phase.

---

### **Phase 6: Cycles**

#### Conditional Loop:
1. **Compliance Check**: Once Phase 5 is complete, begin a new cycle starting from Phase 4. This cycle ensures continuous improvement and error mitigation.
   - Version control is updated to 1.2, with each cycle introducing improvements based on the TID review process.
   - Present the updated script and API list for review and testing, ensuring continuous progression.

---

### **Urgent Overrides**

#### Priority:
1. **Immediate Action Task IDs**: In case of critical errors or urgent tasks, use the Immediate Action Task IDs protocol. This overrides other tasks and focuses solely on resolving high-priority issues.
   - TIDs related to urgent actions will be updated to "Corrections Needed" status, requiring immediate resolution.
   - Once all urgent tasks are completed, the system will resume the previous phase progression.

2. **Protocol for Immediate Action**:
   - Update the API list to reflect urgent tasks and prioritize their completion.
   - Each Immediate Action TID must be resolved before returning to the standard project phase.

---

### **Final Phase Requirements**

#### Production-Ready Script:
1. **No Simplified Examples**: Ensure all examples and code segments demonstrate full functionality with the complexity appropriate for the task.
   
2. **Contextual Integration**: The script should integrate seamlessly into existing frameworks or applications. This includes ensuring compatibility with API versions, dependencies, and external libraries.

3. **Idempotency**: Ensure that the script is idempotent by implementing checks to avoid unnecessary operations if the desired state is already achieved. This prevents redundancy and enhances stability.

4. **Complete and Polished Logic**: Every function and logic block must be fully developed and tested, with no incomplete sections. Ensure proper error handling for all edge cases.

5. **Syntax and Logic Checks**: Conduct thorough testing for syntax and logic errors. Prevent issues caused by incorrect implementation, unhandled exceptions, or faulty logic.

6. **Security Considerations**: Apply security best practices, including input sanitization and vulnerability checks. The script must be protected from potential security risks while maintaining its full functionality.
