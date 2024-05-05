from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from punq import Container

from application.api.messages.filters import (
    GetAllChatsFilters,
    GetMessagesFilters,
)
from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetAllChatsQueryResponseSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetAllChatsQuery,
    GetChatDetailQuery,
    GetMessagesQuery,
)

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create new chat, if chat with that title already exists - return 400",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Create new chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/messages/",
    status_code=status.HTTP_201_CREATED,
    description="Add new message in chat by chat_oid",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageRequestSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Add new message in chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    "/{chat_oid}/",
    status_code=status.HTTP_200_OK,
    description="Get chat by chat_oid",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> ChatDetailSchema:
    """Get chat by chat_oid."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return ChatDetailSchema.from_entity(chat)


@router.get(
    "/{chat_oid}/messages/",
    status_code=status.HTTP_200_OK,
    description="Get messages in chat by chat_oid",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetMessagesQueryResponseSchema:
    """Get messages in chat by chat_oid."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all open on this moment chats",
    responses={
        status.HTTP_200_OK: {"model": GetAllChatsQueryResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
    summary="Get all open on this moment chats",
)
async def get_all_chats_handler(
    filters: GetAllChatsFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetAllChatsQueryResponseSchema:
    """Get all open on this moment chats."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chats, count = await mediator.handle_query(
            GetAllChatsQuery(filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        ) from exception

    return GetAllChatsQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ChatDetailSchema.from_entity(chat) for chat in chats],
    )
