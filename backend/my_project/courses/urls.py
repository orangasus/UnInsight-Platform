from django.urls import path
from .views import (get_all_courses, get_course_by_id, update_course_by_id, delete_course_by_id,
                    create_course, CourseSearchView, CourseRatingView, CourseSearchView_Uni, search_for_courses)
from .views import Course_Status_Update_View, Course_Status_List_View
urlpatterns = [
    path('get_course/<int:course_id>', get_course_by_id, name='get_course'),
    path('update_course/<int:course_id>', update_course_by_id, name='update_course'),
    path('delete_course/<int:course_id>', delete_course_by_id, name='delete_course'),
    path('get_all_courses/', get_all_courses, name='get_all_courses'),
    path('create_course/', create_course, name='create_course'),
    # URL pattern for searching courses within a specific university
    path('universities/<int:uni_id>/search_query/', CourseSearchView_Uni.as_view(), name='course_search_Uni'),
    # URL pattern for searching courses via name or code
    path('search/search_query/', CourseSearchView.as_view(), name='course_search'),
    # URL pattern for rating a course by ID
    path('<int:pk>/rate/', CourseRatingView.as_view(), name='course_rate'),
    path('course/<int:pk>/status/', Course_Status_Update_View.as_view(), name='course_status_update'),
    path('status/', Course_Status_List_View.as_view(), name='course_status_list'),#/courses/status/?course_status=<status_value>
    path('course_search/', search_for_courses, name='course_search')
]



