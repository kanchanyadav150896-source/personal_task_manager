import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required


from .models import Task
from .serializers import TaskSerializer


User = get_user_model()


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ('id', 'title', 'status', 'created_at', 'assigned_to')


class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)


    @login_required
    def resolve_tasks(self, info):
        user = info.context.user
        return Task.objects.filter(assigned_to=user).order_by('-created_at')


# A mutation that uses the DRF TaskSerializer to validate and save
class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        status = graphene.String(required=False)


    task = graphene.Field(TaskType)


    @login_required
    def mutate(self, info, title, status=None):
        user = info.context.user
        data = {'title': title}
        if status:
            data['status'] = status
            # Attach assigned_to implicitly
        serializer = TaskSerializer(data=data)
        if not serializer.is_valid():
            # convert serializer errors to GraphQLError
            raise GraphQLError(str(serializer.errors))
        task = serializer.save(assigned_to=user)
        return CreateTask(task=task)


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)