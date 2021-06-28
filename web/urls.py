from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("create", views.create),
    path("explore", views.explore),
    path("jsonclick", views.jsonclick),
    path("jsonscroll", views.jsonscroll),
    path("jsonwrite", views.jsonwrite),
    path("jsonpress", views.jsonpress),
    path("jsonloop", views.jsonloop),
    path("jsonwait", views.jsonwait),
    path("jsonbot", views.jsonbot),
    path("jsonstatus", views.jsonstatus),
    path("jsoncontrol", views.jsoncontrol),
    path("jsondrag", views.jsondrag),
    path("mousecoords", views.mousecoords),
    path("delete", views.delete),
    path("bot/<int:id>", views.bot_),
    path("listen", views.listen)
]
