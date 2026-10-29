# SecAuditAI &mdash; Documento de Seguridad y AppSec

## 1. Modelo de Amenazas y Postura de Seguridad

SecAuditAI fue concebido bajo el principio de **Defensa en Profundidad (Defense in Depth)** y **Mínimo Privilegio**. El sistema procesa documentos que provienen de usuarios internos o terceros y que, por definición, deben tratarse como **datos no confiables (untrusted data)**.

Las principales amenazas consideradas en el diseño son:
1. **Inyección de Prompts e Instrucciones Maliciosas en Documentos**: Archivos que contienen directivas diseñadas para manipular el modelo de lenguaje (Jailbreak / Prompt Injection) y forzar evaluaciones fraudulentas.
2. **Ataques de Salto de Directorio (Path Traversal)**: Nombres de archivo que intentan escribir o leer fuera de la carpeta designada para evidencias (`data/uploads`).
3. **Carga de Archivos Maliciosos (Malicious File Upload)**: Ejecutables, scripts (.sh, .php, .exe) o binarios camuflados con extensiones permitidas.
4. **Denegación de Servicio (DoS) por Archivo Excesivo**: Intentos de agotar memoria o espacio en disco con archivos masivos.
5. **Divulgación de Información Interna**: Fugas de trazas de error (stack traces) o variables de entorno hacia el cliente HTTP.
6. **Falsificación o Sobrescritura de Evaluaciones Oficiales**: Manipulación no autorizada del estado de cumplimiento o suplantación de la decisión humana por parte de la IA.

---

## 2. Controles de Seguridad Implementados (AppSec)

### 2.1 Validación y Sanitización de Archivos
- **Lista Blanca de Extensiones (Allowlist)**: Únicamente se admiten archivos con extensión `.pdf`, `.docx`, `.txt` y `.md`.
- **Inspección de Firmas Binarias (Magic Bytes)**:
  - Archivos `.pdf`: Deben comenzar obligatoriamente con los bytes `%PDF`.
  - Archivos `.docx`: Deben comenzar con la firma de archivo comprimido OpenXML `PK\x03\x04`.
  - Archivos `.txt` y `.md`: Se verifica la ausencia de bytes nulos (`\x00`) en el encabezado para impedir la evasión binaria.
- **Límite de Tamaño Estricto**: Configurable mediante la variable `MAX_UPLOAD_SIZE_MB` (por defecto 15 MB). Los archivos que superan este umbral son rechazados inmediatamente.
- **Prevención de Path Traversal**:
  - Función `sanitize_filename()` que normaliza separadores multiplataforma (`/` y `\`), elimina secuencias de puntos `..` y caracteres no alfanuméricos.
  - Generación de un nombre interno aleatorio con prefijo UUID hexadecimal (`uuid.uuid4().hex`) para el almacenamiento en disco.
  - Verificación formal de contención mediante `is_path_safe()`, asegurando que la ruta final resuelta (`Path.resolve()`) resida estrictamente dentro de `data/uploads`.

### 2.2 Protección Frente a Inyecciones de Prompt (Prompt Injection Defense)
Los documentos cargados se someten a la función `defend_prompt_injection()` antes de ser transferidos al modelo local:
- El contenido del documento se encapsula dentro de delimitadores unívocos del sistema:
  ```text
  <<<DOCUMENT_CONTENT>>>
  [Contenido del documento evaluado]
  <<<END_DOCUMENT_CONTENT>>>
  ```
- **Neutralización de Evasión**: Si el documento contiene deliberadamente secuencias `<<<DOCUMENT_CONTENT>>>` o `<<<END_DOCUMENT_CONTENT>>>` para intentar cerrar el bloque de datos y dar órdenes al modelo, dichas cadenas son neutralizadas automáticamente a `[DELIMITER_ESCAPED]`.
- **Directiva de Sistema Reforzada**: La Skill instruye taxativamente al modelo a tratar todo el contenido entre dichos delimitadores únicamente como evidencia pasiva a auditar y a ignorar cualquier instrucción operativa interna.
- **Validación Estricta de Esquema**: La salida del modelo es forzada a JSON (`format: "json"`) y parseada exhaustivamente con modelos Pydantic con validación de rangos (1 a 5 y 0.0 a 1.0).

### 2.3 Soberanía y Privacidad de Datos
- **Procesamiento 100% Local**: La integración con IA se realiza exclusivamente mediante la API HTTP local de Ollama (`127.0.0.1:11434`).
- **Sin Servicios Cloud de Terceros**: No se envían documentos, textos, resúmenes ni telemetría a ninguna API externa en la nube.
- **Cálculo de Hash Criptográfico**: Cada evidencia genera y almacena su hash SHA-256 para garantizar la integridad y no repudio del archivo auditado.

### 2.4 Separación de Roles y Trazabilidad (Audit Trail)
- **Las Sugerencias de la IA no Sobrescriben al Auditor**: Las conclusiones generadas por el modelo se persisten como registros independientes en `AIProposal` en estado `pending`. La evaluación oficial registrada en `Requirement.compliance_score` o `AnnexControl.implementation_score` solo cambia cuando un usuario humano acepta o ajusta la propuesta.
- **Historial de Cambios Inmutable**: Cada cambio de evaluación genera un registro en la tabla `Assessment` con el valor anterior, el nuevo valor, la justificación y el responsable.
- **Bitácora de Auditoría Global (`AuditLog`)**: Se registran cronológicamente todas las acciones críticas: inicio de tablas, cargas de archivo, análisis de IA, decisiones de aplicabilidad de la SoA y resoluciones de propuestas.

### 2.5 Manejo Seguro de Errores y Excepciones
- Se implementó un manejador de excepciones global en FastAPI que intercepta cualquier error no controlado.
- No se exponen trazas internas de Python (*tracebacks*), rutas del sistema operativo ni variables de entorno en las respuestas HTML o JSON dirigidas al cliente.

---

## 3. Advertencia de Despliegue y Limitaciones del MVP

> [!WARNING]
> **Entorno de Ejecución Local**:  
> SecAuditAI está configurado para ejecutarse exclusivamente en la interfaz de bucle invertido local (`127.0.0.1:8080`).  
> **NO exponga esta versión MVP directamente a una red pública o no confiable** sin implementar previamente:
> 1. Mecanismo de autenticación robusta y control de acceso basado en roles (RBAC).
> 2. Protección de sesiones cifradas con tokens seguros (JWT / HttpOnly Cookies).
> 3. Terminación TLS/HTTPS mediante un proxy inverso (como Nginx o Caddy).
> 4. Protección contra ataques de CSRF en formularios web.
> 5. Limitador de tasa de peticiones (Rate Limiting).
