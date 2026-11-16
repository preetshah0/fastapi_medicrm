# from sqladmin import ModelView
# from app.model.User import User
# from app.model.Organization import Organization

# class OrganizationAdmin(ModelView, model=Organization):
#     column_list = [
#         Organization.organization_name,
#         Organization.organization_email,
#         Organization.status,
#         Organization.profile_photo,
#         Organization.address,
#       ]

#     form_columns  =  [
#         Organization.profile_photo,
#         Organization.organization_name,
#         Organization.organization_email,
#         Organization.address
#     ]

#     name = "Organization"
#     name_plural = " Organizations"
#     icon = "fa-solid fa-book"
       

#     column_list = [Company.id, Company.name]

# class UserAdmin(ModelView, model=User):
#     # Dictates which columns display in the main data table view
#     column_list = [User.id, User.username, "owner.name"] # Dot notation works for list view

#     # Dictates which fields show in Create/Edit forms
#     # CRITICAL: Use the relationship name 'company', NOT the foreign key ID 'company_id'
#     form_columns = ["owner.name"]
     
#     # Optimization: Enables a searchable AJAX dropdown instead of loading thousands of items at once
  
