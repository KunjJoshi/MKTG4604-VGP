# SampleCode

## What is Ollama?
Ollama is a local LLM runtime that lets you run and chat with models on your own machine. It provides a simple CLI and a Python API so you can download models and make inference calls from code. In this repo, we use Ollama to generate story components (characters, timeline, title, and final story).

## What is LangGraph?
LangGraph is a lightweight framework for building multi-step LLM workflows with explicit, typed state. You define a state object and a graph of nodes; each node reads and updates parts of the state. This makes complex, multi-stage tasks more deterministic and easier to debug.

## What do they do together?
- LangGraph orchestrates the workflow steps (character creation, timeline creation, title generation, story writing).
- Ollama executes the LLM calls inside each step.

## Installation

### Install Ollama
1. Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Pull a model (example used in this repo):

```bash
ollama pull ministral-3:3b
```

### Install LangGraph and dependencies
If you are using a virtual environment, activate it first. Then run:

```bash
pip install langgraph ollama
```

## Running the sample
From the project root:

```bash
python SampleCode/lanngraph_sample.py
```
