from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator
from application.api.messages.schemas import CreateChatResponseSchema, CreateChatRequestSchema
from logic.init import init_container

router = APIRouter(tags=['Chat'])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create new chat, if chat with that title already exists - return 400",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(schema: CreateChatRequestSchema, container=Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))

    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})

    return CreateChatResponseSchema.from_entity(chat)
