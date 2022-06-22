from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("AdminLogin", views.AdminLogin, name="AdminLogin"),
			path("Admin.html", views.Admin, name="Admin"),
			path("About.html", views.About, name="About"),
			path("AddEvidence.html", views.AddEvidence, name="AddEvidence"),
			path("AddEvidenceAction", views.AddEvidenceAction, name="AddEvidenceAction"),
			path("ViewEvidence", views.ViewEvidence, name="ViewEvidence"),
]