from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt
import uuid

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Chess Mate."""

# - users
#   - id: UUID, PK
#   - username: String
#   - password: String, hashed

# User model
class User(db.Model):
    """Creates user model"""

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password):
        """Registers user, hashes password, and adds user to database."""
        duplicate_user_found = User.check_duplicate_username(username)
        if duplicate_user_found:
            return {"failed": "username taken"}

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return {"success": "user created"}

    @classmethod
    def check_duplicate_username(cls, username):
        """Checks whether the username is already taken"""
        user = cls.query.filter_by(username=username).first()
        if user:
            return True
        return False

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return {"success": "successfully logged in"}

        return {"failed": "invalid username/password combination"}


# - stats
#   - user_id: UUID, PK
#   - win: Integer
#   - loss: Integer

# Stat model
class Stat(db.Model):
    """Creates stat model"""

    __tablename__ = "stats"

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    win = db.Column(db.Integer, nullable=False, default=0)
    loss = db.Column(db.Integer, nullable=False, default=0)
