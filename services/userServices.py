from models.userModel import UserModel, user_schema, users_schema
from logger.log import log

class UserServices:

    @staticmethod
    def login_user(data):
        log.debug('login_user', data=data['email'])
        user_model = UserModel().get_user_by_email(data['email'])
        if user_model and user_model.get_decrypted_password() == data['password']:
            user_model.generate_token()
            log.info('User logged in', user=user_model.email)
            return user_schema.dump(user_model), user_model.token
        log.error('User not found', user=data['email'])
        return None, None
    @staticmethod
    def register_user(data):
        log.debug('register_user', data=data)
        user_model, msg = UserModel(**data).create_user()
        if not user_model:
            log.error(msg, user=data['email'])
            return None, msg
        user_model.generate_token()
        return user_schema.dump(user_model), user_model.token


    @staticmethod
    def get_all_users(limit, offset):
        log.debug('get_all_users', limit=limit, offset=offset)
        user_model = UserModel()
        users = user_model.get_all_users(limit, offset)
        return users_schema.dump(users)

    @staticmethod
    def get_user_by_id(user_id):
        user_model = UserModel()
        user = user_model.get_user_by_id(user_id)
        return user_schema.dump(user)

    @staticmethod
    def get_user_by_email(email):
        log.debug('get_user_by_email', email=email)
        user_model = UserModel()
        user = user_model.get_user_by_email(email)
        return user_schema.dump(user)

    @staticmethod
    def create_user(data):
        log.debug('create_user', data=data)
        user_model, msg = UserModel(**data).create_user()
        if not user_model:
            log.error(msg, user=data['email'])
            return msg
        return user_schema.dump(user_model)

    @staticmethod
    def update_user(user_id, data):
        log.debug('update_user', user_id=user_id, data=data)
        # new_user = UserModel(**data)
        user_model = UserModel().get_user_by_id(user_id)
        if not user_model:
            return None, 'User not found'
        has_user_updated, msg = user_model.update_user(**data)
        if not has_user_updated:
            return None, msg
        return user_schema.dump(user_model), None

    @staticmethod
    def update_user_by_email(email, data):
        log.debug('update_user_by_email', email=email, data=data)
        user_model = UserModel().get_user_by_email(email)
        has_user_updated, msg = user_model.update_user(**data)
        if not has_user_updated:
            return None, msg
        return user_schema.dump(user_model), None

    @staticmethod
    def delete_user(user_id):
        log.debug('delete_user', user_id=user_id)
        user_model = UserModel()
        user_model.delete_user(user_id)
        return user_schema.dump(user_model)