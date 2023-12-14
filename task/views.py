from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['created_at', 'due_date', 'priority', 'is_complete']
    ordering_fields = ['created_at', 'due_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TaskPhotoView(generics.CreateAPIView):
    queryset = TaskPhoto.objects.all()
    serializer_class = TaskPhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        task_id = self.request.data.get('task')
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)
