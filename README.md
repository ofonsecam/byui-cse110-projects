🚀 Fons Inventory - Backend (AI-Powered)
Este es el motor de Fons Inventory, una solución Full-Stack diseñada para la gestión de inventarios con análisis predictivo mediante Inteligencia Artificial. El sistema permite a negocios locales gestionar su stock de manera segura y recibir consejos estratégicos en tiempo real.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.11.

Framework: FastAPI (para una API REST de alto rendimiento).

Base de Datos: PostgreSQL alojado en Supabase.

ORM: SQLAlchemy para el mapeo de datos.

Seguridad: Autenticación JWT con validación asimétrica (JWKS).

IA: Google Gemini Pro API para el análisis de inventario.

🧠 Desafíos Técnicos Resueltos
Uno de los mayores retos en este proyecto fue la transición hacia la criptografía moderna en la nube:

Migración de Esquemas: Se rediseñó la base de datos para pasar de identificadores basados en texto a llaves primarias numéricas, mejorando la integridad referencial.

Validación de Tokens ES256: Implementé una solución de validación híbrida. Debido a que Supabase utiliza el algoritmo ES256 (Curva Elíptica), configuré un cliente JWKS (JSON Web Key Set) que descarga las llaves públicas del servidor de autenticación de forma dinámica, garantizando máxima seguridad sin comprometer la flexibilidad.

🔧 Instalación y Configuración
Clona el repositorio.

Instala las dependencias: pip install -r requirements.txt.

Configura las variables de entorno en un archivo .env:

DB_URL: Tu conexión a PostgreSQL.

SUPABASE_URL: La URL de tu proyecto en Supabase.

GEMINI_API_KEY: Tu llave de Google AI.

👨‍💻 Sobre el Autor
Soy Oscar Fonseca, estudiante de Software Development en BYU-Idaho (graduación prevista en 2027). Mi objetivo es convertirme en un AI-First Full Stack Developer, creando herramientas que cierren la brecha entre la tecnología avanzada y las necesidades de los negocios reales.