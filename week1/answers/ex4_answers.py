"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = """
There are currently no Edinburgh venues available that can accommodate 300 guests with vegan options. Would you like to:
1. Try a lower minimum capacity (e.g., 200-250 people)
2. Remove the vegan requirement
3. Search for multiple smaller venues combined?
"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I set The Albanach to full in the venue server data. In the first run search_venues returned two
venues so the model made an extra get_venue_details call to pick the best one. In the second run
only Haymarket Vaults came back, so the model skipped the details call and answered straight from
the search result — fewer tool calls needed. No client code or prompt changes were required.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 248   # count in exercise2_langgraph.py (venue_tools.py, imported directly)
LINES_OF_TOOL_CODE_EX4 = 0   # count in exercise4_mcp_client.py (tools discovered via MCP, no definitions)

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP gives you runtime tool discovery — the client doesn't need to know what tools exist at import time.
You can add, remove, or change tools on the server without touching the client code at all. Also any
agent that speaks MCP can connect to the same server — a LangGraph agent and a Rasa action could both
use the same venue tools without duplicating the definitions. It's a shared contract, not just a
separate file.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a thinking model (e.g. Qwen3-32B) that breaks Rod's WhatsApp message into subgoals like "find venue", "confirm booking", "generate flyer". It sits upstream of the autonomous loop so the executor gets clear, ordered tasks.
- The Executor is the ReAct loop from research_agent.py — it takes one subgoal at a time and reasons across tool calls (search venues, check weather, etc). It lives in the autonomous-loop half and grows with new tools like web search and file ops.
- The Shared MCP Tool Server (evolved from mcp_venue_server.py) is the shared layer both halves connect to. It serves venue lookups, web search, calendar, email — neither half cares where a tool came from, they just discover what's available.
- The Handoff Bridge sits between the two halves. When the executor hits a task that needs a human conversation (like confirming a deposit with the pub manager), it routes to the Rasa side. When Rasa needs research, it routes back to the loop.
- The Structured Agent is the Rasa CALM agent from exercise3_rasa — it handles the pub manager call with explicit flows and deterministic business guards. It lives in the structured-agent half and gets wired to the shared MCP server and a RAG knowledge base.
- The Persistent Memory Store runs alongside the executor in the autonomous loop, keeping track of what's been done across subgoals so the planner doesn't repeat work and the system can resume if interrupted.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph for research, Rasa CALM for the call. In exercise 2 the LangGraph agent decided on its own
which venues to check and in what order — that's what you need for open-ended research. But in
scenario 3 it couldn't handle an out-of-scope question properly. Rasa CALM in exercise 3 did the
opposite — fixed flow, deterministic guards, and when the manager asked about parking it deflected
cleanly and offered to resume. Swapping them would mean letting a probabilistic agent handle the
£300 deposit check (it could reason around it) and forcing a rigid flow agent to do venue comparison
(it can't call tools outside flows.yml). Both would break.
"""