from fastapi import APIRouter, status

from src.api.posts import (
    create_post,
    read_posts,
    read_post,
    update_post,
    patch_post,
    delete_post,
)

router = APIRouter(prefix="/posts", tags=["posts"])

router.add_api_route(
    methods=["POST"],
    path="/",
    endpoint=create_post.handle,
    status_code=status.HTTP_201_CREATED,
    summary="게시글을 추가합니다.",
)
router.add_api_route(
    methods=["GET"],
    path="/",
    endpoint=read_posts.handle,
    status_code=status.HTTP_200_OK,
    summary="게시글 목록을 조회합니다.",
    response_model=read_posts.ReadPostsResponse,
)
router.add_api_route(
    methods=["GET"],
    path="/{post_id}",
    endpoint=read_post.handle,
    status_code=status.HTTP_200_OK,
    summary="게시글을 조회합니다.",
    response_model=read_post.ReadPostResponse,
)
router.add_api_route(
    methods=["PUT"],
    path="/{post_id}",
    endpoint=update_post.handle,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글 전체를 수정합니다.",
)
router.add_api_route(
    methods=["PATCH"],
    path="/{post_id}",
    endpoint=patch_post.handle,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글 일부를 수정합니다.",
)
router.add_api_route(
    methods=["DELETE"],
    path="/{post_id}",
    endpoint=delete_post.handle,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글을 삭제합니다.",
)
