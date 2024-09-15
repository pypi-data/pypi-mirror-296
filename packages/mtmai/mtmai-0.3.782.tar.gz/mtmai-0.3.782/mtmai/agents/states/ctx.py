from contextlib import contextmanager
from typing import Annotated, Type

import httpx
import orjson
from json_repair import repair_json
from langchain_core.prompts import PromptTemplate

# from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.channels.context import Context
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import Session

from mtmai.agents.graphs.graph_utils import get_graph_config
from mtmai.agents.retrivers.mtmdoc import MtmDocStore
from mtmai.core.db import getdb
from mtmai.core.logging import get_logger
from mtmai.llm.embedding import get_default_embeddings
from mtmai.models.graph_config import GraphConfig

logger = get_logger()


class AgentContext(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    httpx_session: httpx.Client
    db: Engine
    session: Session
    vectorstore: MtmDocStore
    graph_config: GraphConfig

    def retrive_graph_config(self):
        return self.graph_config

    def load_doc(self):
        return self.vectorstore

    async def call_model_chat(
        self, tpl: PromptTemplate, inputs: dict, structured_output: BaseModel = None
    ):
        llm_chat = self.graph_config.llms.get("chat")
        llm_inst = ChatOpenAI(
            base_url=llm_chat.base_url,
            api_key=llm_chat.api_key,
            model=llm_chat.model,
            temperature=llm_chat.temperature,
            max_tokens=llm_chat.max_tokens,
        )

        messages = await tpl.ainvoke(inputs)
        llm_chain = llm_inst
        # if structured_output:
        #     llm_chain = llm_chain.with_structured_output(
        #         structured_output, include_raw=True
        #     )
        llm_chain = llm_chain.with_retry(stop_after_attempt=5)
        llm_chain = llm_chain.bind(response_format={"type": "json_object"})
        result = await llm_chain.ainvoke(messages)
        return result

    def repair_json(self, json_like_input: str):
        """修复 ai 以非标准的json回复 的 json 字符串"""
        good_json_string = repair_json(json_like_input, skip_json_loads=True)
        return good_json_string

    def load_json_response(
        self, ai_json_resonse_text: str, model_class: Type[BaseModel]
    ) -> Type[BaseModel]:
        repaired_json = self.repair_json(ai_json_resonse_text)
        try:
            loaded_data = orjson.loads(repaired_json)
            return model_class(**loaded_data)
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            raise ValueError(
                f"Failed to parse JSON and create {model_class.__name__} instance"
            ) from e


def get_mtmai_ctx():
    session = httpx.Client()
    db = getdb()
    embedding = get_default_embeddings()
    gconfig = get_graph_config()
    vectorstore = MtmDocStore(session=Session(db), embedding=embedding)
    agent_ctx = AgentContext(
        httpx_session=session,
        db=db,
        session=Session(db),
        vectorstore=vectorstore,
        graph_config=gconfig,
    )
    return agent_ctx


@contextmanager
def make_agent_context(config: RunnableConfig):
    session = httpx.Client()
    db = getdb()
    embedding = get_default_embeddings()
    gconfig = get_graph_config()
    try:
        vectorstore = MtmDocStore(session=Session(db), embedding=embedding)
        yield AgentContext(
            httpx_session=session,
            db=db,
            session=Session(db),
            vectorstore=vectorstore,
            graph_config=gconfig,
        )
    finally:
        session.close()


context = Annotated[AgentContext, Context(make_agent_context)]


class LcHelper:
    def __init__(self, state, config: RunnableConfig = None) -> AgentContext:
        self.state = state
        self.config = config


def get_ctx(state, config: RunnableConfig = None) -> AgentContext:
    ctx = state.get("context")
    return ctx


# def get_lc_helper(state, config: RunnableConfig = None) -> LcHelper:
#     return LcHelper(self.state, self.config)
