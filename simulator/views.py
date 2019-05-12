from rest_framework import views
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from profiles_api.models import UserProfile, Fighter
from profiles_api.serializers import FighterSerializer
from .utils import simualtions
from rest_framework.parsers import JSONParser
from rest_framework import status
import json,io


class SimulatorAPIView(views.APIView):
    """
    The simualtor view for the project
    Responsible for simulating fights between fighters
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Sending back the docs of the view.
        Also sending data as an example on how to interact
        with the API correctly.
        """
        example_data = {
            "user_fighter_id": 1,
            "opponent_id": 2,
            "opponent_fighter_id": 9
        }
        return Response({"doc": self.__doc__.strip(), "body_example": example_data})

    def post(self, request, format=None):
        """
        Recieves request body containing the following parameters:
        user fighter id
        opponent id
        opponent fighter id
        return the result of the fight between the two users' fighters
        """
        user_fighter_id, opponent_id, opponent_fighter_id = request.data["user_fighter_id"], \
                                                            request.data["opponent_id"], \
                                                            request.data["opponent_fighter_id"]
        user_fighter = self.request.user.fighter_set.get(id=user_fighter_id)
        user_fighter = FighterSerializer(user_fighter)
        opponent = FighterSerializer(UserProfile.objects.get(id=opponent_id).fighter_set.get(id=opponent_fighter_id))
        fight_res = simualtions.simualte_fight(user_fighter,opponent)
        winner_msg = ("User {} won (challenger)".format(self.request.user.id)) if fight_res else (
        "User {} won (opponent)".format(opponent_id))
        return Response({"winner_id": self.request.user.id if fight_res else opponent_id, "msg": winner_msg},
                        status=status.HTTP_200_OK)