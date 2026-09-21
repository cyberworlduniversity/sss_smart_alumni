from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import PostForm, CommentForm


@login_required
def post_list(request):
    posts = Post.objects.select_related("author").prefetch_related("comments")

    return render(
        request,
        "forum/list.html",
        {
            "posts": posts,
        },
    )


@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(
                request,
                "Post created successfully."
            )

            return redirect("post_list")

    else:
        form = PostForm()

    return render(
        request,
        "forum/create.html",
        {
            "form": form,
        },
    )


@login_required
def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            messages.success(
                request,
                "Comment added successfully."
            )

            return redirect("post_detail", pk=pk)

    else:
        comment_form = CommentForm()

    return render(
        request,
        "forum/detail.html",
        {
            "post": post,
            "comment_form": comment_form,
        },
    )


@login_required
def delete_post(request, pk):

    post = get_object_or_404(
        Post,
        pk=pk
    )

    if post.author != request.user:
        messages.error(
            request,
            "You are not allowed to delete this post."
        )
        return redirect("post_list")

    post.delete()

    messages.success(
        request,
        "Post deleted successfully."
    )

    return redirect("post_list")