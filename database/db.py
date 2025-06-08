from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DATETIME, Enum, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Modelos

class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comuna = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)


    region = relationship("Region", back_populates="comuna")
    actividad = relationship("Actividad", back_populates="comuna")

class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DATETIME, nullable=False)
    dia_hora_termino = Column(DATETIME, nullable=True)
    descripcion = Column(String(500), nullable=True)

    comuna = relationship("Comuna", back_populates="actividad")
    foto = relationship("Foto", back_populates="actividad")
    contactar_por = relationship("Contactar_por", back_populates="actividad")
    actividad_tema = relationship("Actividad_tema", back_populates="actividad")
    comentario = relationship("Comentario", back_populates="actividad")

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), primary_key=True, nullable=False)

    actividad = relationship("Actividad", back_populates="foto")

class Contactar_por(Base):
    __tablename__ = 'contactar_por'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), primary_key=True, nullable=False)

    actividad = relationship("Actividad", back_populates="contactar_por")

class Actividad_tema(Base):
    __tablename__ = 'actividad_tema'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), primary_key=True, nullable=False)

    actividad = relationship("Actividad", back_populates="actividad_tema")

class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False, default=func.now())
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship("Actividad", back_populates="comentario")

def crear_foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    new_foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, actividad_id=actividad_id)
    session.add(new_foto)
    session.commit()
    session.close()

def crear_contacto(nombre, identificador, actividad_id):
    session = SessionLocal()
    new_contacto = Contactar_por(nombre=nombre, identificador=identificador, actividad_id=actividad_id)
    session.add(new_contacto)
    session.commit()
    session.close()

def crear_tema_actividad(tema, glosa_otro, actividad_id):
    session = SessionLocal()
    new_tema = Actividad_tema(tema=tema, glosa_otro=glosa_otro, actividad_id=actividad_id)
    session.add(new_tema)
    session.commit()
    session.close()

def get_actividades(page_size):
    session = SessionLocal()
    actividades = session.query(Actividad).order_by(Actividad.id.desc()).limit(page_size).all()
    session.close()
    return actividades

def get_actividad_by_id(id):
    session = SessionLocal()
    actividad = session.query(Actividad).filter_by(id=id).first()
    session.close()
    return actividad

def get_tema_by_id(id):
    session = SessionLocal()
    tema = session.query(Actividad_tema).filter_by(actividad_id=id).first()
    session.close()
    return tema

def get_comuna_by_name(name):
    session = SessionLocal()
    nombre_comuna = session.query(Comuna).filter_by(nombre=name).first()
    session.close()
    return nombre_comuna

def get_region_by_name(name):
    session = SessionLocal()
    nombre_region = session.query(Region).filter_by(nombre=name).first()
    session.close()
    return nombre_region