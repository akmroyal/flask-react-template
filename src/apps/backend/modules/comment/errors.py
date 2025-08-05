from modules.application.base_exception import BaseException
from modules.comment.types import CommentErrorCode


class CommentNotFoundError(BaseException):
    def __init__(self, *, comment_id: str) -> None:
        super().__init__(
            message=f"Comment with id={comment_id} not found",
            error_code=CommentErrorCode.NOT_FOUND,
            status_code=404,
        )


class CommentBadRequestError(BaseException):
    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            error_code=CommentErrorCode.BAD_REQUEST,
            status_code=400,
        )