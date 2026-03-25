"""Minimal LangGraph example with explicit state and two nodes.

This is a small boilerplate that demonstrates:
- A predefined, typed State
- Multiple nodes that read/update the shared state
- A simple linear graph with an entry point and end

Install (if needed):
  pip install langgraph

Note that we are predefining the state to add determinism to LLM outputs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, END, START
from ollama import chat
from ollama import ChatResponse


PROMPTS_DIR = Path(__file__).with_name("prompts")
OLLAMA_MODEL = "ministral-3:3b"


class StoryState(TypedDict):
    """Fixed shape for graph state."""

    characters: dict
    timeline: dict
    story_text: str
    prompt: str
    title: str


def _load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _call_ollama(prompt: str) -> str:
    response: ChatResponse = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response.message.content.strip()


def create_characters(state: StoryState):
    """ 
    This function creates characters for your story. Each character must serve a purpose in the story.
    Therefore we ask the LLM to return a JSON state that returns characters along with their descriptions.
    For e.g. the output should look like this:
    {
        "Alex Prowse": "Main Character, Undergraduate Student of Computer Science at Northeastern University. American Descent. Smart Kid. Potential Researcher.
        His PhD Applications are stuck because he failed a test on suspicions of cheating.",
        "Professor John Davidson": "Professor of Computer Science at Northeastern University. American Descent. Strict Grader. He failed Alex
        in a test on suspicion of cheating.",
        "Rohan Kumar": "Teaching Assistant for Professor Davidson. Indian Descent. Fair Grader. He believes that Alex deserves another chance and Professor Davidson
        was too strict on him"
    }

    This output gets stored as characters key in the StoryState
    """

    prompt_template = _load_prompt("create_characters.md")
    prompt = prompt_template.format(story_prompt=state["prompt"])
    content = _call_ollama(prompt)

    try:
        characters = json.loads(content)
    except json.JSONDecodeError:
        characters = {
            "Alex Prowse": "Main Character, Undergraduate Student of Computer Science at Northeastern University. American Descent.",
            "Professor John Davidson": "Professor of Computer Science at Northeastern University. Strict Grader.",
        }

    return {"characters": characters}


def timeline_creator(state: StoryState) -> StoryState:
    """
    Creates timeline based on prompt. Again returns a JSON output. Each key represents a particular period of time. 
    For e.g.:
    {
        "January 2025": "Professor Davidson fails Alex in final test of Algorithms on suspicion of cheating. He invokes an OSCAR meeting over Alex.",
        "March 2025": "Alex attends OSCAR hearing and pleads not guilty as he did not cheat on the exam. He requests re-appearing of the test under strict vigilance.",
        "May 2025": "OSCAR deems Alex not guilty but fails him in the class anyways. It requires Alex to re-take the course over the summer.",
        "June 2025": "Alex re-starts the Algorithms class, again under Professor Davidson for Summer 2 Semester",
        "August 2025": "Alex's research on stack-based algorithms gets accepted to a renowned conference.",
        "September 2025": "OSCAR Committee decide to lift the ban on Alex for working in research labs.",
        "November 2025": "Alex meets Rohan, a TA for Professor Davidson, who believes that Alex did not deserve the treatment he received. He vouches for him 
        and asks Professor Davidson to vouch for Alex in his PhD Applications".
        "December 2025": "Professor Davidson advises Alex to not pursue PhD this year as the F grade in Algorithms will leave a bad impact on the committee."
    }
    This goes into timeline key of the StoryState
    """

    prompt_template = _load_prompt("timeline_creator.md")
    prompt = prompt_template.format(
        story_prompt=state["prompt"],
        characters=json.dumps(state["characters"]),
    )
    content = _call_ollama(prompt)

    try:
        timeline = json.loads(content)
    except json.JSONDecodeError:
        timeline = {
            "January 2025": "An incident derails the student during finals.",
            "March 2025": "They appeal and prepare to rebuild their plan.",
        }

    return {"timeline": timeline}


def title_generator(state: StoryState) -> StoryState:
    """
    Creates a title of the story based on the StoryState. Output goes into the title key of StoryState.
    """

    prompt_template = _load_prompt("title_generator.md")
    prompt = prompt_template.format(
        story_prompt=state["prompt"],
        characters=json.dumps(state["characters"]),
        timeline=json.dumps(state["timeline"]),
    )
    title = _call_ollama(prompt)

    return {"title": title}


def story_writer(state: StoryState) -> StoryState:
    """
    Writes a short story using characters, timeline and prompt provided
    """

    prompt_template = _load_prompt("story_writer.md")
    prompt = prompt_template.format(
        story_prompt=state["prompt"],
        title=state["title"],
        characters=json.dumps(state["characters"]),
        timeline=json.dumps(state["timeline"]),
    )
    story_text = _call_ollama(prompt)

    return {"story_text": story_text}


def build_graph():
    builder = StateGraph(StoryState)

    builder.add_node("characters", create_characters)
    builder.add_node("timeline", timeline_creator)
    builder.add_node("title", title_generator)
    builder.add_node("story", story_writer)

    builder.add_edge(START, "characters")
    builder.add_edge("characters", "timeline")
    builder.add_edge("timeline", "title")
    builder.add_edge("title", "story")
    builder.add_edge("story", END)

    return builder.compile()


def main() -> None:
    graph = build_graph()

    initial_state: StoryState = {
        "prompt": "Write a coming of age story about an aspiring Computer Science bachelors student who wants to pursue a PhD but faces an unexepected hurdle in his journey.",
        "characters": {},
        "timeline": {},
        "title": "",
        "story_text": "",
    }

    final_state = graph.invoke(initial_state)
    print("Final state:")
    print(final_state)


if __name__ == "__main__":
    main()
