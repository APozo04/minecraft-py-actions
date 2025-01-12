[![codecov](https://codecov.io/gh/APozo04/minecraft-py-actions/graph/badge.svg?token=HKLF1MQHO3)](https://codecov.io/gh/APozo04/minecraft-py-actions)

# Minecraft Agent Framework

This project is part of a university assignment at the **Universitat Rovira i Virgili** in Tarragona. The goal of this task is to develop a Python framework that enables the creation and execution of Python-coded agents in a shared Minecraft server. These agents are able to interact with the Minecraft world by moving, building, destroying blocks, and interacting with the chat.

## Features
- **Functional Programming**: The scripts demonstrate the use of functional programming paradigms in Python. Different examples are provided to showcase how functional techniques can be used to write cleaner and more efficient code.
- **Reflective Programming**: The codebase also incorporates examples of reflective programming, allowing dynamic analysis and manipulation of objects and methods in the game, making the system highly flexible and extensible.
  
## Example Agents
Here are some examples of agents that can be created using this framework:
- **InsultBot**: This bot insults players in the chat to bother users.
- **TNTBot**: This agent places TNT and causes explosions, adding an element of chaos to the game.
- **OracleBot**: This bot answers questions in the chat using a predefined list of answers or even integrates with AI models like ChatGPT.

## Minecraft Server Setup

To run the Minecraft server and interact with the agent scripts, follow these steps:

1. **Download and Install Minecraft Server**:
   - Download the appropriate server package from the [Adventures in Minecraft GitHub repository for Linux/macOS](https://github.com/AdventuresInMinecraft/AdventuresInMinecraft-Linux) or the [Adventures in Minecraft GitHub repository for Windows](https://github.com/AdventuresInMinecraft/AdventuresInMinecraft-PC).
   - Ensure you have **Java 8** installed, as the server requires this version of Java to run correctly. If you have a newer version, you might need to install Java 8 or configure the server to use it.
   - Make sure you are using the Minecraft version specified in the repository (most likely **Minecraft 1.12**) to ensure compatibility with the server and the Python scripts.

2. **Set the Repository Location**:
   - Place the folder of this repository (`minecraft-py-actions-main`) inside the `Adventures in Minecraft` folder as shown in the image below:
     ![Repository Placement](./img/minecraft-py-actions-ubication.png)

3. **Start the Server**:
   - Open the `startServer.bat` (Windows) or `startServer.sh` (Linux/macOS) file from the Minecraft server directory to start the server. 
   - After a few seconds, the server will be up and running, and you can interact with it in the game.

4. **Install Python Dependencies**:
   - You need to install the required Python libraries using `pip`. Specifically, the `mcpi` library will allow Python to interact with the Minecraft server.
   - Install the library by running the following command:
     ```bash
     pip install mcpi
     ```

5. **Run the Python Scripts**:
   - Clone this repository and execute the Python scripts in your terminal or Python environment. The scripts interact with the Minecraft server to execute actions based on your Python code.
