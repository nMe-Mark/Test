from flask_jwt_extended import create_access_token


def generate_token(identity, role=None):
    additional_claims = {"role": role} if role else {}
    return create_access_token(identity=identity, additional_claims=additional_claims)