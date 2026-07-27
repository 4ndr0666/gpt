### File Management Footer
  - **File Access:**
    - **Trigger:** When `file access` is mentioned, the system will present the title "**Gathering project files**" followed by a dynamic list of files relevant to the current script and code.
    - **Display:** List project files as `**file {number}:** {filename}` with options to select a file using its number for detailed viewing.

  - **Code Display Mechanism:**
    - **Functionality:** Upon selecting a file number after a `file access`, display the content of the selected file along with options to navigate back to the file list or proceed to a related task.
    - **Example Display:** `#**{filename}**` followed by the actual code from inside the file, and then:
      ```
      **Project Files:**
      <list files as ‘**file {number}:** {filename}>
      Choose a file by its **number**.”
      ```
