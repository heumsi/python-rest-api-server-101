from fastapi import APIRouter, status

from src.api.posts import create_post, read_posts, read_post, update_post, patch_post, delete_post

router = APIRouter(prefix="/posts", tags=["posts"])

router.add_api_route(
    methods=["POST"],
    path="/",
    endpoint=create_post.handle,
    status_code=status.HTTP_201_CREATED,
)
router.add_api_route(
    methods=["GET"],
    path="/",
    endpoint=read_posts.handle,
    status_code=status.HTTP_200_OK,
)
router.add_api_route(
    methods=["GET"],
    path="/{post_id}",
    endpoint=read_post.handle,
    status_code=status.HTTP_200_OK,
)
router.add_api_route(
    methods=["PUT"],
    path="/{post_id}",
    endpoint=update_post.handle,
    status_code=status.HTTP_200_OK,
)
router.add_api_route(
    methods=["PATCH"],
    path="/{post_id}",
    endpoint=patch_post.handle,
    status_code=status.HTTP_200_OK,
)
router.add_api_route(
    methods=["DELETE"],
    path="/{post_id}",
    endpoint=delete_post.handle,
    status_code=status.HTTP_204_NO_CONTENT,
)
