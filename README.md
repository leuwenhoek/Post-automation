# Post-Automation 🚀

This project leverages **open-source models** to automate posting workflows.  
Future updates will include direct automation for **X (Twitter)** and **LinkedIn**, enabling seamless posting to your accounts.

---

## Getting Started ⚙️

### Prerequisites

- Install [Ollama](https://ollama.com/) on your system.

### Setup Instructions

1. **Download a model**  
   Open your terminal and run:
   
   ```cmd
   ollama pull <model-name>
   ```
   
   You can choose a model based on your PC specs. Explore available models at [Ollama Search](https://ollama.com/search).

2. **Verify the Model**  
   Test if the model runs correctly:
   
   ```cmd
   ollama run <model-name>
   ```
   
   > *Congrats! You have downloaded your open-source model to run in the project.*

## Setup in VS Code 🥀

1. **Clone the repository**
   
   ```bash
   git clone https://github.com/leuwenhoek/Post-automation.git
   ```
   
   > **Recommendation:**  
   > You can install [uv](https://pypi.org/project/uv/) globally — it is a very fast package manager compared to pip.

2. **Create a virtual environment**
   
   If you are using the default package manager:
   
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   ```
   
   If you are using uv:
   
   ```bash
   uv venv
   venv\Scripts\activate.bat
   ```
   
   If you are using Conda:
   
   ```bash
   conda create -n post-automation python=3.10
   conda activate post-automation
   ```

3. Install all the requirements using:
    ```python
    pip install -r requirements.txt
    ```

4. Now you can the script by:
    ```python
    python scraper.py
    ```

## What it can do (for now) 😋
1. Can analyze the market trends for your topic.
2. Reccomends you the best topics to create post.
3. generates the post for X (for now).

## Roadmap 🔨

- 🔜 Integration with X (Twitter) for automated posting
- 🔜 Integration with LinkedIn for automated posting
- 📈 Expansion to other platforms and advanced scheduling features

## Contributing 🤝

**Contributions are welcome!** Feel free to fork the repo, open issues, or submit pull requests to improve functionality.

## License 📄

This project is open-source under the MIT License.