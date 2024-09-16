import logging

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

# from mtmai.models.chat import ChatInput, MtmChatMessage, MtmChatMessageBase
from mtmai.models.chat import ChatFeedback, ChatStep, ChatThread

logger = logging.getLogger()


# async def user_threads(session:AsyncSession, user_id:str,thread_id:str, limit=100):
async def user_threads(
    session: AsyncSession, user_id: str, thread_id: str, limit: int = 100
):
    query = (
        select(ChatThread)
        .where((ChatThread.user_id == user_id) | (ChatThread.id == thread_id))
        .order_by(desc(ChatThread.created_at))
        .limit(limit)
    )

    result = await session.execute(query)
    user_threads = result.scalars().all()

    if not user_threads:
        return None

    thread_ids = [thread.id for thread in user_threads]

    steps_feedbacks_query = (
        select(ChatStep, ChatFeedback)
        .join(ChatFeedback, ChatStep.id == ChatFeedback.for_id, isouter=True)
        .where(ChatStep.thread_id.in_(thread_ids))
        .order_by(ChatStep.created_at)
    )

    steps_feedbacks_result = await session.exec(steps_feedbacks_query)
    steps_feedbacks = steps_feedbacks_result.all()

    threads_dict = []
    for thread in user_threads:
        thread_dict = {
            "id": thread.id,
            "createdAt": thread.created_at,
            "name": thread.name,
            "userId": thread.user_id,
            "userIdentifier": thread.user_identifier,
            "tags": thread.tags,
            "metadata": thread.metadata,
            "steps": [],
        }

        for step, feedback in steps_feedbacks:
            if step.thread_id == thread.id:
                step_dict = {
                    "id": step.id,
                    "name": step.name,
                    "type": step.type,
                    "threadId": step.thread_id,
                    "parentId": step.parent_id,
                    "streaming": step.streaming,
                    "waitForAnswer": step.wait_for_answer,
                    "isError": step.is_error,
                    "metadata": step.metadata,
                    "tags": step.tags,
                    "input": step.input,
                    "output": step.output,
                    "createdAt": step.created_at,
                    "start": step.start,
                    "end": step.end,
                    "generation": step.generation,
                    "showInput": step.show_input,
                    "language": step.language,
                    "indent": step.indent,
                    "feedback": {
                        "value": feedback.value if feedback else None,
                        "comment": feedback.comment if feedback else None,
                    },
                }
                thread_dict["steps"].append(step_dict)

        threads_dict.append(thread_dict)

    return threads_dict


# class ChatSubmitPublic(BaseModel):
#     chat_id: str | None = None
#     agent_name: str
#     messages: list[MtmChatMessageBase]


# def submit_chat_messages(
#     *, db: Session, data: ChatSubmitPublic, owner_id: str
# ) -> Account:
#     chat_input_item = ChatInput()
#     chat_input_item.agent_id = data.agent_name
#     chat_input_item.user_id = owner_id
#     chat_input_item.id = data.chat_id
#     # if not data.chat_id:
#     #     # 是全新的对话
#     #     db.add(chat_input_item)
#     #     db.commit()
#     #     db.refresh(chat_input_item)
#     #     logger.info("创建了 chat input %s", chat_input_item.id)
#     # else:
#     # 现有对话
#     chat_input_get = get_chat_input(db, data.chat_id)
#     if not chat_input_get:
#         # msg = "获取 chat input 记录出错"
#         # raise Exception(msg)
#         # 是全新的对话
#         db.add(chat_input_item)
#         db.commit()
#         db.refresh(chat_input_item)
#         logger.info("创建了 chat input %s", chat_input_item.id)

#     db.add_all(
#         [
#             MtmChatMessage(
#                 content=x.content,
#                 # chat=chat_input_item,
#                 chat_id=chat_input_item.id,
#                 role=x.role,
#             )
#             for x in data.messages
#         ]
#     )
#     db.commit()
#     return chat_input_item


# def append_chat_messages(db: Session, chat_messages: list[MtmChatMessage]):
#     """批量追加聊天历史"""
#     logger.info("追加聊天历史, 消息数量: %d", len(chat_messages))
#     db.add_all(chat_messages)


# def get_chat_input(db: Session, id: str):
#     statement = select(ChatInput).where(ChatInput.id == id)
#     result = db.exec(statement=statement).first()
#     return result


# def get_conversation_messages(
#     db: Session,
#     conversation_id: str,
#     offset: int = 0,
#     limit: int = 100,
# ):
#     """
#     获取 对话的消息记录
#     """
#     if limit > 1000:
#         msg = "limit too large"
#         raise Exception(msg)  # noqa: TRY002
#     if not conversation_id:
#         msg = "require conversation_id"
#         raise Exception(msg)  # noqa: TRY002
#     chat_messages = db.exec(
#         select(MtmChatMessage)
#         .where(MtmChatMessage.chat_id == conversation_id)
#         .order_by(desc(MtmChatMessage.created_at))
#         .offset(offset)
#         .limit(limit)
#     ).all()

#     chat_messages.reverse()
#     return chat_messages
