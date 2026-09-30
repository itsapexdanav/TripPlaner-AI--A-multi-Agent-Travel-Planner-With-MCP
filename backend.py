import os
import certifi
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict, Annotated
import operator
import uuid

from psycopg_pool import AsyncConnectionPool

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from mcp_client import (
    tavily_mcp_search,
    aviation_mcp_call,
    extract_destination,
    forecast_mcp_search,
    weather_mcp_search,
)


# ============================================================
# DATABASE
# ============================================================

def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. "
            "Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url


# ============================================================
# GROQ
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY
)


# ============================================================
# STATE
# ============================================================

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    weather_results: str


# ============================================================
# FLIGHT AGENT
# ============================================================

FLIGHT_AGENT_PROMPT = """
You are a travel flight expert.

User Query:
{query}

Airport Information:
{airport_data}

Airline Information:
{airline_data}

Generate:

1. Likely departure airport
2. Likely arrival airport
3. Airlines serving this route
4. Typical flight duration
5. Estimated airfare range
6. Peak season pricing warning
7. Booking advice

Return concise travel guidance.
"""


async def flight_agent(state: TravelState):

    print("\nINSIDE FLIGHT AGENT\n")

    query = state["user_query"]

    try:

        airports = await aviation_mcp_call(
            "list_airports"
        )

        airlines = await aviation_mcp_call(
            "list_airlines"
        )

        print("\nAIRPORTS:", airports)
        print("\nAIRLINES:", airlines)

        prompt = FLIGHT_AGENT_PROMPT.format(
            query=query,
            airport_data=str(airports)[:3000],
            airline_data=str(airlines)[:3000]
        )

        response = llm.invoke([
            SystemMessage(
                content="You are an expert travel flight planner."
            ),
            HumanMessage(
                content=prompt
            )
        ])

        flight_data = response.content

    except Exception as e:

        print(
            f"\nFlight agent error: {e}\n"
        )

        flight_data = (
            f"Flight information unavailable: {str(e)}"
        )

    return {
        "flight_results": flight_data,

        "messages": [
            AIMessage(
                content="Flight recommendations generated"
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# ============================================================
# HOTEL AGENT
# ============================================================

async def hotel_agent(state: TravelState):

    query = (
        f"Best hotels for {state['user_query']}"
    )

    try:

        hotel_results = await tavily_mcp_search(
            query
        )

    except Exception as e:

        print(
            f"\nHotel agent error: {e}\n"
        )

        hotel_results = (
            f"Hotel information unavailable: {str(e)}"
        )

    return {
        "hotel_results": hotel_results,

        "messages": [
            AIMessage(
                content="Hotel information fetched."
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# ============================================================
# WEATHER AGENT
# ============================================================

async def weather_agent(state: TravelState):

    city = extract_destination(
        state["user_query"]
    )

    print(
        f"\nWEATHER DESTINATION: {city}\n"
    )

    try:

        weather_data = await weather_mcp_search(
            city
        )

        forecast_data = await forecast_mcp_search(
            city
        )

        weather_results = f"""
Current Weather:
{weather_data}

Forecast:
{forecast_data}
"""

    except Exception as e:

        print(
            f"\nWeather agent error: {e}\n"
        )

        weather_results = (
            f"Weather information unavailable: {str(e)}"
        )

    return {
        "weather_results": weather_results,

        "messages": [
            AIMessage(
                content="Weather information fetched"
            )
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# ============================================================
# ITINERARY AGENT
# ============================================================

def itinerary_agent(state: TravelState):

    prompt = f"""
Create a complete travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}

Weather Results:
{state['weather_results']}

Make the itinerary practical, budget-aware, and easy to follow.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner."
        ),
        HumanMessage(
            content=prompt
        )
    ])

    return {
        "itinerary": response.content,

        "messages": [
            response
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# ============================================================
# FINAL RESPONSE AGENT
# ============================================================

def final_agent(state: TravelState):

    final_prompt = f"""
Generate the final travel response for the user.

User Request:
{state['user_query']}

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Weather:
{state['weather_results']}

Itinerary:
{state['itinerary']}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Weather Information
5. Day-by-Day Itinerary
6. Estimated Budget
7. Final Recommendations

Important:
- Be clear and practical.
- Mention that live flight API may not provide ticket prices if pricing is unavailable.
- Include weather-based travel advice.
- Keep the response useful for real travel planning.
"""

    response = llm.invoke([
        SystemMessage(
            content="You are a professional AI travel booking assistant."
        ),
        HumanMessage(
            content=final_prompt
        )
    ])

    return {
        "messages": [
            response
        ],

        "llm_calls": (
            state.get("llm_calls", 0) + 1
        )
    }


# ============================================================
# BUILD GRAPH
# ============================================================

graph = StateGraph(TravelState)


graph.add_node(
    "flight_agent",
    flight_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "weather_agent",
    weather_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)


# ============================================================
# GRAPH FLOW
# ============================================================

graph.add_edge(
    START,
    "flight_agent"
)

graph.add_edge(
    "flight_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "weather_agent"
)

graph.add_edge(
    "weather_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)


# ============================================================
# ASYNC POSTGRES CHECKPOINTER
# ============================================================

DATABASE_URL = get_database_url()

db_pool = None
checkpointer = None
travel_graph = None


async def initialize_backend():

    global db_pool
    global checkpointer
    global travel_graph

    print("\n================================")
    print("Initializing PostgreSQL")
    print("================================")

    db_pool = AsyncConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=10,
        kwargs={
            "autocommit": True,
            "prepare_threshold": 0,
        },
        open=False,
    )

    await db_pool.open()

    print("PostgreSQL connection pool opened.")

    checkpointer = AsyncPostgresSaver(
        db_pool
    )

    await checkpointer.setup()

    print("PostgreSQL checkpointer initialized.")

    travel_graph = graph.compile(
        checkpointer=checkpointer
    )

    print("LangGraph compiled successfully.")


async def shutdown_backend():

    global db_pool

    if db_pool is not None:

        print("\n================================")
        print("Closing PostgreSQL pool")
        print("================================")

        await db_pool.close()

        print("PostgreSQL connection pool closed.")


# ============================================================
# FASTAPI ENTRY POINT
# ============================================================

async def run_travel_agent(
    user_input: str,
    thread_id: str | None = None
):

    global travel_graph

    if travel_graph is None:
        raise RuntimeError(
            "Travel graph is not initialized. "
            "FastAPI startup has not completed."
        )

    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await travel_graph.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content=user_input
                )
            ],

            "user_query": user_input,

            "flight_results": "",

            "hotel_results": "",

            "weather_results": "",

            "itinerary": "",

            "llm_calls": 0
        },

        config=config
    )

    final_answer = (
        result["messages"][-1].content
    )

    return {
        "thread_id": thread_id,

        "answer": final_answer,

        "flight_results": result.get(
            "flight_results",
            ""
        ),

        "hotel_results": result.get(
            "hotel_results",
            ""
        ),

        "weather_results": result.get(
            "weather_results",
            ""
        ),

        "itinerary": result.get(
            "itinerary",
            ""
        ),

        "llm_calls": result.get(
            "llm_calls",
            0
        )
    }