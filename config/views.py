from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Endpoint para mensaje en la ruta raiz
@api_view(['GET'])
def index(request):
    return Response({
        'status': 'success',
        'message': 'Information about the project successfully obtained.',
        'data': {
            'info': {
                'project': {
                    'github': 'https://github.com/JohannGaviria/shiny-umbrella',
                    'production': 'https://shiny-umbrella-production.up.railway.app/',
                    'description': 'Development of a REST API that allows users to create and participate in surveys. It offers profile management, visualization of results and notifications about survey activity, facilitating data collection for decision making.',
                    'technologies': [
                        'Python',
                        'Django',
                        'Django Rest Framework',
                        'PostgreSQL',
                        'SQLite',
                        'Docker',
                        'Railway'
                    ]
                },
                'developer': {
                    'name': 'Johann Gaviria',
                    'github': 'https://github.com/JohannGaviria',
                    'linkedin': 'https://www.linkedin.com/in/johanngaviria',
                }
            },
            'endpoints': {
                'users': [
                    {
                        'Name': 'User Registration',
                        'Method': 'POST',
                        'URL': '/api/users/sign_up',
                        'Description': 'User registration in the system.'
                    },
                    {
                        'Name': 'User Email Verification',
                        'Method': 'GET',
                        'URL': '/api/users/verify/<str:token_email>',
                        'Description': 'User email verification.'
                    },
                    {
                        'Name': 'User Login',
                        'Method': 'POST',
                        'URL': '/api/users/sign_in',
                        'Description': 'User login to the system.'
                    },
                    {
                        'Name': 'User Logout',
                        'Method': 'POST',
                        'URL': '/api/users/sign_out',
                        'Description': 'User logout from the system.'
                    },
                    {
                        'Name': 'User Update',
                        'Method': 'PUT',
                        'URL': '/api/users/update_user',
                        'Description': 'Update user profile information.'
                    },
                    {
                        'Name': 'User Deletion',
                        'Method': 'DELETE',
                        'URL': '/api/users/delete_user',
                        'Description': 'Delete the current user.'
                    }
                ],
                'surveys': [
                    {
                        'Name': 'Create Survey',
                        'Method': 'POST',
                        'URL': '/api/surveys/create',
                        'Description': 'Create a new survey.'
                    },
                    {
                        'Name': 'Get Survey by ID',
                        'Method': 'GET',
                        'URL': '/api/surveys/get/<str:survey_id>',
                        'Description': 'Get a survey by its ID.'
                    },
                    {
                        'Name': 'Get All Surveys',
                        'Method': 'GET',
                        'URL': '/api/surveys/get_all?page_size=<size_value>&page=<page_value>',
                        'Description': 'Get all surveys.'
                    },
                    {
                        'Name': 'Search Surveys',
                        'Method': 'GET',
                        'URL': '/api/surveys/search_surveys?query=<search_value>&page_size=<size_value>&page=<page_value>',
                        'Description': 'Search surveys.'
                    },
                    {
                        'Name': 'Update Survey',
                        'Method': 'PUT',
                        'URL': '/api/surveys/update/<str:survey_id>',
                        'Description': 'Update a survey by its ID.'
                    },
                    {
                        'Name': 'Delete Survey',
                        'Method': 'DELETE',
                        'URL': '/api/surveys/delete/<str:survey_id>',
                        'Description': 'Delete a survey by its ID.'
                    },
                    {
                        'Name': 'Answer Survey',
                        'Method': 'POST',
                        'URL': '/api/surveys/<str:survey_id>/answer',
                        'Description': 'Answer a survey.'
                    },
                    {
                        'Name': 'Invite to Answer Survey',
                        'Method': 'POST',
                        'URL': '/api/surveys/<str:survey_id>/invite',
                        'Description': 'Invite to answer a survey.'
                    }
                ],
                'feedbacks': [
                    {
                        'Name': 'Add Comment',
                        'Method': 'POST',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/comment/add',
                        'Description': 'Add a comment to a survey.'
                    },
                    {
                        'Name': 'Get All Comments of a Survey',
                        'Method': 'GET',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/comment/all?page_size=<size_value>&page=<page_value>',
                        'Description': 'Get all comments of a survey.'
                    },
                    {
                        'Name': 'Update Comment',
                        'Method': 'PUT',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/update',
                        'Description': 'Update a comment of a survey.'
                    },
                    {
                        'Name': 'Delete Comment',
                        'Method': 'DELETE',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/delete',
                        'Description': 'Delete a comment of a survey.'
                    },
                    {
                        'Name': 'Add Rating',
                        'Method': 'POST',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/qualify/add',
                        'Description': 'Add a rating to a survey.'
                    },
                    {
                        'Name': 'Get All Ratings of a Survey',
                        'Method': 'GET',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/qualify/all?page_size=<size_value>&page=<page_value>',
                        'Description': 'Get all ratings of a survey.'
                    },
                    {
                        'Name': 'Update Rating',
                        'Method': 'PUT',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/update',
                        'Description': 'Update a rating of a survey.'
                    },
                    {
                        'Name': 'Delete Rating',
                        'Method': 'DELETE',
                        'URL': '/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/delete',
                        'Description': 'Delete a rating of a survey.'
                    }
                ],
                'analysis': [
                    {
                        'Name': 'Export Analysis Details',
                        'Method': 'GET',
                        'URL': '/api/analysis/survey/<str:survey_id>/export',
                        'Description': 'Export survey analysis details.'
                    }
                ]
            }
        }
    }, status=status.HTTP_200_OK)