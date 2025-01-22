from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    SeatedPosture, HandPosition, DeskPosition, 
    Annotation, GenerateReport, AnnotateObject, 
    AnthropicAnalysis, BackAngleAnalysis, ArmScreenAnalysis,
    ImageQualityCheck, CameraAngleAnalysis
)

urlpatterns = [
    path('api/images/seatedposture/', SeatedPosture.as_view(), name='seated-posture'),
    path('api/images/handposition/', HandPosition.as_view(), name='hand-position'),
    path('api/images/deskposition/', DeskPosition.as_view(), name='desk-position'),
    path('api/images/annotateimage/', Annotation.as_view(), name='annotate-image'),
    path('api/report/generate', GenerateReport.as_view(), name='generate-report'),
    path('api/images/annotateobject/', AnnotateObject.as_view(), name='annotate-object'),
    path('api/images/anthropic-analysis/', AnthropicAnalysis.as_view(), name='anthropic-analysis'),
    path('api/analyze/back-angle/', BackAngleAnalysis.as_view(), name='back-angle-analysis'),
    path('api/analyze/arm-screen/', ArmScreenAnalysis.as_view(), name='arm-screen-analysis'),
    path('api/preprocess/check-quality/', ImageQualityCheck.as_view(), name='image-quality-check'),
    path('api/analyze/camera-angle/', CameraAngleAnalysis.as_view(), name='camera-angle-analysis'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
