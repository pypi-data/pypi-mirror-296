import chainlit as cl
import chainlit.data as cl_data
import orjson
from chainlit.input_widget import Select, Slider, Switch
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from mtmai.agents.states.ctx import get_mtmai_ctx
from mtmai.agents.states.research_state import Outline
from mtmai.core.config import settings
from mtmai.core.db import get_session_v2
from mtmai.core.logging import get_logger
from mtmai.crud import crud
from mtmai.mtlibs.chainlit.data.data import SQLAlchemyDataLayer

cl_data._data_layer = SQLAlchemyDataLayer(conninfo=settings.DATABASE_URL)

logger = get_logger()


async def init_outline(topic: str):
    """初始化大纲"""
    ctx = get_mtmai_ctx()
    parser = PydanticOutputParser(pydantic_object=Outline)
    direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific."
                "\n\nIMPORTANT: Your response must be in valid JSON format. Follow these guidelines:"
                "\n- Use double quotes for all strings"
                "\n- Ensure all keys and values are properly enclosed"
                "\n- Do not include any text outside of the JSON object"
                "\n- Strictly adhere to the following JSON schema:"
                "\n{format_instructions}"
                "\n\nDouble-check your output to ensure it is valid JSON before submitting.",
            ),
            ("user", "topic is: {topic}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    ai_response = await ctx.call_model_chat(direct_gen_outline_prompt, {"topic": topic})

    loaded_data = orjson.loads(ctx.repair_json(ai_response.content))
    outline: Outline = Outline.model_validate(loaded_data)
    return outline


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    # if (username, password) == ("admin", "admin"):
    #     return cl.User(
    #         identifier="admin", metadata={"role": "admin", "provider": "credentials"}
    #     )
    # else:
    #     return None
    db_session = get_session_v2()
    user = crud.authenticate(session=db_session, email=username, password=password)
    if user:
        return cl.User(
            identifier=user.username,
            metadata={"role": "admin", "provider": "credentials"},
        )
    else:
        return None


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    cl.user_session.set("counter", 0)
    public_profiles = [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**, a *1.5T parameter model* trained on 3.5TB of text data.",
            icon="https://picsum.photos/250",
        ),
    ]

    admin_profiles = [
        cl.ChatProfile(
            name="GPT-5",
            markdown_description="The underlying LLM model is **GPT-5**.",
            icon="https://picsum.photos/200",
        ),
    ]

    if current_user.metadata["role"] == "ADMIN":
        return admin_profiles.append(public_profiles)
    else:
        return public_profiles


counter = 0


@cl.on_chat_start
async def chat_start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                initial_index=0,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Slider(
                id="SAI_Steps",
                label="Stability AI - Steps",
                initial=30,
                min=10,
                max=150,
                step=1,
                description="Amount of inference steps performed on image generation.",
            ),
            Slider(
                id="SAI_Cfg_Scale",
                label="Stability AI - Cfg_Scale",
                initial=7,
                min=1,
                max=35,
                step=0.1,
                description="Influences how strongly your generation is guided to match your prompt.",
            ),
            Slider(
                id="SAI_Width",
                label="Stability AI - Image Width",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
            Slider(
                id="SAI_Height",
                label="Stability AI - Image Height",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
        ]
    ).send()

    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(content=f"开始使用 {chat_profile} 聊天").send()
    await cl.Message(
        content="环境准备好了, 你可以开始提问了",
    ).send()
    # if res:
    #     await Message(
    #         content=f"Your name is: {res['content']}.\n",
    #     ).send()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)


@cl.on_chat_end
def end():
    print("goodbye", cl.user_session.get("id"))


@cl.on_message
async def on_message(message: cl.Message):
    app_user = cl.user_session.get("user")

    global counter
    counter += 1
    logger.info(f"Received message {counter} from {app_user.username}")

    topic = message.content

    topic = message.content
    result = await init_outline(topic)
    reply = result.model_dump_json()
    await cl.Message(
        content=f"Received: {reply}",
    ).send()
