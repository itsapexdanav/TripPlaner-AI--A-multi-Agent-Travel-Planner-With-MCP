# ✈️ TripPlanner AI

### Multi-Agent AI Travel Planner powered by LangGraph + MCP

<p align="center">
  <strong>Research flights • Discover hotels • Check weather • Build itineraries • Maintain conversation context</strong>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1.2+-1C3C3C?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-1.3+-1C3C3C?style=for-the-badge)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Checkpointing-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)

</p>

---

# 🌍 What is TripPlanner AI?

**TripPlanner AI** is a multi-agent travel planning application built with:

* Python
* FastAPI
* LangGraph
* LangChain
* Model Context Protocol (MCP)
* Groq
* PostgreSQL
* Tavily
* AviationStack
* OpenWeather

The system converts a natural-language travel request into a structured travel plan.

For example:

> **"Plan a 5-day trip to Japan with a budget of $1500. Find flights, hotels, check the weather, and create a practical itinerary."**

Instead of making one LLM responsible for everything, the application divides the task into specialized agents.

The current workflow is:

```text
                         USER
                           │
                           ▼
                  ┌──────────────────┐
                  │   Flight Agent   │
                  │                  │
                  │ AviationStack MCP│
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   Hotel Agent    │
                  │                  │
                  │   Tavily MCP     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Weather Agent   │
                  │                  │
                  │ Weather MCP      │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Itinerary Agent  │
                  │                  │
                  │     Groq LLM     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Final Response   │
                  │      Agent       │
                  └────────┬─────────┘
                           │
                           ▼
                    FINAL TRAVEL PLAN
```

The important architectural change in this version is that external capabilities are exposed through **MCP servers** rather than being tightly coupled to the LangGraph agents.

---

# 🎯 Why MCP?

The earlier implementation of this project directly interacted with external services.

Conceptually:

```text
Agent
  │
  ├──► AviationStack API
  │
  ├──► Tavily API
  │
  └──► Weather API
```

The new implementation introduces **Model Context Protocol (MCP)** as a tool integration layer.

```text
                    LangGraph
                       │
                       ▼
                 MCP Client Layer
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Tavily MCP   AviationStack   Weather MCP
                       MCP
          │            │            │
          ▼            ▼            ▼
      Tavily       AviationStack  OpenWeather
```

This creates a separation between:

```text
Agent / Orchestration
        │
        ▼
    MCP Client
        │
        ▼
     MCP Tools
        │
        ▼
 External Services
```

This means the agent logic does not need to directly implement the communication details of every external service.

---

# 🧠 What is MCP?

**MCP (Model Context Protocol)** is a protocol for connecting AI applications with external tools and data sources through a standardized interface.

Instead of writing service-specific integration logic directly inside every agent, an MCP server can expose capabilities as tools.

For example:

```text
Weather MCP Server

get_current_weather(city)
get_forecast(city)
```

The application can then discover and invoke those tools through an MCP client.

Conceptually:

```text
┌─────────────────────┐
│    LangGraph Agent  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    MCP Client       │
└──────────┬──────────┘
           │
           │ MCP
           ▼
┌─────────────────────┐
│    MCP Server       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ External API / Tool │
└─────────────────────┘
```

---

# ✨ Key Features

| Feature                   | Description                                    |
| ------------------------- | ---------------------------------------------- |
| 🤖 Multi-Agent Workflow   | Specialized agents coordinated with LangGraph  |
| 🔌 MCP Integration        | External capabilities accessed through MCP     |
| ✈️ Flight Research        | AviationStack MCP integration                  |
| 🏨 Hotel Research         | Tavily MCP integration                         |
| 🌤️ Weather Research      | Custom Weather MCP server                      |
| 🗓️ AI Itinerary          | Groq-powered itinerary generation              |
| 🧠 Shared State           | Agents communicate through `TravelState`       |
| 💾 PostgreSQL Persistence | Persistent LangGraph checkpoints               |
| 🧵 Conversation Threads   | Continue conversations using `thread_id`       |
| 🌐 FastAPI                | Backend API                                    |
| 🎨 Web UI                 | HTML/CSS/JavaScript interface                  |
| 🐳 Docker                 | Container-ready application                    |
| 🛠️ MCP Client            | `MultiServerMCPClient` manages MCP connections |

---

# 🏗️ System Architecture

```mermaid
flowchart TD

    USER["👤 User"]

    UI["🌐 TripPlanner Web UI<br/>HTML + CSS + JavaScript"]

    API["⚡ FastAPI<br/>POST /api/travel"]

    GRAPH["🧠 LangGraph<br/>Travel Planning Workflow"]

    STATE["📦 TravelState"]

    F["✈️ Flight Agent"]
    H["🏨 Hotel Agent"]
    W["🌤️ Weather Agent"]
    I["🗓️ Itinerary Agent"]
    R["📝 Final Response Agent"]

    MCP["🔌 MCP Client Layer"]

    TMCP["🔎 Tavily MCP"]
    AMCP["✈️ AviationStack MCP"]
    WMCP["🌤️ Custom Weather MCP"]

    T["Tavily"]
    A["AviationStack"]
    O["OpenWeather"]

    LLM["⚡ Groq LLM"]

    DB[("🐘 PostgreSQL<br/>LangGraph Checkpoints")]

    USER --> UI
    UI --> API
    API --> GRAPH

    GRAPH --> F
    F --> MCP
    MCP --> AMCP
    AMCP --> A
    F --> STATE

    STATE --> H
    H --> MCP
    MCP --> TMCP
    TMCP --> T
    H --> STATE

    STATE --> W
    W --> MCP
    MCP --> WMCP
    WMCP --> O
    W --> STATE

    STATE --> I
    I --> LLM
    I --> STATE

    STATE --> R
    R --> LLM
    R --> STATE

    STATE --> DB
    DB -. persisted state .-> GRAPH

    R --> API
    API --> UI
```

---

# 🔄 Agent Workflow

The current LangGraph workflow is sequential:

```mermaid
flowchart LR

    START(["👤 User Request"])

    F["1️⃣ Flight Agent<br/>AviationStack MCP"]

    H["2️⃣ Hotel Agent<br/>Tavily MCP"]

    W["3️⃣ Weather Agent<br/>Weather MCP"]

    I["4️⃣ Itinerary Agent<br/>Groq"]

    R["5️⃣ Final Response Agent<br/>Groq"]

    END(["📋 Final Travel Plan"])

    START --> F
    F --> H
    H --> W
    W --> I
    I --> R
    R --> END
```

The current graph explicitly connects:

```text
START
  ↓
Flight Agent
  ↓
Hotel Agent
  ↓
Weather Agent
  ↓
Itinerary Agent
  ↓
Final Response Agent
  ↓
END
```

This makes the data dependencies straightforward and allows each stage to enrich the shared state.

---

# 🔌 MCP Architecture

The MCP layer currently connects three external capabilities.

```text
                         MCP Client
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
       Tavily MCP       AviationStack MCP   Weather MCP
            │                │                │
            ▼                ▼                ▼
         Tavily         AviationStack      OpenWeather
```

The project uses `MultiServerMCPClient` from `langchain-mcp-adapters`.

The current configuration contains:

```text
tavily
aviationstack
weather
```

---

# 🔎 1. Tavily MCP

The Hotel Agent uses Tavily through MCP for web-based hotel research.

```text
Hotel Agent
     │
     ▼
MCP Client
     │
     ▼
Tavily MCP
     │
     ▼
Tavily Search
     │
     ▼
Hotel Research
     │
     ▼
TravelState
```

The Tavily MCP server is connected through a **streamable HTTP transport**.

The application discovers the `tavily_search` tool and invokes it asynchronously.

---

# ✈️ 2. AviationStack MCP

The Flight Agent accesses AviationStack through an MCP server.

```text
Flight Agent
     │
     ▼
MCP Client
     │
     ▼
AviationStack MCP
     │
     ▼
AviationStack
     │
     ▼
Flight / Airport Information
     │
     ▼
TravelState
```

The AviationStack MCP server is launched locally using:

```text
uvx aviationstack-mcp
```

The MCP client communicates with this server through **stdio transport**.

The current implementation loads AviationStack tools independently and uses tools such as:

```text
list_airports
list_airlines
```

This separation also means that an AviationStack connection problem does not have to prevent the other MCP integrations from being initialized.

---

# 🌤️ 3. Custom Weather MCP Server

This version also introduces a custom Weather MCP server:

```text
custom_weather_mcp_server.py
```

The server exposes weather capabilities to the application through MCP.

The Weather Agent uses:

```text
get_current_weather
get_forecast
```

Conceptually:

```text
Weather Agent
      │
      ▼
  MCP Client
      │
      ▼
Weather MCP Server
      │
      ▼
 OpenWeather
      │
      ▼
Current Weather
+
Forecast
```

The server runs locally using the same Python environment as the main application.

---

# 🧩 MCP Client

The main MCP integration is implemented in:

```text
mcp_client.py
```

The client uses:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
```

The client maintains connections to:

```text
tavily
aviationstack
weather
```

The application can load tools from each server independently.

This is useful for failure isolation.

For example:

```text
Tavily MCP fails
       │
       ▼
Hotel research unavailable

BUT

AviationStack MCP
       │
       ▼
Can still initialize independently
```

Similarly, the Weather MCP server can be initialized separately.

---

# 🧠 Multi-Agent Architecture

The system contains five specialized agents.

```text
┌───────────────────────────────────────────────┐
│              TripPlanner AI                   │
│                                               │
│  ┌───────────────┐                            │
│  │ Flight Agent  │──────► AviationStack MCP   │
│  └───────┬───────┘                            │
│          │                                    │
│  ┌───────▼───────┐                            │
│  │ Hotel Agent   │──────► Tavily MCP          │
│  └───────┬───────┘                            │
│          │                                    │
│  ┌───────▼───────┐                            │
│  │ Weather Agent │──────► Weather MCP         │
│  └───────┬───────┘                            │
│          │                                    │
│  ┌───────▼──────────┐                         │
│  │ Itinerary Agent  │──────► Groq             │
│  └───────┬──────────┘                         │
│          │                                    │
│  ┌───────▼──────────┐                         │
│  │ Final Response   │──────► Groq             │
│  │ Agent            │                         │
│  └──────────────────┘                         │
└───────────────────────────────────────────────┘
```

---

# ✈️ Flight Agent

### Responsibility

The Flight Agent handles flight-related research.

It:

1. Receives the user's travel request.
2. Accesses AviationStack through MCP.
3. Retrieves available airport and airline information.
4. Provides the information to the LLM.
5. Stores the resulting flight guidance in `TravelState`.

Conceptually:

```text
User Query
    │
    ▼
Flight Agent
    │
    ▼
AviationStack MCP
    │
    ├── list_airports
    │
    └── list_airlines
    │
    ▼
Groq
    │
    ▼
Flight Research
```

---

# 🏨 Hotel Agent

### Responsibility

The Hotel Agent performs accommodation research.

```text
User Query
    │
    ▼
Hotel Agent
    │
    ▼
Tavily MCP
    │
    ▼
Web Search
    │
    ▼
Hotel Results
```

The agent sends a hotel-focused query to the Tavily MCP search tool and stores the results in the shared state.

---

# 🌤️ Weather Agent

### Responsibility

The Weather Agent retrieves current weather and forecast information.

First, the destination is extracted from the user's request.

Then:

```text
Destination
     │
     ▼
Weather Agent
     │
     ├──────────────► Current Weather
     │
     └──────────────► Forecast
                         │
                         ▼
                    Weather MCP
```

The results are stored in:

```python
weather_results
```

---

# 🗓️ Itinerary Agent

The Itinerary Agent receives the information accumulated by previous agents.

```text
User Requirements
       +
Flight Research
       +
Hotel Research
       +
Weather Information
       │
       ▼
Itinerary Agent
       │
       ▼
    Groq LLM
       │
       ▼
Day-by-Day Itinerary
```

The itinerary is designed to be:

* Practical
* Budget-aware
* Easy to follow
* Based on the collected travel information

---

# 📝 Final Response Agent

The Final Response Agent combines all collected information.

```text
User Request
     +
Flights
     +
Hotels
     +
Weather
     +
Itinerary
     │
     ▼
Final Response Agent
     │
     ▼
  Groq LLM
     │
     ▼
Formatted Travel Plan
```

The final response is structured into:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Weather Information
5. Day-by-Day Itinerary
6. Estimated Budget
7. Final Recommendations

---

# 📦 Shared `TravelState`

LangGraph provides a shared state between the agents.

The current state contains:

```python
TravelState = {
    "messages": [...],
    "user_query": "...",
    "flight_results": "...",
    "hotel_results": "...",
    "weather_results": "...",
    "itinerary": "...",
    "llm_calls": 0
}
```

The state progressively grows:

```text
Initial State
     │
     ▼
+ flight_results
     │
     ▼
+ hotel_results
     │
     ▼
+ weather_results
     │
     ▼
+ itinerary
     │
     ▼
+ final response
```

This allows downstream agents to use information produced by earlier stages.

---

# 💾 Conversation Persistence

TripPlanner uses PostgreSQL for persistent LangGraph checkpointing.

```mermaid
flowchart LR

    UI["🌐 Browser"]

    API["⚡ FastAPI"]

    LG["🧠 LangGraph"]

    CP["💾 AsyncPostgresSaver"]

    DB[("🐘 PostgreSQL")]

    UI -->|"message + thread_id"| API
    API --> LG
    LG --> CP
    CP --> DB

    DB -. checkpoint .-> CP
    CP -. restore state .-> LG
```

The application uses `thread_id` to identify a conversation.

For example:

### First request

```json
{
  "message": "Plan a trip to Japan",
  "thread_id": null
}
```

The backend creates a thread ID.

A follow-up request can reuse that thread:

```json
{
  "message": "Make the hotel cheaper",
  "thread_id": "existing-thread-id"
}
```

This allows the application to maintain context across multiple requests.

---

# 🌐 FastAPI Backend

FastAPI provides the HTTP boundary between the frontend and the AI system.

```text
Browser
   │
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ├── MCP tools
   ├── Groq
   └── PostgreSQL
```

The browser does not directly communicate with the MCP servers or external APIs.

---

# 📡 API

| Method | Endpoint      | Purpose                 |
| ------ | ------------- | ----------------------- |
| `GET`  | `/`           | Serve the web interface |
| `GET`  | `/health`     | Health check            |
| `POST` | `/api/travel` | Generate a travel plan  |

### Request

```json
{
  "message": "Plan a 5 day trip to Japan",
  "thread_id": null
}
```

### Follow-up request

```json
{
  "message": "Make it cheaper",
  "thread_id": "existing-thread-id"
}
```

### Response

```json
{
  "success": true,
  "thread_id": "existing-thread-id",
  "answer": "## Your Japan Travel Plan...",
  "flight_results": "...",
  "hotel_results": "...",
  "weather_results": "...",
  "itinerary": "...",
  "llm_calls": 5
}
```

---

# 🖥️ Frontend

The frontend is implemented using:

```text
templates/
└── index.html

static/
├── style.css
└── script.js
```

### `index.html`

Provides the web interface.

### `style.css`

Controls the application's:

* Layout
* Theme
* Cards
* Buttons
* Responsive design
* Agent workflow presentation

### `script.js`

Handles:

* User input
* API requests
* Loading states
* Error messages
* Thread IDs
* Markdown rendering
* Copying results
* PDF generation

---

# 📁 Project Structure

```text
TripPlaner-AI--A-multi-Agent-Travel-Planner-With-MCP/
│
├── app.py
│   └── FastAPI application
│
├── backend.py
│   ├── TravelState
│   ├── LangGraph agents
│   ├── graph definition
│   └── PostgreSQL checkpointing
│
├── mcp_client.py
│   ├── MultiServerMCPClient
│   ├── Tavily MCP
│   ├── AviationStack MCP
│   └── Weather MCP
│
├── custom_weather_mcp_server.py
│   └── Custom Weather MCP server
│
├── mcp_client_test.py
│   └── MCP client testing
│
├── test.py
│   └── Application testing
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── tools/
│   └── Supporting project tools
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/travel_db

GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

OPENWEATHER_API_KEY=your_openweather_api_key
```

### Variables

| Variable                | Purpose                           |
| ----------------------- | --------------------------------- |
| `DATABASE_URL`          | PostgreSQL connection             |
| `GROQ_API_KEY`          | Groq LLM authentication           |
| `TAVILY_API_KEY`        | Tavily MCP authentication         |
| `AVIATIONSTACK_API_KEY` | AviationStack MCP authentication  |
| `OPENWEATHER_API_KEY`   | Custom Weather MCP authentication |

### ⚠️ Security

Never commit `.env`.

Add it to `.gitignore`:

```text
.env
```

---

# 🚀 Local Setup

## Prerequisites

Install:

* Python 3.11+
* PostgreSQL
* Git
* `uv` for the AviationStack MCP server

You also need API keys for:

* Groq
* Tavily
* AviationStack
* OpenWeather

---

## 1. Clone the repository

```bash
git clone https://github.com/itsapexdanav/TripPlaner-AI--A-multi-Agent-Travel-Planner-With-MCP.git

cd TripPlaner-AI--A-multi-Agent-Travel-Planner-With-MCP
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🔌 MCP Setup

The application automatically configures three MCP integrations.

### Tavily

Uses Streamable HTTP:

```text
https://mcp.tavily.com/mcp/
```

The Tavily API key is supplied through the environment configuration.

### AviationStack

Uses stdio:

```text
uvx aviationstack-mcp
```

The application launches the MCP server through `uvx`.

### Weather

Uses the local Python environment:

```text
custom_weather_mcp_server.py
```

The application resolves the server path automatically from the project directory.

---

# 🗄️ PostgreSQL Setup

Create a PostgreSQL database.

```sql
CREATE DATABASE travel_db;
```

Configure:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/travel_db
```

The backend creates an asynchronous PostgreSQL connection pool and initializes the LangGraph checkpoint store during application startup.

---

# ▶️ Run the Application

Start the application:

```bash
python app.py
```

Or:

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# 🐳 Docker

Build the image:

```bash
docker build -t tripplanner .
```

Run:

```bash
docker run -p 8000:8000 --env-file .env tripplanner
```

Then open:

```text
http://127.0.0.1:8000/
```

The PostgreSQL database and external services must still be reachable from the container.

---

# 💡 Example Prompts

### 🇯🇵 Japan

```text
Plan a 7-day trip to Japan with a budget of $2000.
Include flights, hotels, weather and major attractions.
```

### 🇦🇪 Dubai

```text
Plan a 4-day trip to Dubai for two people.
My budget is $1200.
```

### 🇹🇭 Thailand

```text
Create a 6-day Thailand itinerary with affordable hotels
and interesting places to visit.
```

### ✈️ Flight-focused

```text
Plan a trip from Delhi to Tokyo and include flight
information and a practical itinerary.
```

### 🌤️ Weather-focused

```text
Plan a trip to Tokyo and include weather information
and recommendations based on the forecast.
```

### 💰 Budget-focused

```text
Plan a 5-day international trip under $1000.
Prioritize affordable hotels and activities.
```

### 🔄 Follow-up

After generating a plan:

```text
Make the itinerary cheaper.
```

or:

```text
Add more sightseeing activities.
```

or:

```text
Reduce the number of hotel changes.
```

---

# 🔁 Complete Request Lifecycle

```mermaid
sequenceDiagram

    actor User
    participant UI as TripPlanner UI
    participant API as FastAPI
    participant LG as LangGraph
    participant MCP as MCP Client
    participant F as Flight Agent
    participant H as Hotel Agent
    participant W as Weather Agent
    participant I as Itinerary Agent
    participant R as Final Agent
    participant DB as PostgreSQL
    participant LLM as Groq

    User->>UI: Enter travel request
    UI->>API: POST /api/travel

    API->>LG: Invoke graph + thread_id

    LG->>DB: Load checkpoint
    DB-->>LG: Previous state

    LG->>F: Execute Flight Agent
    F->>MCP: Request AviationStack tools
    MCP-->>F: Airport / airline information
    F->>LLM: Generate flight guidance
    LLM-->>F: Flight research
    F-->>LG: Update TravelState

    LG->>H: Execute Hotel Agent
    H->>MCP: Request Tavily search
    MCP-->>H: Search results
    H-->>LG: Update TravelState

    LG->>W: Execute Weather Agent
    W->>MCP: Request weather tools
    MCP-->>W: Current weather + forecast
    W-->>LG: Update TravelState

    LG->>I: Execute Itinerary Agent
    I->>LLM: Generate itinerary
    LLM-->>I: Itinerary
    I-->>LG: Update TravelState

    LG->>R: Execute Final Agent
    R->>LLM: Generate final response
    LLM-->>R: Final answer
    R-->>LG: Update TravelState

    LG->>DB: Save checkpoint

    LG-->>API: Final state
    API-->>UI: JSON response
    UI-->>User: Render travel plan
```

---

# 🧠 Important Design Decisions

## 1. MCP for External Tool Integration

The new implementation separates external tool access from the main application logic.

```text
LangGraph
    │
    ▼
MCP Client
    │
    ├── Tavily MCP
    ├── AviationStack MCP
    └── Weather MCP
```

This provides a standardized tool boundary between the AI application and external capabilities.

---

## 2. LangGraph for Orchestration

LangGraph controls the workflow:

```text
START
  ↓
Flight Agent
  ↓
Hotel Agent
  ↓
Weather Agent
  ↓
Itinerary Agent
  ↓
Final Agent
  ↓
END
```

The graph provides explicit control over execution order and shared state.

---

## 3. Shared State

Instead of manually passing separate variables between agents, the workflow maintains a shared `TravelState`.

```text
TravelState
    │
    ├── user_query
    ├── flight_results
    ├── hotel_results
    ├── weather_results
    ├── itinerary
    ├── messages
    └── llm_calls
```

---

## 4. Independent MCP Initialization

The MCP client loads the external integrations independently.

This is important because one external service can fail without necessarily preventing the other MCP integrations from loading.

For example:

```text
AviationStack MCP ❌

Tavily MCP       ✅
Weather MCP      ✅
```

The system can identify the failing integration rather than treating every tool connection as one large dependency.

---

## 5. FastAPI as the Backend Boundary

The browser communicates only with FastAPI.

```text
Browser
   │
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ├── MCP
   ├── Groq
   └── PostgreSQL
```

This keeps service credentials and orchestration logic on the backend.

---

## 6. PostgreSQL for Persistent State

LangGraph checkpoints are stored in PostgreSQL rather than only in process memory.

This allows conversation state to survive application restarts and supports thread-based conversations.

---

# 🛡️ Failure Handling

The system depends on several external components.

```text
                  TripPlanner
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
   Tavily MCP   AviationStack MCP  Weather MCP
       │              │              │
       ▼              ▼              ▼
    Failure        Failure         Failure
```

Examples:

```text
Tavily unavailable
        ↓
Hotel research unavailable
```

```text
AviationStack unavailable
        ↓
Flight research unavailable
```

```text
Weather MCP unavailable
        ↓
Weather information unavailable
```

```text
Groq unavailable
        ↓
LLM generation unavailable
```

```text
PostgreSQL unavailable
        ↓
Checkpointing unavailable
```

The current implementation catches tool/agent errors and returns fallback information rather than silently hiding the failure.

For production, the system can be extended with:

* Retries
* Timeouts
* Circuit breakers
* Rate limiting
* Caching
* Structured errors
* Health checks
* Observability
* MCP server monitoring

---

# 🧪 Testing

The repository includes:

```text
mcp_client_test.py
test.py
```

The MCP client tests can be used to verify MCP server/tool connectivity separately from the complete travel workflow.

A production-grade testing structure could eventually become:

```text
tests/
├── unit/
│   ├── test_mcp_client.py
│   ├── test_flight_agent.py
│   ├── test_hotel_agent.py
│   ├── test_weather_agent.py
│   └── test_agents.py
│
├── integration/
│   ├── test_tavily_mcp.py
│   ├── test_aviation_mcp.py
│   ├── test_weather_mcp.py
│   └── test_travel_workflow.py
│
└── api/
    └── test_api.py
```

---

# 🧠 Engineering Concepts Demonstrated

### AI Engineering

* Multi-agent systems
* LangGraph orchestration
* LLM-powered planning
* Tool calling
* MCP
* Shared agent state
* Multi-turn conversations

### MCP

* MCP client architecture
* MCP server integration
* Streamable HTTP transport
* stdio transport
* Tool discovery
* Tool invocation
* Custom MCP server development

### Backend Engineering

* FastAPI
* REST APIs
* Request/response models
* Environment configuration
* External service integration
* Async Python

### Distributed-System Concepts

* Service boundaries
* External dependency failures
* Persistent state
* Connection pools
* Checkpointing
* Failure isolation
* Request context

### Database

* PostgreSQL
* Async connection pooling
* LangGraph checkpoint persistence
* Thread-based sessions

### DevOps

* Docker
* Environment-based configuration
* Git/GitHub
* Containerized deployment

---

# 🔮 Future Improvements

## MCP

* [ ] Add more MCP servers
* [ ] Currency conversion MCP
* [ ] Maps MCP
* [ ] Places/activities MCP
* [ ] Hotel-specific MCP
* [ ] Booking-related MCP integrations
* [ ] MCP server health monitoring
* [ ] Better MCP failure isolation

## Agents

* [ ] Parallel flight + hotel + weather research
* [ ] Dedicated budget agent
* [ ] Activity research agent
* [ ] Better agent routing
* [ ] Follow-up/refinement agent
* [ ] Human-in-the-loop approval

## Reliability

* [ ] Retry mechanisms
* [ ] Timeouts
* [ ] Circuit breakers
* [ ] Rate limiting
* [ ] Caching
* [ ] Graceful degradation
* [ ] Structured logging

## AI Observability

* [ ] Agent tracing
* [ ] MCP tool tracing
* [ ] LLM token tracking
* [ ] Latency metrics
* [ ] MCP tool latency metrics
* [ ] Cost tracking
* [ ] Agent evaluation

## Production

* [ ] Authentication
* [ ] User accounts
* [ ] CI/CD
* [ ] Cloud deployment
* [ ] Monitoring
* [ ] Redis caching
* [ ] Background workers
* [ ] Distributed MCP infrastructure

---

# ⚠️ Limitations

TripPlanner AI depends on external services and LLM-generated information.

Therefore:

* Flight information can change.
* Flight availability can change.
* Web search results can change.
* Weather forecasts can change.
* External MCP servers can become unavailable.
* API services can experience downtime or rate limits.
* LLM-generated itineraries may contain inaccurate information.

TripPlanner AI should be treated as a **travel planning assistant**, not the final authority for bookings or travel requirements.

Always verify important information with official airlines, hotels, government authorities, and other relevant sources before making bookings.

---

# 🔐 Security

Never place API keys directly inside Python source code.

Use environment variables:

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
AVIATIONSTACK_API_KEY=...
OPENWEATHER_API_KEY=...
DATABASE_URL=...
```

Keep:

```text
.env
```

out of Git.

For Docker deployments, provide secrets through environment configuration rather than baking them into the image.

---

# 🚧 Project Evolution

This repository represents the **MCP-based evolution** of the TripPlanner project.

The earlier implementation focused on direct external API integrations.

The current implementation introduces an MCP-based tool layer:

```text
Previous Architecture

LangGraph
    │
    ├── Direct API calls
    ├── Direct API calls
    └── Direct API calls
```

The current architecture:

```text
Current Architecture

LangGraph
    │
    ▼
MCP Client
    │
    ├── Tavily MCP
    ├── AviationStack MCP
    └── Weather MCP
```

The goal is to make the travel-planning system more modular and demonstrate how **MCP can act as a standardized tool boundary for AI agents**.

---

# 📚 Tech Stack

| Layer               | Technology                        |
| ------------------- | --------------------------------- |
| Language            | Python 3.11+                      |
| API                 | FastAPI                           |
| Agent Orchestration | LangGraph                         |
| LLM Framework       | LangChain                         |
| LLM                 | Groq                              |
| Tool Protocol       | Model Context Protocol            |
| MCP Client          | LangChain MCP Adapters            |
| Flight Data         | AviationStack MCP                 |
| Hotel Research      | Tavily MCP                        |
| Weather             | Custom Weather MCP + OpenWeather  |
| Database            | PostgreSQL                        |
| Persistence         | LangGraph PostgreSQL Checkpointer |
| Frontend            | HTML + CSS + JavaScript           |
| Templates           | Jinja2                            |
| Containerization    | Docker                            |
| Package Runner      | uvx                               |

---

# 👨‍💻 Author

**Nirmal Singh**

Built as an AI Engineering project to explore:

```text
LLMs
  +
Multi-Agent Systems
  +
LangGraph
  +
MCP
  +
FastAPI
  +
PostgreSQL
  +
External Tools
  +
Docker
```

---

<p align="center">

### ✈️ TripPlanner AI

**From a natural-language travel request to an AI-generated travel plan.**

Built with **Python · FastAPI · LangGraph · MCP · LangChain · Groq · PostgreSQL · Tavily · AviationStack · OpenWeather**

</p>
