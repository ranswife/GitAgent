import git
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Basic tools
@tool
def now_date_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
@tool
def quit_conversation():
    """Quit the conversation."""
    exit("Conversation ended by Agent.")

# Middleware to handle tool errors
@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

# Git tools
def git_init(dir: str) -> str:
    """Initialize a new Git repository."""
    repo = git.Repo.init(dir)
    return f"Initialized empty Git repository in {repo.git_dir}"

@tool
def git_status(dir: str) -> str:
    """Get the status of the Git repository."""
    repo = git.Repo(dir)
    return repo.git.status()

@tool
def git_add(dir: str, file: str) -> str:
    """Add a file to the staging area."""
    repo = git.Repo(dir)
    repo.git.add(file)
    return f"Added {file} to staging area."

@tool
def git_commit(dir: str, message: str) -> str:
    """Commit changes to the repository."""
    repo = git.Repo(dir)
    repo.index.commit(message)
    return f"Committed changes with message: {message}"

@tool
def git_log(dir: str) -> str:
    """Get the commit log of the repository."""
    repo = git.Repo(dir)
    return repo.git.log()

@tool
def git_branch(dir: str, branch_name: str) -> str:
    """Create a new branch."""
    repo = git.Repo(dir)
    repo.git.branch(branch_name)
    return f"Created new branch: {branch_name}"

@tool
def git_checkout(dir: str, branch_name: str) -> str:
    """Checkout a branch."""
    repo = git.Repo(dir)
    repo.git.checkout(branch_name)
    return f"Checked out branch: {branch_name}"

@tool
def git_merge(dir: str, branch_name: str) -> str:
    """Merge a branch into the current branch."""
    repo = git.Repo(dir)
    repo.git.merge(branch_name)
    return f"Merged branch {branch_name} into current branch."

@tool
def git_push(dir: str, remote: str = 'origin', branch: str = 'main') -> str:
    """Push changes to a remote repository."""
    repo = git.Repo(dir)
    repo.git.push(remote, branch)
    return f"Pushed changes to {remote}/{branch}."

@tool
def git_pull(dir: str, remote: str = 'origin', branch: str = 'main') -> str:
    """Pull changes from a remote repository."""
    repo = git.Repo(dir)
    repo.git.pull(remote, branch)
    return f"Pulled changes from {remote}/{branch}."

@tool
def git_clone(repo_url: str, dir: str) -> str:
    """Clone a remote repository."""
    git.Repo.clone_from(repo_url, dir)
    return f"Cloned repository from {repo_url} to {dir}."

@tool
def git_diff(dir: str) -> str:
    """Get the diff of the repository."""
    repo = git.Repo(dir)
    diff = repo.git.diff()
    return diff

@tool
def git_reset(dir: str, file: str) -> str:
    """Reset a file in the working directory."""
    repo = git.Repo(dir)
    repo.git.reset(file)
    return f"Reset {file} in the working directory."

# Files tools
@tool
def file_read(file_path: str) -> str:
    """Read the contents of a file."""
    with open(file_path, 'r') as file:
        content = file.read()
    return content

@tool
def file_write(file_path: str, content: str) -> str:
    """Write content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)
    return f"Wrote content to {file_path}."

@tool
def tree(dir_path: str) -> str:
    """List the directory structure."""
    structure = []
    for root, dirs, files in os.walk(dir_path):
        level = root.replace(dir_path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{subindent}{f}")
    result = '\n'.join(structure)
    return result

# Main function
def main():

    # Initialize the language model
    model = ChatOpenAI(
        model = os.getenv("DEFAULT_MODEL"),
        base_url = os.getenv("BASE_URL"),
    )

    # Create the agent with git tools
    git_agent = create_agent(
        tools = [
            # Basic tools
            now_date_time,
            quit_conversation,
            # Git tools
            git_init,
            git_status,
            git_add,
            git_commit,
            git_log,
            git_branch,
            git_checkout,
            git_merge,
            git_push,
            git_pull,
            git_clone,
            git_diff,
            git_reset,
            # Files tools
            file_read,
            file_write,
            tree,
        ],
        model = model,
        middleware = [handle_tool_errors]
    )

    # Chat history
    chat_history = [
        {
            "role": "system", 
            "content": os.getenv("SYSTEM_PROMPT")
        }
    ]

    # Interactive loop
    print("Welcome to the Git Agent! Type your commands below.")
    print("Type 'exit' to quit.")
    print("")

    model_response = ""

    while True:
        # Get user input
        print("")
        user_prompt = input(">> ")
        print("")

        # Append user message to chat history
        chat_history.append({"role": "user", "content": user_prompt})
        chat_history.append({"role": "assistant", "content": model_response})

        model_response = ""

        # Stream response from the agent
        for chunk, metadata in git_agent.stream(
            {
                "messages": chat_history
            },
            stream_mode = "messages",
        ):
            if chunk.content:
                print(chunk.content, end = "", flush = True)
                model_response = model_response + chunk.content
            

if __name__ == "__main__":
    main()
