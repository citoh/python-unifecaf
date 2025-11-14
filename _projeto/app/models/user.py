import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, func, Enum
import enum
from app.database import Base
import bcrypt

# Função para hash de senhas usando bcrypt diretamente
def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt."""
    # Converte a senha para bytes se necessário
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Gera o salt e faz o hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password, salt)
    # Retorna como string
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha está correta."""
    # Converte para bytes se necessário
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    # Verifica a senha
    return bcrypt.checkpw(password, hashed)


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)

    # Datas de criação/alteração
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relacionamento com carrinho
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")

    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash da senha."""
        return hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta."""
        return verify_password(password, self.hashed_password)

    def is_admin(self) -> bool:
        """Verifica se o usuário é admin."""
        return self.role == UserRole.ADMIN

