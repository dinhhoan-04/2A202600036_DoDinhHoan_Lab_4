"""
agent.py — TravelBuddy AI Agent sử dụng LangGraph
Kiến trúc: Agent Node ↔ Tool Node (vòng lặp ReAct)
"""

import os
import sys
import logging
from datetime import datetime
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

from tools import search_flights, search_hotels, calculate_budget

# ============================================================
# KHỞI TẠO
# ============================================================

load_dotenv()

# Logging rõ ràng — chỉ hiện INFO trở lên
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("TravelBuddy")


# ============================================================
# 1. ĐỌC SYSTEM PROMPT
# ============================================================

def _load_system_prompt() -> str:
    """Đọc system_prompt.txt. Nếu không tìm thấy, dùng fallback tối thiểu."""
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            logger.info("✅ Đọc system_prompt.txt thành công (%d ký tự)", len(content))
            return content
    except FileNotFoundError:
        logger.warning("⚠️ Không tìm thấy system_prompt.txt — dùng prompt mặc định")
        return (
            "Bạn là TravelBuddy, trợ lý du lịch thông minh. "
            "Trả lời bằng tiếng Việt. Chỉ hỗ trợ về du lịch."
        )


SYSTEM_PROMPT: str = _load_system_prompt()


# ============================================================
# 2. KHAI BÁO STATE
# ============================================================

class AgentState(TypedDict):
    """State của Agent — chỉ lưu danh sách messages."""
    messages: Annotated[list, add_messages]


# ============================================================
# 3. KHỞI TẠO LLM VÀ TOOLS
# ============================================================

TOOLS_LIST = [search_flights, search_hotels, calculate_budget]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,        # Thấp → nhất quán, ít hallucination
    max_tokens=1500,
    timeout=30,
    max_retries=2,
)

llm_with_tools = llm.bind_tools(TOOLS_LIST)

logger.info("✅ Khởi tạo LLM (gpt-4o-mini) + %d tools thành công", len(TOOLS_LIST))


# ============================================================
# 4. AGENT NODE
# ============================================================

def agent_node(state: AgentState) -> dict:
    """
    Node chính — LLM suy nghĩ và quyết định:
    - Trả lời trực tiếp, HOẶC
    - Gọi một/nhiều tool
    """
    messages = state["messages"]

    # Inject ngày giờ thực tế vào SystemMessage — cập nhật mỗi lần gọi
    now = datetime.now()
    DAYS_VI = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    day_name = DAYS_VI[now.weekday()]
    date_ctx = (
        f"\n\n<current_datetime>"
        f"Hôm nay là {day_name}, ngày {now.day:02d}/{now.month:02d}/{now.year}, "
        f"giờ Việt Nam: {now.strftime('%H:%M')}."
        f"</current_datetime>"
    )
    system_msg = SystemMessage(content=SYSTEM_PROMPT + date_ctx)

    # Thay SystemMessage cũ (nếu có) hoặc thêm vào đầu
    if messages and isinstance(messages[0], SystemMessage):
        messages = [system_msg] + list(messages[1:])
    else:
        messages = [system_msg] + list(messages)

    logger.info("🤖 Agent đang xử lý (%d messages trong context)...", len(messages))

    try:
        response: AIMessage = llm_with_tools.invoke(messages)
    except Exception as e:
        logger.error("❌ Lỗi gọi LLM: %s", str(e))
        error_msg = AIMessage(
            content="⚠️ Xin lỗi, tôi gặp sự cố kỹ thuật. Vui lòng thử lại sau giây lát."
        )
        return {"messages": [error_msg]}

    # Logging chi tiết
    if response.tool_calls:
        for tc in response.tool_calls:
            logger.info("🔧 Gọi tool: %s(%s)", tc["name"], tc["args"])
    else:
        logger.info("💬 Trả lời trực tiếp (không gọi tool)")

    return {"messages": [response]}


# ============================================================
# 5. XÂY DỰNG GRAPH
# ============================================================

def build_graph() -> StateGraph:
    """Xây dựng và compile LangGraph Agent."""
    builder = StateGraph(AgentState)

    # Thêm nodes
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS_LIST))

    # Khai báo edges
    builder.add_edge(START, "agent")

    # Conditional edge: agent → tools NẾU có tool_calls, ngược lại → END
    builder.add_conditional_edges(
        "agent",
        tools_condition,   # built-in condition: kiểm tra tool_calls
    )

    # Sau khi tools chạy xong → quay về agent để tổng hợp
    builder.add_edge("tools", "agent")

    graph = builder.compile()
    logger.info("✅ LangGraph compiled thành công")
    return graph


# Biên dịch graph một lần duy nhất khi import module
graph = build_graph()


# ============================================================
# 6. HÀM CHAT WRAPPER
# ============================================================

def chat(user_input: str, conversation_history: list | None = None) -> tuple[str, list]:
    """
    Gửi tin nhắn và nhận phản hồi từ Agent.
    Trả về: (response_text, updated_history)
    Hỗ trợ multi-turn conversation.
    """
    if conversation_history is None:
        conversation_history = []

    # Thêm message của user vào history
    new_message = HumanMessage(content=user_input)
    messages_in = conversation_history + [new_message]

    try:
        result = graph.invoke({"messages": messages_in})
        final_message: AIMessage = result["messages"][-1]
        response_text: str = final_message.content or ""

        # Cập nhật history đầy đủ (bao gồm cả tool messages ở giữa)
        updated_history = result["messages"]

        return response_text, updated_history

    except Exception as e:
        logger.error("❌ Lỗi trong graph.invoke: %s", str(e))
        error_response = (
            "⚠️ Đã xảy ra lỗi không mong muốn. Vui lòng thử lại."
        )
        return error_response, conversation_history + [new_message]


# ============================================================
# 7. CHAT LOOP — Giao diện CLI
# ============================================================

def main() -> None:
    """Vòng lặp chat tương tác trên terminal."""
    print("=" * 60)
    print("  TravelBuddy — Trợ lý Du lịch Thông minh 🌏")
    print("  Gõ 'quit' / 'exit' / 'q' để thoát")
    print("=" * 60)
    print()

    conversation_history: list = []

    while True:
        try:
            user_input = input("Bạn: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nTạm biệt! Chúc bạn có chuyến đi vui vẻ! ✈️")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q", "thoát"):
            print("TravelBuddy: Tạm biệt! Chúc bạn có chuyến đi tuyệt vời! ✈️🌟")
            break

        print("\nTravelBuddy đang suy nghĩ...\n")

        response, conversation_history = chat(user_input, conversation_history)

        print(f"TravelBuddy: {response}")
        print()


if __name__ == "__main__":
    main()
