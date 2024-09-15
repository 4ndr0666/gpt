import pandas as pd

# Define the master API list as a dataframe
api_list_master = {
    "TID": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19"],
    "Description": [
        "Trigger file access and dynamically list project files",
        "Present file options to select and display using the file number",
        "Skip to a specific phase directly (P1-P6)",
        "Generate and maintain an API list of functions",
        "Real-time project progress review with color-coded visual feedback",
        "Validate decisions using PlantUML-generated flowcharts",
        "Validate flowchart decisions and provide corrections",
        "Submit the revised code and present a comparison with the original",
        "Allow users to prioritize tasks through action ID prompts",
        "Provide context-specific help when an unrecognized command is entered",
        "Modularize file access into a helper function",
        "Modularize file editing into a helper function",
        "Modularize file exporting into a helper function",
        "Add error handling for invalid file access",
        "Add error handling for unsupported file formats",
        "Implement pagination for large file sets",
        "Implement search functionality for file management",
        "Introduce caching for frequently accessed files",
        "Introduce caching for frequently used phase commands"
    ],
    "Associated Functions": [
        "File Manager", "File Manager", "P<1-6>", "API List Creation", "Progress Tracking", 
        "U1", "U2", "Code Submission", "Task Prioritization (A)", "Help System", 
        "File Manager", "File Manager", "File Manager", "Error Handling", "Error Handling", 
        "File Management", "File Management", "File Caching", "Phase Caching"
    ],
    "Status": [
        "Completed", "Completed", "Completed", "Completed", "Completed", "Completed", 
        "Completed", "Planned", "Planned", "Completed", "Planned", "Planned", "Planned", 
        "Planned", "Planned", "Planned", "Planned", "Planned", "Planned"
    ]
}

# Convert the data into a dataframe
df_api_list_master = pd.DataFrame(api_list_master)

# Save the dataframe as a markdown file in the sandbox
api_list_path = '/mnt/data/master_api_list.md'
df_api_list_master.to_markdown(api_list_path, index=False)

# Confirm file has been saved
api_list_path
