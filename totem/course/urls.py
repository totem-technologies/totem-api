from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="list"),
    # path("<int:pk>/", views.PlanDetailView.as_view(), name="detail"),
    # path("plans/create/", views.PlanCreateView.as_view(), name="create"),
    # path("plans/<int:pk>/update/", views.PlanUpdateView.as_view(), name="update"),
    # path("plans/<int:pk>/delete/", views.PlanDeleteView.as_view(), name="delete"),
]
