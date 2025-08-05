from flask import Blueprint

from modules.comment.rest_api.comment_router import CommentRouter


class CommentRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        blueprint = Blueprint("comment", __name__)
        blueprint = CommentRouter.create_route(blueprint=blueprint)
        return blueprint