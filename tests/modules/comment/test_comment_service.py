from modules.application.common.types import PaginationParams
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentNotFoundError
from modules.comment.types import (
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentService(BaseTestComment):

    def test_create_comment_success(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        create_params = CreateCommentParams(account_id=account.id, task_id=task.id, content="Test comment content")

        created_comment = CommentService.create_comment(params=create_params)

        assert created_comment.account_id == account.id
        assert created_comment.task_id == task.id
        assert created_comment.content == "Test comment content"
        assert created_comment.id is not None

    def test_get_comment_success(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        get_params = GetCommentParams(account_id=account.id, task_id=task.id, comment_id=created_comment.id)

        retrieved_comment = CommentService.get_comment(params=get_params)

        assert retrieved_comment.id == created_comment.id
        assert retrieved_comment.account_id == created_comment.account_id
        assert retrieved_comment.task_id == created_comment.task_id
        assert retrieved_comment.content == created_comment.content

    def test_get_comment_not_found(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        get_params = GetCommentParams(
            account_id=account.id, task_id=task.id, comment_id="507f1f77bcf86cd799439011"  # Non-existent ID
        )

        try:
            CommentService.get_comment(params=get_params)
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass  # Expected

    def test_get_paginated_comments_success(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        self.create_multiple_test_comments(account_id=account.id, task_id=task.id, count=5)

        pagination_params = PaginationParams(page=1, size=3, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id=account.id, task_id=task.id, pagination_params=pagination_params
        )

        result = CommentService.get_paginated_comments(params=get_params)

        assert len(result.items) == 3
        assert result.total_count == 5
        assert result.pagination_params.page == 1
        assert result.pagination_params.size == 3

    def test_update_comment_success(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(account_id=account.id, task_id=task.id, content="Original content")

        update_params = UpdateCommentParams(
            account_id=account.id, task_id=task.id, comment_id=created_comment.id, content="Updated content"
        )

        updated_comment = CommentService.update_comment(params=update_params)

        assert updated_comment.id == created_comment.id
        assert updated_comment.content == "Updated content"
        assert updated_comment.account_id == account.id
        assert updated_comment.task_id == task.id

    def test_update_comment_not_found(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        update_params = UpdateCommentParams(
            account_id=account.id,
            task_id=task.id,
            comment_id="507f1f77bcf86cd799439011",  # Non-existent ID
            content="Updated content",
        )

        try:
            CommentService.update_comment(params=update_params)
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass  # Expected

    def test_delete_comment_success(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        delete_params = DeleteCommentParams(account_id=account.id, task_id=task.id, comment_id=created_comment.id)

        result = CommentService.delete_comment(params=delete_params)

        assert result.success == True
        assert result.comment_id == created_comment.id
        assert result.deleted_at is not None

        # Verify comment is actually deleted
        get_params = GetCommentParams(account_id=account.id, task_id=task.id, comment_id=created_comment.id)

        try:
            CommentService.get_comment(params=get_params)
            assert False, "Expected CommentNotFoundError after deletion"
        except CommentNotFoundError:
            pass  # Expected

    def test_delete_comment_not_found(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        delete_params = DeleteCommentParams(
            account_id=account.id, task_id=task.id, comment_id="507f1f77bcf86cd799439011"  # Non-existent ID
        )

        try:
            CommentService.delete_comment(params=delete_params)
            assert False, "Expected CommentNotFoundError"
        except CommentNotFoundError:
            pass  # Expected
