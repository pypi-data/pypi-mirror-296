from textwrap import dedent


def make_main_readme_prompt(py_files_content: str) -> str:
    return dedent(f"""You are an expert python developer. Your task is to write an efficient README.md file for the python project whose files are listed below:
                  
                  # Python project files
                  
                  {py_files_content}
                  
                  # Task description
                  Write a README.md file that will make the program easy to read and to maintain for developers.
                  
                  # REAMDE.md
                  """)
