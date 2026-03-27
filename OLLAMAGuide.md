# OLLAMA Installation and Usage Guide

## Install OLLAMA on your PC

Before Installing OLLAMA, we need to understand that OLLAMA requires a two step installation. It is an independent service that runs on your device as well as runs on Python scripts. This creates a seamless On-Device hosting of your LLM.

### OLLAMA App Installation

1. Install OLLAMA on your device: https://ollama.com/download
2. Feel free to use the CLI if you are comfortable with it or download the `.dmg` or `.exe` file.
3. Once installed, you will find the OLLAMA app on your PC. It's icon is a cute LLAMA.
4. Start the OLLAMA App.
5. Confirm OLLAMA is running by visiting http://localhost:11434 in your browser.

### OLLAMA Python Installation

1. Go to the Github we created earlier and fire a Command Line Interface in the Directory.
2. Create a Python Virtual Environment: `python3 -m venv venv`.
3. Activate the Virtual Environment using `source venv/bin/activate`
4. Install OLLAMA using `pip`: `pip install ollama`. (You can also run `pip install -r requirements.txt` if you are cloning this repository).

### Using OLLAMA in your code.

1. We have a boilerplate OLLAMA code available at `SampleCode/ollama_sample.py`.
2. To run the code, you need to "pull" a model from OLLAMA model store.
3. Select your favorite model from: https://ollama.com/search
4. I am selecting the model `ministral-3:3b`.
5. Download the model using the command: `ollama pull ministral-3:3b` in your Terminal. NOTE: Ollama App must be running for this command to run successfully.
6. Once done, check the Boilerplate Code and start developing!