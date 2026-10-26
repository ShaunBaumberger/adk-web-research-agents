# Web research agent team (Google ADK)

A small multi-agent system built with [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/), defined entirely in YAML: no Python code.

Give it a URL or a topic, and three agents work in a chain:

```
web_research_coordinator ──► research_agent ──► summary_agent
   receives the request        scrapes the web      writes the final report
                               with Firecrawl
```

- **web_research_coordinator** ([root_agent.yaml](my_first_agent/root_agent.yaml)) takes the request and hands it to the research agent.
- **research_agent** ([research_agent.yaml](my_first_agent/research_agent.yaml)) reads web pages through the [Firecrawl](https://www.firecrawl.dev) MCP server, then hands over to the summary agent.
- **summary_agent** ([summary_agent.yaml](my_first_agent/summary_agent.yaml)) writes the final report: executive summary, detailed summary, key takeaways and recommendations.

All agents use `gemini-3.5-flash`.

## Bonus: code execution agent

[code_agent](code_agent/agent.py) is a single Python agent with ADK's `BuiltInCodeExecutor`. For calculations, dates and data, Gemini writes Python, runs it in Google's sandbox, and answers from the real output instead of guessing. Try *"What is 48,273 × 9,184?"* or *"On which weekday was 1 August 1291?"* and open the event in `adk web` to see the code and its result.

It only needs a Gemini API key: `cp code_agent/.env.example code_agent/.env` and fill it in.

## Bonus: two agents talking over A2A

[serve_code_agent.py](serve_code_agent.py) runs `code_agent` as a standalone [A2A](https://a2a-protocol.org) service on port 8001 and publishes its agent card at `http://localhost:8001/.well-known/agent-card.json`. [trip_planner](trip_planner/agent.py) is a separate agent that only knows that address: it adds the calculator as a `RemoteA2aAgent` and hands every calculation over the network.

Run them in two terminals from the repository root (after `cp trip_planner/.env.example trip_planner/.env` and adding your key):

```bash
uvicorn serve_code_agent:app --port 8001   # terminal 1: the calculator service
adk web .                                  # terminal 2: pick trip_planner
```

Ask something like *"4 people, train CHF 86 per person one way, 2 hotel rooms at CHF 240 for 3 nights: total for the round trip?"* and watch terminal 1 log the `GET` for the agent card and the `POST` with the task.

## Run it yourself

You need Python 3.10+ and Node.js (for `npx`), plus two API keys: Gemini ([Google AI Studio](https://aistudio.google.com/apikey)) and [Firecrawl](https://www.firecrawl.dev).

```bash
git clone https://github.com/ShaunBaumberger/adk-web-research-agents.git
cd adk-web-research-agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp my_first_agent/.env.example my_first_agent/.env   # then put your keys in .env
adk web .
```

Open http://127.0.0.1:8000, pick **my_first_agent**, and try *"Scrape and analyze https://example.com"*.

Start `adk web .` from the repository root: the research agent loads its Firecrawl key from `my_first_agent/.env` relative to that folder.

## What I changed from the original tutorial

This started from a [tutorial thread](https://x.com/Saboo_Shubham_) written for an older ADK version. Getting it to run on ADK 2.13 took a few changes:

| Problem | Fix |
|---|---|
| `gemini-2.5-flash` is outdated | Switched every agent to `gemini-3.5-flash` |
| `No module named 'mcp'` | MCP support is now an optional extra: `pip install "google-adk[mcp]"` |
| ADK blocks YAML configs from launching local processes | Set `ADK_ALLOW_CONFIG_STDIO_MCP_SERVERS=1` in `.env` (only for configs you trust) |
| Firecrawl timed out after 5 seconds | Moved to `stdio_connection_params` with `timeout: 60` |
| `"${FIRECRAWL_API_KEY}"` in YAML is passed through literally, and MCP servers don't inherit your environment | The server starts through `sh`, which loads the key from `.env`, so no key is stored in the YAML |
| With `sub_agents`, the research agent answered directly and the summary agent never ran | The research agent now explicitly transfers to `summary_agent` when it's done |

I also tried making the coordinator call both helpers as tools (`AgentTool`) and merge their results. `adk web` refuses that in YAML (`Blocked key 'args'`), so the agents pass the conversation along a chain instead. That's also cheaper in tokens, since findings aren't copied back and forth through the coordinator.
