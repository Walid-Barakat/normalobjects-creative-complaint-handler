"""
NormalObjects - Creative Complaint Handler (LangChain)

This lab solution builds "Becma's Chaos Mode": a creative complaint-handling
agent that can call themed tools in a flexible, freeform order.

Run:
    python normalobjects_langchain.py

Optional deterministic demo without an API key:
    python normalobjects_langchain.py --mock
"""

from __future__ import annotations

import argparse
import os
import random
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# -----------------------------
# 1. Environment and constants
# -----------------------------

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_COMPLAINTS: List[str] = [
    "Why do demogorgons sometimes eat people and sometimes just stare at lamps?",
    "The portal opens on different days. Is there a schedule or is the universe improvising?",
    "Why can some psychics see the Downside Up and others only get headaches?",
    "Why do creatures and power lines react so strangely together?",
]


# -----------------------------
# 2. Creative themed tools
# -----------------------------

@tool
def consult_demogorgon(complaint: str) -> str:
    """Get the Demogorgon's perspective on a complaint about the Downside Up.

    Use this when the complaint involves creatures, monster behavior, fear,
    hunger, portals, or anything that might benefit from a chaotic creature's
    interpretation.

    Args:
        complaint: The complaint or inconsistency to ask the Demogorgon about.

    Returns:
        A creative, creature-centered interpretation of the problem.
    """
    responses = [
        (
            f"The Demogorgon tilts its head at: '{complaint}'. "
            "It believes the complainant is using ordinary geometry in a place "
            "where hallways may be emotionally curved."
        ),
        (
            f"The Demogorgon clicks twice about: '{complaint}'. "
            "Translation by the Bureau: the behavior depends on scent, fear, "
            "electricity, and whether lunch already happened in a parallel minute."
        ),
        (
            f"The Demogorgon scratches a symbol into the wall about: '{complaint}'. "
            "It seems to say consistency is a human superstition, but patterns appear "
            "near magnets, music, and unattended snack food."
        ),
    ]
    return random.choice(responses)


@tool
def check_hawkins_records(query: str) -> str:
    """Search fictional Hawkins/Walvins anomaly records for clues.

    Use this tool when the complaint asks for historical patterns, schedules,
    records, timelines, portals, electricity, monsters, or psychic events.

    Args:
        query: Search terms or a short description of the mystery.

    Returns:
        A record-style explanation with clues and caveats.
    """
    records: Dict[str, str] = {
        "portal": (
            "Archive result: portals rarely follow a calendar. They cluster around "
            "emotional surges, electromagnetic spikes, failing lights, basement leaks, "
            "and events that adults call 'probably just the wind.'"
        ),
        "schedule": (
            "Archive result: no reliable public schedule exists. However, previous openings "
            "often occurred near repeating pulses: lights flicker, compasses drift, then a "
            "wall becomes suspiciously damp."
        ),
        "monster": (
            "Archive result: creature behavior varies with territory, hunger, fear nearby, "
            "distance from portals, and interference from music or improvised plans made by kids."
        ),
        "demogorgon": (
            "Archive result: demogorgons are territorial but inconsistent because they react "
            "to smell, blood, fear, electrical noise, and interdimensional weather fronts."
        ),
        "psychic": (
            "Archive result: psychic abilities differ by person. Some can sense the Downside Up, "
            "some move objects, and some only receive migraines and dramatic nosebleeds."
        ),
        "electricity": (
            "Archive result: power lines behave like antennae around the Downside Up. Surges, "
            "flickers, and humming wires often indicate a feedback loop between worlds."
        ),
        "power": (
            "Archive result: lights and power lines are early-warning instruments. They do not "
            "cause every anomaly, but they reveal when the boundary between worlds gets thin."
        ),
    }

    query_lower = query.lower()
    matched = [value for key, value in records.items() if key in query_lower]
    if matched:
        return "\n".join(matched)

    return (
        f"Archive result: no exact file for '{query}', but the Bureau records say most "
        "inconsistencies become less random after checking three things: emotional pressure, "
        "electromagnetic noise, and whether a portal recently sighed open."
    )


@tool
def cast_interdimensional_spell(problem: str, creativity_level: str = "medium") -> str:
    """Suggest creative ritual-style fixes for a Downside Up complaint.

    Use this when the agent needs an entertaining solution, a practical-but-weird
    recommendation, or a final creative action plan.

    Args:
        problem: The complaint or problem to solve.
        creativity_level: One of low, medium, or high.

    Returns:
        One or more creative solution ideas.
    """
    level = creativity_level.lower().strip()
    if level not in {"low", "medium", "high"}:
        level = "medium"

    number_to_return = {"low": 1, "medium": 2, "high": 3}[level]
    spells = [
        (
            f"Compass Recalibration: put a compass inside a cereal bowl, turn off the lights, "
            f"and ask it politely to point toward the least dramatic version of: {problem}"
        ),
        (
            f"Walkman Stabilizer: play one emotionally important song near the anomaly while "
            f"someone writes down every light flicker connected to: {problem}"
        ),
        (
            f"Salt-and-Snack Containment: make a salt circle, place three waffles or crackers "
            f"at the corners, and declare the Bureau temporarily in charge of: {problem}"
        ),
        (
            f"Reverse Complaint Ritual: restate the complaint as a compliment, then ask the "
            f"Downside Up to become embarrassed and correct itself: {problem}"
        ),
        (
            f"Flashlight Morse Accord: blink 'B-E-C-M-A' at the nearest suspicious wall, then "
            f"wait for the wall to negotiate terms about: {problem}"
        ),
    ]

    return "\n".join(f"- {spell}" for spell in random.sample(spells, number_to_return))


@tool
def gather_party_wisdom(question: str) -> str:
    """Ask the Bureau's kid-investigator party for collective wisdom.

    Use this for practical reasoning, teamwork-style hypotheses, and translating
    scary anomalies into testable ideas.

    Args:
        question: The question or complaint to ask the party about.

    Returns:
        A multi-perspective answer from the party.
    """
    question_lower = question.lower()

    if any(word in question_lower for word in ["portal", "schedule", "calendar", "opens"]):
        return (
            "Mike: 'Portals probably follow pressure, not a calendar.' "
            "Dustin: 'Measure lights, compasses, and weird radio noise first.' "
            "Lucas: 'Also create an escape route before calling it research.' "
            "Will: 'It feels colder right before the boundary thins.'"
        )

    if any(word in question_lower for word in ["monster", "demogorgon", "creature", "eat"]):
        return (
            "Lucas: 'Creatures are territorial and opportunistic.' "
            "Dustin: 'Fear, food, and electrical interference could explain the inconsistent behavior.' "
            "Mike: 'So the answer is not random; it is badly documented.' "
            "Will: 'They also react to attention. Try not to be the loudest snack.'"
        )

    if any(word in question_lower for word in ["psychic", "powers", "see", "headache"]):
        return (
            "Mike: 'Powers connect to emotion and practice.' "
            "Dustin: 'Different brains tune into different frequencies.' "
            "Lucas: 'So not seeing the Downside Up does not mean nothing is there.' "
            "Will: 'Sometimes the signal arrives as feelings before images.'"
        )

    if any(word in question_lower for word in ["electric", "power", "wire", "line", "lights"]):
        return (
            "Dustin: 'Power lines act like accidental antennas.' "
            "Lucas: 'That means creatures may follow the noise or be irritated by it.' "
            "Mike: 'Track flickers like breadcrumbs.' "
            "Will: 'The humming gets worse when something is close.'"
        )

    return (
        "Mike: 'Name the pattern first.' Dustin: 'Then gather measurements.' "
        "Lucas: 'Then do not split up.' Will: 'And listen when the walls sound wet.'"
    )


@tool
def consult_eleven_signal(static_description: str) -> str:
    """Interpret psychic/static signals related to a complaint.

    Use this when the complaint involves visions, missing information, intuition,
    signal noise, emotional resonance, or why some people sense anomalies while
    others cannot.

    Args:
        static_description: A short description of the signal, symptom, or mystery.

    Returns:
        A psychic-signal interpretation.
    """
    return (
        f"Eleven Signal Reading for '{static_description}': the signal is not absent; "
        "it is filtered. Strong emotion sharpens it, exhaustion distorts it, and nearby "
        "electromagnetic noise can turn a clear vision into a headache with subtitles missing."
    )


TOOLS = [
    consult_demogorgon,
    check_hawkins_records,
    cast_interdimensional_spell,
    gather_party_wisdom,
    consult_eleven_signal,
]


# -----------------------------
# 3. Agent construction
# -----------------------------

def create_llm(model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE) -> ChatOpenAI:
    """Create the OpenAI chat model used by the agent."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Create a .env file or export the variable before running."
        )

    return ChatOpenAI(model=model, temperature=temperature)


def build_agent_executor(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    verbose: bool = True,
) -> AgentExecutor:
    """Build the LangChain agent executor with all creative tools registered."""
    llm = create_llm(model=model, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are Becma's Chaos Mode, the official complaint handler for the "
                    "Downside-Up Complaint Bureau. Your job is to handle fictional complaints "
                    "about Normal Objects universe inconsistencies.\n\n"
                    "Behavior rules:\n"
                    "1. Use tools creatively and flexibly; there is no required order.\n"
                    "2. For most complaints, consult at least two different tools before the final answer.\n"
                    "3. Explain the inconsistency with a playful but useful theory.\n"
                    "4. End with a creative Bureau Resolution: a short action plan or ritual.\n"
                    "5. Keep the answer entertaining, clear, and safe.\n"
                    "6. Do not claim real-world truth; this is a fictional universe."
                ),
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_openai_tools_agent(llm=llm, tools=TOOLS, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=verbose,
        max_iterations=6,
        early_stopping_method="generate",
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )


# -----------------------------
# 4. Demo and analysis helpers
# -----------------------------

def extract_tool_sequence(intermediate_steps: List[Tuple[Any, Any]]) -> List[str]:
    """Return the ordered tool names from LangChain intermediate steps."""
    sequence: List[str] = []
    for action, _observation in intermediate_steps:
        # action.tool is the standard location for the tool name.
        sequence.append(getattr(action, "tool", "unknown_tool"))
    return sequence


def summarize_tool_usage(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize tool counts and tool chains from demo results."""
    all_sequences: List[List[str]] = [item["tool_sequence"] for item in results]
    flattened = [tool_name for sequence in all_sequences for tool_name in sequence]
    counts = Counter(flattened)

    return {
        "total_tool_calls": sum(counts.values()),
        "tool_counts": dict(counts),
        "most_used": counts.most_common(1)[0][0] if counts else None,
        "tool_sequences": all_sequences,
    }


def handle_complaint(agent_executor: AgentExecutor, complaint: str) -> Dict[str, Any]:
    """Run one complaint through the agent and return output plus tool usage."""
    result = agent_executor.invoke({"input": complaint})
    intermediate_steps = result.get("intermediate_steps", [])
    tool_sequence = extract_tool_sequence(intermediate_steps)

    return {
        "complaint": complaint,
        "response": result.get("output", ""),
        "tool_sequence": tool_sequence,
        "tool_count": len(tool_sequence),
    }


def run_demo(
    complaints: List[str] | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Run the full lab demonstration against at least three complaints."""
    complaints = complaints or SAMPLE_COMPLAINTS
    agent_executor = build_agent_executor(model=model, temperature=temperature, verbose=verbose)

    results: List[Dict[str, Any]] = []
    for complaint in complaints:
        print("\n" + "=" * 80)
        print(f"COMPLAINT: {complaint}")
        print("=" * 80)
        item = handle_complaint(agent_executor, complaint)
        results.append(item)
        print("\nFINAL RESPONSE:")
        print(item["response"])
        print(f"\nTOOLS USED: {' -> '.join(item['tool_sequence']) or 'No tools used'}")

    stats = summarize_tool_usage(results)
    save_demo_markdown(results, stats)

    print("\n" + "=" * 80)
    print("TOOL USAGE ANALYSIS")
    print("=" * 80)
    print(f"Total tool calls: {stats['total_tool_calls']}")
    print(f"Tool counts: {stats['tool_counts']}")
    print(f"Most used tool: {stats['most_used']}")
    print("Tool sequences:")
    for index, sequence in enumerate(stats["tool_sequences"], start=1):
        print(f"  {index}. {' -> '.join(sequence) or 'No tools used'}")

    return {"results": results, "stats": stats}


def save_demo_markdown(results: List[Dict[str, Any]], stats: Dict[str, Any]) -> Path:
    """Save the demonstration evidence required by the lab."""
    output_path = OUTPUT_DIR / "demo_results.md"

    lines = [
        "# Demo Results - NormalObjects Creative Complaint Handler",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Complaints Handled",
        "",
    ]

    for index, item in enumerate(results, start=1):
        lines.extend(
            [
                f"### {index}. Complaint",
                "",
                item["complaint"],
                "",
                "**Tool sequence:** "
                + (" -> ".join(item["tool_sequence"]) if item["tool_sequence"] else "No tools used"),
                "",
                "**Creative solution:**",
                "",
                item["response"],
                "",
            ]
        )

    lines.extend(
        [
            "## Tool Usage Patterns",
            "",
            f"- Total tool calls: {stats['total_tool_calls']}",
            f"- Tool counts: `{stats['tool_counts']}`",
            f"- Most used tool: `{stats['most_used']}`",
            "",
            "## Interpretation",
            "",
            (
                "The agent used tools in flexible orders rather than following a fixed workflow. "
                "That is appropriate for this creative complaint-handling task because the agent "
                "can explore records, creature interpretation, party wisdom, psychic signals, and "
                "ritual-style resolutions depending on the complaint."
            ),
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


# -----------------------------
# 5. Mock mode for environment checks
# -----------------------------

def run_mock_demo() -> Dict[str, Any]:
    """Run a deterministic no-API demonstration for setup checks.

    This is not a replacement for the real LangChain run. It is provided so a
    user can confirm the project files and Python environment work before
    spending API tokens.
    """
    results: List[Dict[str, Any]] = []

    mock_sequences = [
        ["check_hawkins_records", "gather_party_wisdom", "cast_interdimensional_spell"],
        ["check_hawkins_records", "consult_demogorgon", "cast_interdimensional_spell"],
        ["consult_eleven_signal", "gather_party_wisdom", "cast_interdimensional_spell"],
        ["check_hawkins_records", "gather_party_wisdom", "consult_demogorgon"],
    ]

    for complaint, sequence in zip(SAMPLE_COMPLAINTS, mock_sequences):
        response = (
            "Mock Bureau Response: the inconsistency is probably caused by emotional pressure, "
            "electromagnetic noise, and the Downside Up refusing to fill out paperwork. "
            "Bureau Resolution: track flickering lights, ask the party for a second opinion, "
            "then perform a harmless compass-and-Walkman recalibration ritual."
        )
        results.append(
            {
                "complaint": complaint,
                "response": response,
                "tool_sequence": sequence,
                "tool_count": len(sequence),
            }
        )

    stats = summarize_tool_usage(results)
    save_demo_markdown(results, stats)

    print("Mock demo completed. This confirms files and environment structure, not API connectivity.")
    print(f"Demo evidence saved to: {OUTPUT_DIR / 'demo_results.md'}")
    print(f"Tool counts: {stats['tool_counts']}")

    return {"results": results, "stats": stats}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the NormalObjects LangChain lab solution.")
    parser.add_argument("--mock", action="store_true", help="Run deterministic no-API demo.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name.")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="Creativity level.")
    parser.add_argument("--quiet", action="store_true", help="Turn off LangChain verbose logs.")
    args = parser.parse_args()

    if args.mock:
        run_mock_demo()
    else:
        run_demo(model=args.model, temperature=args.temperature, verbose=not args.quiet)


if __name__ == "__main__":
    main()
