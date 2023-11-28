from django.utils.timezone import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from noise_detection_api.models import AudioAnalysis
from noise_detection_api.serializers import AudioAnalysisSerializer
import noise_detection_api.resource.do_analysis as da

# Create your views here.

class RecordingsListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the records of analysis for given requested user
        '''
        todos = AudioAnalysis.objects.filter(user = request.user.id)
        serializer = AudioAnalysisSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateRecordingView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the record and analysis with given video data
        '''
        data = {
            'title': request.data.get('title'), 
            'video_evidence': request.data.get('video_evidence'), 
            'log_date': datetime.now(), 
            'updated_at': datetime.now(), 
            'user': request.user.id
        }
        serializer = AudioAnalysisSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            record_id = serializer.data['id']
            user_id = request.user.id

            try:
                result = da.do_analysis(record_id, user_id)
                serializer = AudioAnalysisSerializer(data=result)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"res": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordingDetailView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, record_id, user_id):
        '''
        Helper method to get the object with given record_id, and user_id
        '''
        try:
            return AudioAnalysis.objects.get(id=record_id, user = user_id)
        except AudioAnalysis.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, record_id, *args, **kwargs):
        '''
        Retrieves the Record with given record_id
        '''
        todo_instance = self.get_object(record_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AudioAnalysisSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, record_id, *args, **kwargs):
        '''
        Updates the record item with given record_id if exists
        Updatable fields include:
        1. title
        2. noise_density
        3. category
        4. user_ip_address
        5. gps_location
        '''
        todo_instance = self.get_object(record_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with record id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'), 
            'noise_density': request.data.get('noise_density'),
            'category': request.data.get('category'),
            'user_ip_address': request.data.get('user_ip_address'),
            'gps_location': request.data.get('gps_location'),
            'updated_at': datetime.now()
        }
        serializer = AudioAnalysisSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, record_id, *args, **kwargs):
        '''
        Deletes the record item with given record_id if exists
        '''
        todo_instance = self.get_object(record_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with record id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
