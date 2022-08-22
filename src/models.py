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

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user


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
