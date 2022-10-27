from main.model.user import User
from flask_login import current_user


def users_related_to_organization(organization_id):
    class Org_user:
        def __init__(self, user) :
            self.user_id = user.id
            self.user = user

    user_list = User.query.filter_by(organization_id = organization_id)
    result_list = [Org_user(user) for user in user_list if user.id != current_user.id]
    return result_list
