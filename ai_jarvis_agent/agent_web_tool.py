import os
import webbrowser
import subprocess
from agents import function_tool

@function_tool
def execute_command(command: str) -> str:
    """
    Execute system-level commands like opening apps or websites.
    Args:
        command (str): The user input text
    Returns:
        str: A status message
    """
    command = command.lower().strip()

    if "notepad" in command:
        os.system("start notepad")
        return "✅ Opening Notepad."

    elif "calculator" in command:
        os.system("start calc")
        return "✅ Opening Calculator."

    elif "chrome" in command or "browser" in command:
        os.system("start chrome")
        return "🌐 Opening Chrome."

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "📺 Opening YouTube."

    elif "google" in command:
        webbrowser.open("https://www.google.com")
        return "🔍 Opening Google."

    elif "file explorer" in command or "explorer" in command:
        os.system("start explorer")
        return "🗂️ Opening File Explorer."

    elif "paint" in command:
        os.system("start mspaint")
        return "🎨 Opening Paint."

    elif "vscode" in command or "visual studio code" in command or "code" in command:
        vs_path = r"C:\Users\theum\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([vs_path])
        return "🧑‍💻 Opening Visual Studio Code."

    return "❌ Sorry, I didn't understand the command."

    

if __name__ == "__main__":
    # Test the tool
    print(execute_command("open code"))
    # print(execute_command("launch calculator"))
    # print(execute_command("start browser"))
    # print(execute_command("open cmd"))