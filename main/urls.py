from django.urls import path
from main.views import *

urlpatterns = [
    path('', login_view, name='login'),
    path("logout/", logout_view, name='logout'),
    path("reset-password/", reset_password_view, name='reset-password'),

    path("index/", index_view, name='index'),
    path("category/", category_view, name='category'),

    path("create-category/", create_category_view, name="create-category"),
    path("category-edit/<int:pk>/", category_edit_view, name='category_edit'),
    path("category-page/", category_page_view, name='category-page'),
    path("delete-category/<int:pk>/", delete_category_view, name='delete_category'),
    path("select-category/", select_category_view, name="select-category"),

    path("category-by-product/<int:pk>/", category_by_product_view, name="category-by-product"),
    path("create-product/<int:pk>/", create_product_view, name='create-product'),
    path("product-edit/<int:pk>/", product_edit_view, name='product-edit'),
    path("save-product/<int:pk>/", save_product_view, name='save-product'),
    path("delete-product/<int:pk>/", delete_product_view, name='delete-product'),


    path("output-page/", output_page_view, name='output-page'),
    path("create-output/", create_output_view, name='create-output'),
    path("output-edit/<int:pk>/", output_edit_view, name='output-edit'),
    path("delete-output/<int:pk>/", delete_output_view, name='delete_output'),

    path("order-create/", order_create_view, name='order-create'),
    path("order-page/", order_page_view, name='order-page'),
    path("order-edit/<int:pk>/", order_edit_view, name='order_edit'),
    path("order-delete/<int:pk>/", order_delete_view, name='order_delete'),

    path("help/", help_view, name='help')


]
