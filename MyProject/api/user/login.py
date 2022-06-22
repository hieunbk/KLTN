
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api.base.authentication import BasicAuthentication

class UserLoginViewSet(ViewSet):
    authentication_classes = (BasicAuthentication,)

    def post(self, request):
        user = request.user
        context = {}
        context.update({
            'user_id': user.id,
            'token': user.get_key,
            'username': user.username,
        })
        return Response(context)

