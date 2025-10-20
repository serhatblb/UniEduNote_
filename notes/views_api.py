from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from .models import Note, Comment, Like

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        comments = note.comments.all().order_by("-created_at")
        data = [
            {
                "id": c.id,
                "user": c.user.username,
                "user_id": c.user.id,
                "content": c.content,
                "created_at": c.created_at.strftime("%d.%m.%Y %H:%M"),
            }
            for c in comments
        ]
        return Response(data)

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        content = request.data.get("content", "").strip()
        if not content:
            return Response({"error": "Yorum boş olamaz."}, status=400)
        comment = Comment.objects.create(user=request.user, note=note, content=content)
        return Response(
            {
                "id": comment.id,
                "user": comment.user.username,
                "user_id": comment.user.id,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M"),
            },
            status=201,
        )

    def put(self, request, note_id):
        data = request.data
        comment_id = data.get("id")
        new_content = data.get("content", "").strip()
        comment = get_object_or_404(Comment, id=comment_id, note_id=note_id)
        if comment.user != request.user:
            return Response({"error": "Yalnızca kendi yorumunu düzenleyebilirsin."}, status=403)
        comment.content = new_content
        comment.save()
        return Response({"message": "Yorum başarıyla güncellendi."})

    def delete(self, request, note_id):
        data = request.data
        comment_id = data.get("id")
        comment = get_object_or_404(Comment, id=comment_id, note_id=note_id)
        if comment.user != request.user:
            return Response({"error": "Yalnızca kendi yorumunu silebilirsin."}, status=403)
        comment.delete()
        return Response({"message": "Yorum silindi."})

class LikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        liked = Like.objects.filter(user=request.user, note=note).exists()
        total_likes = Like.objects.filter(note=note).count()
        return Response({"liked": liked, "total_likes": total_likes})

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        like_obj = Like.objects.filter(user=request.user, note=note).first()
        if like_obj:
            like_obj.delete()
        else:
            Like.objects.create(user=request.user, note=note)
        total = Like.objects.filter(note=note).count()
        note.likes = total
        note.save()
        return Response({"liked": not bool(like_obj), "total_likes": total})
