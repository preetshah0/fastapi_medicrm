from sqladmin import ModelView
from app.model.User import User

class UserAdmin(ModelView, model=User):
    column_list = [
        User.name,
        User.email,
        User.role,
        User.phone,
        User.specialization,
        User.status,
        User.created_at,
    ]
    column_searchable_list = [User.name, User.email, User.role]
    # column_filters = ['role', 'status']
    column_sortable_list = [User.name, User.email, User.role, User.created_at]
    form_excluded_columns = [
        User.password,
        User.remember_token,
        User.deleted_at,
        # User.email_verified_at,
    ]
    column_details_exclude_list = [User.password, User.remember_token]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    # list_template = "sqladmin/list.html"
    # create_template = "sqladmin/create.html"
    # edit_template = "sqladmin/edit.html"
    # details_template = "sqladmin/details.html"