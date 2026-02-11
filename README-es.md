## 2026–2027 – Roadmap para Convertirme en AI‑First Full Stack Developer

Este documento resume mi plan personal de aprendizaje y proyectos para 2026–2027 para convertirme en un **AI‑First Full Stack Developer**, al mismo tiempo que completo la **carrera de Software Development en Brigham Young University–Idaho (BYU–Idaho)** y me gradúo a finales de 2027.  
“AI‑First” significa que en cada sistema o funcionalidad me preguntaré: *¿Cómo puede la IA potenciar esto?* – en la experiencia de usuario, en el backend, en la capa de datos y en las herramientas de desarrollo.

El roadmap está alineado con los cursos que me faltan:

- **Bloque de Programación y Desarrollo Web**
  - CSE 111, CSE 210, CSE 212, CSE 270, CSE 300, CSE 310, CSE 325, CSE 340, CSE 341, CSE 499
  - WDD 131, WDD 231, WDD 330, WDD 430
  - ITM 111
- **Educación General y Fundamentos**
  - BUS 301, FCS 160, PUBH 132, IDS 499

---

## Principios Guía

- **Fundamentos sólidos primero**: bases fuertes de CS, web y datos antes de profundizar en IA avanzada.
- **Aprendizaje guiado por proyectos**: cada tema importante va acompañado de al menos un proyecto real.
- **IA como característica central**: todos los proyectos incluyen al menos una capacidad de IA (asistente, recomendaciones, automatización o analítica).
- **Iteración continua**: revisar el progreso de forma trimestral y ajustar herramientas, stack y metas.

---

## Perfil de Habilidades Meta (Finales de 2027)

- **Frontend**: manejar con soltura un framework moderno (React / Vue / Svelte), diseño responsivo, manejo de estado, enrutamiento, testing y rendimiento básico.
- **Backend**: diseñar y construir APIs REST/GraphQL (Python o Node.js), con autenticación, procesos en segundo plano y manejo de archivos.
- **Bases de datos y datos**: SQL práctico (PostgreSQL / MySQL), algo de NoSQL, migraciones, creación de índices y modelos de datos pensados para aplicaciones con mucha IA.
- **IA / ML**: integrar LLMs y búsqueda vectorial, afinar modelos pequeños, construir pipelines básicos de ML y razonar sobre calidad de datos y evaluación.
- **DevOps y MLOps**: familiaridad con Docker, CI básica, despliegue en la nube y patrones de despliegue de modelos.
- **Buenas prácticas**: uso de Git, pruebas, documentación, code reviews y patrones de arquitectura limpia.

---

## 2026 – Fundamentos y Primeras Apps con IA (Alineado con BYU–Idaho)

### Q1 2026 – Fundamentos de CS y Python

- **Metas**
  - Profundizar en fundamentos de programación y resolución de problemas, reforzando CSE 111.
  - Sentirme cómodo escribiendo Python idiomático y pruebas unitarias.
- **Enfoque**
  - Estructuras de datos en Python (listas, diccionarios, conjuntos, tuplas), clases y módulos.
  - Algoritmos básicos: recursión, búsqueda, ordenamiento, nociones de complejidad.
  - Testing con `pytest`, pensamiento TDD y depuración.
- **Alineación con la universidad**
  - **CSE 111**: usar tareas del curso como base para utilidades reutilizables y tests.
  - Preparar el terreno para **CSE 210** y **CSE 212**.
- **Proyecto hito**
  - **CLI Study Assistant**: herramienta de línea de comandos que usa una API de LLM para generar preguntas y explicaciones de temas de clase.

### Q2 2026 – Fundamentos Web (Frontend + HTTP + Backend básico)

- **Metas**
  - Construir y desplegar aplicaciones full stack sencillas.
  - Entender HTTP, REST y arquitectura cliente‑servidor.
- **Enfoque**
  - HTML, CSS (incluyendo Flexbox/Grid), diseño responsivo.
  - JavaScript moderno (ES6+), async/await, `fetch`/axios.
  - Backend introductorio con Python (Flask / FastAPI) o Node.js (Express).
  - Despliegue básico en una PaaS.
- **Alineación con la universidad**
  - **WDD 131**: bases sólidas de HTML/CSS/JS.
  - Preparar patrones que servirán en **WDD 231** y **WDD 330**.
- **Proyecto hito**
  - **Task Manager with AI Suggestions**: gestor de tareas con API, base de datos básica y un endpoint de IA que sugiere prioridades y próximos pasos.

### Q3 2026 – Backend Más Profundo + Bases de Datos

- **Metas**
  - Diseñar APIs y modelos de datos más robustos.
  - Sentirme cómodo con SQL y migraciones.
- **Enfoque**
  - Bases de datos relacionales (PostgreSQL): esquemas, relaciones, índices.
  - ORMs (SQLAlchemy / Prisma / Django ORM).
  - Autenticación: sesiones/JWT, hashing de contraseñas, roles.
  - Tareas en segundo plano, cron jobs y subidas de archivos.
- **Alineación con la universidad**
  - **ITM 111**: reforzar modelado relacional, SQL y normalización.
  - Preparar **CSE 340** y **CSE 341** diseñando servicios API reales.
- **Proyecto hito**
  - **Learning Tracker Platform**: plataforma para registrar sesiones de estudio y recursos, con tablero analítico y recomendaciones de estudio impulsadas por IA.

### Q4 2026 – Framework Frontend Moderno y UX

- **Metas**
  - Ser productivo con un framework moderno (por ejemplo, React).
  - Mejorar UX, manejo de estado y pruebas de frontend.
- **Enfoque**
  - Componentes, hooks, enrutamiento y formularios.
  - Manejo de estado (React Query / Redux / context + reducer).
  - Librerías de componentes y diseño (Tailwind, Material, etc.).
  - Rendimiento: code splitting, memoización y evitar renders innecesarios.
- **Alineación con la universidad**
  - **WDD 231** y **WDD 330**: practicar patrones SPA y diseño de componentes.
  - Preparar **WDD 430** construyendo frontends más complejos sobre APIs propias.
- **Proyecto hito**
  - **AI‑First Dashboard**: nuevo frontend para backends anteriores, con un panel de asistente de IA que consulta y resume datos de la app.

---

## 2027 – Especialización AI‑First y Listo para Producción (Año de Graduación)

### Q1 2027 – IA Práctica e Integración de LLMs

- **Metas**
  - Integrar LLMs comerciales y open‑source en aplicaciones reales.
  - Entender diseño de prompts, manejo de contexto y evaluación básica.
- **Enfoque**
  - Llamar APIs de LLM (OpenAI, Anthropic, etc.), incluyendo streaming.
  - Patrones de prompt engineering (herramientas, roles, retrieval).
  - Fundamentos de RAG (retrieval‑augmented generation) y bases de datos vectoriales.
- **Alineación con la universidad**
  - Integrar IA en proyectos avanzados de **CSE 310** y **WDD 430**.
  - Empezar a planear cómo se verá la IA dentro de **CSE 499** e **IDS 499**.
- **Proyecto hito**
  - **Documentation Copilot**: web app que indexa documentación y apuntes (incluyendo material de clase) en un vector store y responde preguntas con citas.

### Q2 2027 – Fundamentos de ML y Pipelines de Datos

- **Metas**
  - Aprender ML clásico y flujos de datos simples.
  - Crear modelos sencillos más allá de usar solo LLMs.
- **Enfoque**
  - Stack de datos en Python: NumPy, pandas, visualización básica.
  - ML con scikit‑learn: regresión, clasificación, métricas.
  - Limpieza de datos, features, splits train/validation/test.
- **Alineación con la universidad**
  - Usar datasets de **CSE 310**, **ITM 111** u otros cursos.
  - Preparar reportes y justificaciones técnicas para **BUS 301** y **CSE 300**.
- **Proyecto hito**
  - **Prediction Service**: servicio de predicción (por ejemplo, riesgo de abandono, puntuaciones) con modelo entrenado, API desplegada y logging de peticiones.

### Q3 2027 – DevOps, MLOps y Escalabilidad

- **Metas**
  - Empaquetar y desplegar apps y modelos de forma confiable.
  - Entender monitoreo, logging y estrategias básicas de escala.
- **Enfoque**
  - Docker para frontend, backend y servicios de ML.
  - CI (GitHub Actions u otra herramienta) para tests y linting.
  - Manejo de entornos, secretos, configuración y observabilidad.
  - MLOps básico: versionado de modelos, seguimiento de experimentos, retraining sencillo.
- **Alineación con la universidad**
  - Fortalecer la preparación profesional para **CSE 300** con flujos reales de despliegue y documentación.
  - Construir la infraestructura que soportará **CSE 499** e **IDS 499**.
- **Proyecto hito**
  - **AI Microservice Architecture**: arquitectura de microservicios con un servicio de IA dedicado (LLM o ML), todos en contenedores y orquestados con Docker Compose.

### Q4 2027 – Capstone: Producto AI‑First Full Stack (Graduación)

- **Metas**
  - Entregar un producto pulido, realista y listo para mostrar a empleadores.
  - Unificar lo aprendido en la carrera y en este roadmap.
- **Enfoque**
  - Pensamiento de producto: investigación de usuarios, priorización de funcionalidades.
  - Calidad extremo a extremo: pruebas, documentación, onboarding, rendimiento.
  - Integración de múltiples capacidades de IA (asistente, recomendaciones, automatización).
- **Ideas de proyecto capstone**
  - **AI‑First Learning Platform**: planificador de estudio personalizado + tutor IA + analítica de progreso.
  - **AI‑Powered Productivity Hub**: tareas, notas, calendario y un asistente de IA que los coordina.
  - **Asistente especializado (nicho)**: copilot para un dominio concreto (aprendizaje de idiomas, fitness, ejercicios de programación, etc.).
- **Conexión con la universidad**
  - Este producto puede ser la base técnica de **CSE 499 (Senior Capstone)** y la pieza central de reflexión en **IDS 499 (Senior Integration)**.

---

## Hábitos de Trabajo y Métricas

- **Ritmo semanal**
  - 3–5 sesiones concentradas de estudio/código.
  - Al menos una sesión a la semana dedicada solo a construir o mantener proyectos.
- **Revisión mensual**
  - Evaluar avance en los hitos del roadmap.
  - Ajustar recursos, stack y prioridades según sea necesario.
- **Portafolio**
  - Mantener una lista de repos públicos y demos.
  - Añadir READMEs claros, capturas de pantalla y pequeños videos de demostración.

---

## Mapeo Curso → Roadmap (BYU–Idaho)

| Curso | Título | Conexiones principales con el roadmap |
|-------|--------|----------------------------------------|
| **CSE 111** | Programming with Functions | Q1 2026 – fundamentos de Python, testing, **CLI Study Assistant** |
| **CSE 210** | Programming with Classes | Q1–Q2 2026 – diseño orientado a objetos, refactor de proyectos existentes |
| **CSE 212** | Programming with Data Structures | Q1–Q3 2026 – estructuras para funcionalidades de IA (colas, árboles, grafos) |
| **CSE 270** | Software Testing | Q1–Q4 2026 – pruebas para APIs backend, servicios de IA y componentes frontend |
| **CSE 300** | Professional Readiness | Q2–Q3 2027 – documentación y presentaciones sobre decisiones de arquitectura e IA |
| **CSE 310** | Applied Programming | Q1–Q2 2027 – integrar IA y ML en apps grandes, **Prediction Service** |
| **CSE 325** | .NET Software Development (u otra electiva) | Q2–Q3 2027 – explorar full stack en .NET y añadir integración con LLMs |
| **CSE 340** | Web Backend Development | Q3 2026–Q3 2027 – APIs sólidas y listas para IA, auth y datos |
| **CSE 341** | Web Services | Q3 2026–Q3 2027 – servicios web para exponer modelos y LLMs |
| **CSE 499** | Senior Capstone | Q4 2027 – **AI‑First Full Stack Product** como proyecto principal |
| **WDD 131** | Dynamic Web Fundamentals | Q2 2026 – UI para **Task Manager with AI Suggestions** |
| **WDD 231** | Web Frontend Development I | Q4 2026 – SPAs iniciales, reconstrucción de UIs con componentes |
| **WDD 330** | Web Frontend Development II | Q4 2026–Q1 2027 – patrones avanzados, **AI‑First Dashboard** |
| **WDD 430** | Web Full‑Stack Development | Q1–Q3 2027 – producto full stack con IA integrada (RAG, asistentes) |
| **ITM 111** | Introduction to Databases | Q3 2026–Q2 2027 – bases de datos para **Learning Tracker** y **Prediction Service** |
| **BUS 301** | Advanced Writing in Professional Contexts | Q2–Q4 2027 – redacción profesional de documentación técnica y reportes de capstone |
| **FCS 160** | Family Leadership | Cualquier trimestre – liderazgo y gestión del tiempo en equipos de proyecto |
| **PUBH 132** | Personal Health & Wellness | Cualquier trimestre – equilibrio entre estudios, trabajo y salud mientras sigo el roadmap |
| **IDS 499** | Senior Integration | Q4 2027 – reflexión final usando el producto AI‑First como evidencia de aprendizaje |

Voy a adaptar y refinar este plan a medida que avanzo, pero el objetivo final se mantiene:  
**pensar y construir como un AI‑First Full Stack Developer al terminar 2027.**

