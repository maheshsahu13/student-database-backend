from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.ai.nodes import retrieve_students, generate_answer


class ChatState(TypedDict, total=False):
    question: str
    students: list
    answer: str


workflow = StateGraph(ChatState)

workflow.add_node("retrieve_students", retrieve_students)
workflow.add_node("generate_answer", generate_answer)

workflow.add_edge(START, "retrieve_students")
workflow.add_edge("retrieve_students", "generate_answer")
workflow.add_edge("generate_answer", END)

chat_graph = workflow.compile()