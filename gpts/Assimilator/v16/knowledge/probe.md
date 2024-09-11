# **Probe Directive**

### **Objective**:
Ensure a thorough probing, confirmation, and updating process for all variables in the provided configuration or script. The goal is to align the script with user requirements before finalization, ensuring accuracy and readiness for execution.

---

### **Instructions**:

---

#### **1. Initialization**:
   - **Action**: Parse all variables and their current values from the provided configuration or script. Present them in a structured format (e.g., a table) for the user to review.
   
   - **Purpose**: Establish a clear reference point for all variables and their default values. This provides transparency, allowing the user to see the current state of the configuration before any modifications are made.
   
   - **Output Example**:
     ```
     | Variable Name | Current Value | Description |
     |---------------|---------------|-------------|
     | var1          | 100           | Description of var1 |
     | var2          | False         | Description of var2 |
     ```

---

#### **2. Probing**:
   - **Action**: Sequentially present each variable to the user for review, with detailed explanations of each variable’s role and purpose in the script or configuration. Include common value examples where applicable to guide the user.
   
   - **Purpose**: Ensure the user fully understands the importance of each variable and how it affects the overall functionality of the script or system. This step helps avoid misconfiguration or incorrect assumptions.

   - **Example Workflow**:
     ```
     Variable: var1 (current value: 100)
     Purpose: This variable controls the system's timeout setting. Common values: 100, 200, 300.
     
     Would you like to modify this value? (yes/no):
     If yes, please enter the new value: [User input]
     ```

---

#### **3. Confirmation**:
   - **Action**: After probing, explicitly confirm the user-provided or modified values for each variable. Summarize all the confirmed values in a list or table for easy review.
   
   - **Purpose**: Validate that the user has approved the final values for all variables before proceeding. This step ensures clarity and prevents errors caused by overlooked changes or misinterpretations.

   - **Output Example**:
     ```
     Confirmed Variable Values:
     | Variable Name | New Value     |
     |---------------|---------------|
     | var1          | 200           |
     | var2          | True          |
     ```
   
   - **Error Handling**: If any values are invalid or conflict with existing system rules (e.g., incorrect data types or ranges), alert the user and prompt them to provide a valid value.

---

#### **4. Updating**:
   - **Action**: Update the configuration or script with the confirmed values. Ensure each revision is saved incrementally to avoid data loss and maintain a version history.
   
   - **Purpose**: Systematically replace the initial variable values with the newly confirmed ones. This process should be done safely to ensure no overwrites or mistakes occur during the update.
   
   - **Best Practices**:
     - Maintain a backup of the original configuration or script before any changes are made.
     - Save incremental versions of the updated configuration to ensure easy rollback if needed.

   - **Example**:
     ```
     Original: var1 = 100
     Updated: var1 = 200
     ```

---

#### **5. Final Review**:
   - **Action**: Present the fully updated configuration or script to the user for a final review before finalization. This should include all confirmed variable values and any structural or logical changes made to the script.
   
   - **Purpose**: Allow the user to make any last-minute adjustments and ensure the configuration meets their exact specifications before finalization.
   
   - **Output Example**:
     ```
     Finalized Configuration:
     var1 = 200
     var2 = True
     ```
   
   - **Error Handling**: Ensure that the script passes all syntax and logic checks. If any errors are detected, return to the user with a summary of the issues and request further modifications or confirmations.

---

#### **6. Finalization**:
   - **Action**: Finalize the configuration or script with the confirmed values. Ensure the script is fully tested and ready for execution, following all user requirements and preferences.
   
   - **Purpose**: Lock in all changes and prepare the script or configuration for production use. Perform final checks to ensure idempotency, correctness, and readiness for deployment.

   - **Checklist for Finalization**:
     - Ensure all variables are set to their confirmed values.
     - Perform a final syntax and logic check.
     - Test the script to confirm it runs without errors and meets the user’s requirements.
     - Generate a version-controlled final output file.

---

### **Final Submission**:

#### **Action**:
   - Present the finalized configuration or script for user approval. This should include a summary of all changes, including the initial and final variable values.
   
#### **Purpose**:
   - Ensure that the final product is free from errors and ready for production. Once approved, the script should be stored securely for future use, with a version history maintained for reference.

---

### **Best Practices for Probing and Finalization**:
- **Idempotency**: Ensure that the script is idempotent, meaning it does not perform unnecessary actions if the desired state has already been achieved.
- **Error-Free Execution**: Perform rigorous testing to ensure that the script runs without errors under all expected conditions.
- **Security Considerations**: Validate that all variables are safe and do not introduce vulnerabilities (e.g., ensure proper sanitization of user inputs).
- **User-Friendly Feedback**: Provide clear, concise feedback to the user at each step of the process, making it easy for them to follow along and confirm their decisions.
