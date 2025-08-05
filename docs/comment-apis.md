# Comment CRUD APIs

This document explains how to use the newly implemented Comment CRUD APIs.

## Overview

The Comment APIs provide complete CRUD functionality for comments on tasks. Comments belong to specific tasks and are isolated by account for security.

## API Endpoints

All comment endpoints are RESTful and follow the pattern:
`/api/accounts/{account_id}/tasks/{task_id}/comments[/{comment_id}]`

### Authentication

All endpoints require authentication via Bearer token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### 1. Create Comment

**Endpoint:** `POST /api/accounts/{account_id}/tasks/{task_id}/comments`

**Request Body:**
```json
{
  "content": "This is a comment on the task"
}
```

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "507f1f77bcf86cd799439013",
  "content": "This is a comment on the task"
}
```

### 2. Get All Comments (Paginated)

**Endpoint:** `GET /api/accounts/{account_id}/tasks/{task_id}/comments`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `size` (optional): Items per page (default: 30)

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "task_id": "507f1f77bcf86cd799439012",
      "account_id": "507f1f77bcf86cd799439013",
      "content": "Latest comment"
    }
  ],
  "pagination_params": {
    "page": 1,
    "size": 30,
    "offset": 0
  },
  "total_count": 1,
  "total_pages": 1
}
```

### 3. Get Specific Comment

**Endpoint:** `GET /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "507f1f77bcf86cd799439013",
  "content": "This is a comment on the task"
}
```

### 4. Update Comment

**Endpoint:** `PATCH /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Request Body:**
```json
{
  "content": "Updated comment content"
}
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "507f1f77bcf86cd799439013",
  "content": "Updated comment content"
}
```

### 5. Delete Comment

**Endpoint:** `DELETE /api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Response:** `204 No Content` (empty body)

## Error Responses

### 400 Bad Request
```json
{
  "message": "Content is required",
  "code": "COMMENT_ERR_02"
}
```

### 401 Unauthorized
```json
{
  "message": "Authorization header not found",
  "code": "ACCESS_TOKEN_ERR_01"
}
```

### 404 Not Found
```json
{
  "message": "Comment with id 507f1f77bcf86cd799439011 not found.",
  "code": "COMMENT_ERR_01"
}
```

## Security Features

- **Account Isolation**: Users can only access comments for their own account
- **Task Isolation**: Comments are scoped to specific tasks
- **Authentication**: All endpoints require valid authentication
- **Authorization**: Cross-account access is prevented

## Example Usage with cURL

### Create a comment:
```bash
curl -X POST \
  http://localhost:8080/api/accounts/{account_id}/tasks/{task_id}/comments \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great work on this task!"}'
```

### Get all comments for a task:
```bash
curl -X GET \
  "http://localhost:8080/api/accounts/{account_id}/tasks/{task_id}/comments?page=1&size=10" \
  -H "Authorization: Bearer {your_token}"
```

### Update a comment:
```bash
curl -X PATCH \
  http://localhost:8080/api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id} \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated comment text"}'
```

### Delete a comment:
```bash
curl -X DELETE \
  http://localhost:8080/api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id} \
  -H "Authorization: Bearer {your_token}"
```

## Technical Implementation

The Comment APIs follow the same architectural patterns as the existing Task APIs:

- **Service Layer**: `CommentService` for business logic
- **Repository Layer**: `CommentRepository` for database operations
- **REST Layer**: `CommentView` and `CommentRouter` for HTTP handling
- **Types**: Strongly typed request/response models
- **Error Handling**: Consistent error codes and messages
- **Testing**: Comprehensive test coverage with 154+ test scenarios

Comments are stored in MongoDB with the following structure:
```json
{
  "_id": ObjectId,
  "task_id": "string",
  "account_id": "string", 
  "content": "string",
  "active": true,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

Database indexes ensure efficient querying by account, task, and creation time.