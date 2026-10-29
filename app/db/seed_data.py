"""
Catálogo normativo oficial precargado para SecAuditAI.
Norma de referencia: ISO/IEC 27001:2022 + Enmienda 1:2024.
Los textos y descripciones son paráfrasis técnicas estructuradas en español
destinadas a la gestión y evaluación interna de cumplimiento.
"""

REQUIREMENTS_DATA = [
    # Cláusula 4: Contexto de la organización
    {
        "code": "4.1",
        "clause_number": 4,
        "title": "Comprensión de la organización y de su contexto",
        "description": "La organización debe determinar las cuestiones externas e internas pertinentes para su propósito y que afectan a su capacidad para lograr los resultados previstos de su SGSI. Nota Enmienda 1:2024: La organización debe determinar si el cambio climático es una cuestión relevante.",
        "normative_ref": "ISO/IEC 27001:2022 / Amd 1:2024, Cláusula 4.1",
    },
    {
        "code": "4.2",
        "clause_number": 4,
        "title": "Comprensión de las necesidades y expectativas de las partes interesadas",
        "description": "La organización debe determinar las partes interesadas relevantes para el SGSI, sus requisitos en seguridad de la información y cuáles de estos requisitos se abordarán en el SGSI. Nota Enmienda 1:2024: Las partes interesadas relevantes pueden tener requisitos relativos al cambio climático.",
        "normative_ref": "ISO/IEC 27001:2022 / Amd 1:2024, Cláusula 4.2",
    },
    {
        "code": "4.3",
        "clause_number": 4,
        "title": "Determinación del alcance del sistema de gestión de la seguridad de la información",
        "description": "La organización debe determinar los límites y la aplicabilidad del SGSI para establecer su alcance, considerando el contexto, las partes interesadas y las interfaces o dependencias.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 4.3",
    },
    {
        "code": "4.4",
        "clause_number": 4,
        "title": "Sistema de gestión de la seguridad de la información",
        "description": "La organización debe establecer, implementar, mantener y mejorar continuamente un SGSI, incluidos los procesos necesarios y sus interacciones, de conformidad con los requisitos de esta norma.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 4.4",
    },

    # Cláusula 5: Liderazgo
    {
        "code": "5.1",
        "clause_number": 5,
        "title": "Liderazgo y compromiso",
        "description": "La alta dirección debe demostrar liderazgo y compromiso con respecto al SGSI asegurando políticas, objetivos, integración en procesos del negocio, recursos y mejora continua.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 5.1",
    },
    {
        "code": "5.2",
        "clause_number": 5,
        "title": "Política de seguridad de la información",
        "description": "La alta dirección debe establecer una política de seguridad de la información adecuada al propósito de la organización, que proporcione un marco de objetivos y compromiso de mejora continua.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 5.2",
    },
    {
        "code": "5.3",
        "clause_number": 5,
        "title": "Roles, responsabilidades y autoridades en la organización",
        "description": "La alta dirección debe asegurarse de que las responsabilidades y autoridades para los roles pertinentes a la seguridad de la información se asignen y comuniquen en toda la organización.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 5.3",
    },

    # Cláusula 6: Planificación
    {
        "code": "6.1.1",
        "clause_number": 6,
        "title": "Acciones para abordar riesgos y oportunidades - Generalidades",
        "description": "Al planificar el SGSI, la organización debe considerar las cuestiones referidas en 4.1 y 4.2 y determinar los riesgos y oportunidades que es necesario abordar.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 6.1.1",
    },
    {
        "code": "6.1.2",
        "clause_number": 6,
        "title": "Apreciación de riesgos de seguridad de la información",
        "description": "La organización debe definir y aplicar un proceso formal de apreciación de riesgos de seguridad de la información que establezca criterios de riesgo, identifique, analice y evalúe los riesgos de confidencialidad, integridad y disponibilidad.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 6.1.2",
    },
    {
        "code": "6.1.3",
        "clause_number": 6,
        "title": "Tratamiento de riesgos de seguridad de la información",
        "description": "La organización debe definir y aplicar un proceso de tratamiento de riesgos, seleccionar opciones de tratamiento adecuadas, determinar controles necesarios, compararlos con el Anexo A y elaborar la Declaración de Aplicabilidad (SoA).",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 6.1.3",
    },
    {
        "code": "6.2",
        "clause_number": 6,
        "title": "Objetivos de seguridad de la información y planificación para alcanzarlos",
        "description": "La organización debe establecer objetivos de seguridad de la información en funciones y niveles pertinentes, que sean medibles, comunicados, actualizados y dispongan de planes de acción con recursos y plazos.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 6.2",
    },
    {
        "code": "6.3",
        "clause_number": 6,
        "title": "Planificación de los cambios",
        "description": "Cuando la organización determine la necesidad de realizar cambios en el SGSI, estos cambios se deben llevar a cabo de manera planificada.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 6.3",
    },

    # Cláusula 7: Apoyo
    {
        "code": "7.1",
        "clause_number": 7,
        "title": "Recursos",
        "description": "La organización debe determinar y proporcionar los recursos necesarios para el establecimiento, implementación, mantenimiento y mejora continua del SGSI.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.1",
    },
    {
        "code": "7.2",
        "clause_number": 7,
        "title": "Competencia",
        "description": "La organización debe determinar la competencia necesaria de las personas que realizan trabajos bajo su control que afecten a su desempeño en seguridad, y asegurar dicha competencia sobre la base de educación, formación o experiencia.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.2",
    },
    {
        "code": "7.3",
        "clause_number": 7,
        "title": "Concienciación",
        "description": "Las personas que realizan trabajos bajo el control de la organización deben ser conscientes de la política de seguridad, su contribución a la eficacia del SGSI y las implicaciones de no cumplir los requisitos.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.3",
    },
    {
        "code": "7.4",
        "clause_number": 7,
        "title": "Comunicación",
        "description": "La organización debe determinar la necesidad de comunicaciones internas y externas pertinentes al SGSI: qué comunicar, cuándo comunicar, con quién comunicar y quién debe comunicar.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.4",
    },
    {
        "code": "7.5.1",
        "clause_number": 7,
        "title": "Información documentada - Generalidades",
        "description": "El SGSI debe incluir la información documentada requerida por la norma y la determinada por la organización como necesaria para la eficacia del sistema.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.5.1",
    },
    {
        "code": "7.5.2",
        "clause_number": 7,
        "title": "Creación y actualización de la información documentada",
        "description": "Al crear y actualizar información documentada, la organización debe asegurar identificación, formato, medios y revisión/aprobación de idoneidad y adecuación.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.5.2",
    },
    {
        "code": "7.5.3",
        "clause_number": 7,
        "title": "Control de la información documentada",
        "description": "La información documentada requerida por el SGSI se debe controlar para asegurar disponibilidad, idoneidad, protección adecuada, distribución, acceso, recuperación, almacenamiento y conservación.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 7.5.3",
    },

    # Cláusula 8: Operación
    {
        "code": "8.1",
        "clause_number": 8,
        "title": "Planificación y control operacional",
        "description": "La organización debe planificar, implementar y controlar los procesos necesarios para cumplir los requisitos de seguridad y ejecutar las acciones determinadas en la cláusula 6.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 8.1",
    },
    {
        "code": "8.2",
        "clause_number": 8,
        "title": "Apreciación de los riesgos de seguridad de la información en operación",
        "description": "La organización debe realizar evaluaciones de riesgos de seguridad de la información a intervalos planificados o cuando se propongan o se produzcan cambios significativos.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 8.2",
    },
    {
        "code": "8.3",
        "clause_number": 8,
        "title": "Tratamiento de los riesgos de seguridad de la información en operación",
        "description": "La organización debe implementar el plan de tratamiento de riesgos de seguridad de la información y conservar información documentada de los resultados del tratamiento.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 8.3",
    },

    # Cláusula 9: Evaluación del desempeño
    {
        "code": "9.1",
        "clause_number": 9,
        "title": "Seguimiento, medición, análisis y evaluación",
        "description": "La organización debe evaluar el desempeño de la seguridad de la información y la eficacia del SGSI determinando qué necesita seguimiento, métodos, plazos y responsables.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.1",
    },
    {
        "code": "9.2.1",
        "clause_number": 9,
        "title": "Auditoría interna - Generalidades",
        "description": "La organización debe llevar a cabo auditorías internas a intervalos planificados para proporcionar información sobre si el SGSI es conforme con los requisitos propios y de la norma y si está implementado y mantenido eficazmente.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.2.1",
    },
    {
        "code": "9.2.2",
        "clause_number": 9,
        "title": "Programa de auditoría interna",
        "description": "La organización debe planificar, establecer, implementar y mantener programas de auditoría que incluyan frecuencia, métodos, responsabilidades, planificación e informes.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.2.2",
    },
    {
        "code": "9.3.1",
        "clause_number": 9,
        "title": "Revisión por la dirección - Generalidades",
        "description": "La alta dirección debe revisar el SGSI de la organización a intervalos planificados para asegurarse de su continua conveniencia, adecuación y eficacia.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.3.1",
    },
    {
        "code": "9.3.2",
        "clause_number": 9,
        "title": "Entradas de la revisión por la dirección",
        "description": "La revisión por la dirección debe incluir el estado de acciones previas, cambios en cuestiones internas/externas, retroalimentación del desempeño, resultados de auditorías y oportunidades de mejora.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.3.2",
    },
    {
        "code": "9.3.3",
        "clause_number": 9,
        "title": "Resultados de la revisión por la dirección",
        "description": "Los resultados de la revisión por la dirección deben incluir decisiones relacionadas con las oportunidades de mejora continua y cualquier necesidad de cambio en el SGSI.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 9.3.3",
    },

    # Cláusula 10: Mejora
    {
        "code": "10.1",
        "clause_number": 10,
        "title": "Mejora continua",
        "description": "La organización debe mejorar continuamente la conveniencia, adecuación y eficacia del sistema de gestión de la seguridad de la información.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 10.1",
    },
    {
        "code": "10.2",
        "clause_number": 10,
        "title": "No conformidad y acción correctiva",
        "description": "Cuando ocurra una no conformidad, la organización debe reaccionar ante ella, tomar acciones para controlarla y corregirla, evaluar la causa raíz e implementar acciones correctivas conservando información documentada.",
        "normative_ref": "ISO/IEC 27001:2022, Cláusula 10.2",
    },
]

ANNEX_CONTROLS_DATA = [
    # -------------------------------------------------------------
    # A.5: Controles organizacionales (37 controles)
    # -------------------------------------------------------------
    {
        "code": "A.5.1",
        "category": "Organizacional",
        "title": "Políticas para la seguridad de la información",
        "description": "La política de seguridad de la información y las políticas específicas deben ser definidas, aprobadas por la dirección, publicadas, comunicadas y revisadas a intervalos planificados.",
    },
    {
        "code": "A.5.2",
        "category": "Organizacional",
        "title": "Roles y responsabilidades de seguridad de la información",
        "description": "Los roles y responsabilidades en seguridad de la información deben definirse y asignarse de acuerdo con las necesidades de la organización.",
    },
    {
        "code": "A.5.3",
        "category": "Organizacional",
        "title": "Segregación de funciones",
        "description": "Las funciones y áreas de responsabilidad conflictivas deben separarse para reducir las oportunidades de modificación no autorizada o uso indebido de los activos.",
    },
    {
        "code": "A.5.4",
        "category": "Organizacional",
        "title": "Responsabilidades de la dirección",
        "description": "La dirección debe exigir a todo el personal que aplique la seguridad de acuerdo con las políticas y procedimientos establecidos.",
    },
    {
        "code": "A.5.5",
        "category": "Organizacional",
        "title": "Contacto con autoridades",
        "description": "La organización debe mantener contactos apropiados con las autoridades pertinentes para responder a incidentes y cumplir obligaciones legales.",
    },
    {
        "code": "A.5.6",
        "category": "Organizacional",
        "title": "Contacto con grupos de interés especial",
        "description": "La organización debe mantener contacto adecuado con grupos de interés especial, asociaciones profesionales y foros de seguridad.",
    },
    {
        "code": "A.5.7",
        "category": "Organizacional",
        "title": "Inteligencia sobre amenazas",
        "description": "La información relativa a amenazas de seguridad de la información debe recopilarse y analizarse para generar inteligencia de amenazas y adoptar contramedidas.",
    },
    {
        "code": "A.5.8",
        "category": "Organizacional",
        "title": "Seguridad de la información en la gestión de proyectos",
        "description": "La seguridad de la información debe integrarse en la gestión de proyectos, independientemente de la naturaleza del proyecto.",
    },
    {
        "code": "A.5.9",
        "category": "Organizacional",
        "title": "Inventario de información y otros activos asociados",
        "description": "Se debe desarrollar y mantener un inventario de información y otros activos asociados, incluidos sus propietarios.",
    },
    {
        "code": "A.5.10",
        "category": "Organizacional",
        "title": "Uso aceptable de la información y otros activos asociados",
        "description": "Deben identificarse, documentarse e implementarse normas para el uso aceptable y procedimientos de manejo para la información y activos asociados.",
    },
    {
        "code": "A.5.11",
        "category": "Organizacional",
        "title": "Devolución de activos",
        "description": "El personal y partes interesadas externas deben devolver todos los activos de la organización en su posesión al término de su empleo, contrato o acuerdo.",
    },
    {
        "code": "A.5.12",
        "category": "Organizacional",
        "title": "Clasificación de la información",
        "description": "La información debe clasificarse de acuerdo con las necesidades de seguridad basadas en confidencialidad, integridad, disponibilidad y requisitos legales.",
    },
    {
        "code": "A.5.13",
        "category": "Organizacional",
        "title": "Etiquetado de la información",
        "description": "Debe desarrollarse e implementarse un conjunto adecuado de procedimientos para el etiquetado de la información según el esquema de clasificación adoptado.",
    },
    {
        "code": "A.5.14",
        "category": "Organizacional",
        "title": "Transferencia de información",
        "description": "Deben establecerse reglas, procedimientos o acuerdos de transferencia de información para todo tipo de instalaciones de transferencia en la organización.",
    },
    {
        "code": "A.5.15",
        "category": "Organizacional",
        "title": "Control de acceso",
        "description": "Las reglas para controlar el acceso físico y lógico a la información y otros activos asociados deben definirse y aplicarse según requisitos de negocio y seguridad.",
    },
    {
        "code": "A.5.16",
        "category": "Organizacional",
        "title": "Gestión de identidades",
        "description": "El ciclo de vida completo de las identidades debe gestionarse desde su creación hasta su revocación.",
    },
    {
        "code": "A.5.17",
        "category": "Organizacional",
        "title": "Información de autenticación",
        "description": "La asignación y gestión de la información de autenticación secreta debe controlarse mediante un proceso de gestión formal.",
    },
    {
        "code": "A.5.18",
        "category": "Organizacional",
        "title": "Derechos de acceso",
        "description": "Los derechos de acceso a la información y otros activos asociados deben asignarse, revisarse, modificarse y eliminarse de acuerdo con la política de control de acceso.",
    },
    {
        "code": "A.5.19",
        "category": "Organizacional",
        "title": "Seguridad de la información en las relaciones con proveedores",
        "description": "Deben definirse e implementarse procesos y procedimientos para mitigar los riesgos de seguridad asociados con el acceso de proveedores a los activos.",
    },
    {
        "code": "A.5.20",
        "category": "Organizacional",
        "title": "Tratamiento de la seguridad en los acuerdos con proveedores",
        "description": "Los requisitos pertinentes de seguridad de la información deben establecerse y acordarse formalmente con cada proveedor.",
    },
    {
        "code": "A.5.21",
        "category": "Organizacional",
        "title": "Gestión de la seguridad en la cadena de suministro de TIC",
        "description": "Deben definirse e implementarse procesos y procedimientos para gestionar los riesgos de seguridad de la información asociados con la cadena de suministro de productos y servicios de TIC.",
    },
    {
        "code": "A.5.22",
        "category": "Organizacional",
        "title": "Seguimiento, revisión y gestión del cambio en los servicios de proveedores",
        "description": "La organización debe supervisar, revisar, auditar y gestionar periódicamente los cambios en las prácticas de seguridad de los proveedores y la prestación de servicios.",
    },
    {
        "code": "A.5.23",
        "category": "Organizacional",
        "title": "Seguridad de la información para el uso de servicios en la nube",
        "description": "Los procesos de adquisición, uso, gestión y salida de servicios en la nube deben establecerse conforme a los requisitos de seguridad de la organización.",
    },
    {
        "code": "A.5.24",
        "category": "Organizacional",
        "title": "Planificación y preparación para la gestión de incidentes de seguridad",
        "description": "La organización debe planificar y prepararse para gestionar incidentes de seguridad de la información definiendo, estableciendo y comunicando procesos, roles y responsabilidades.",
    },
    {
        "code": "A.5.25",
        "category": "Organizacional",
        "title": "Evaluación y decisión sobre eventos de seguridad de la información",
        "description": "La organización debe evaluar los eventos de seguridad de la información y decidir si deben clasificarse formalmente como incidentes de seguridad.",
    },
    {
        "code": "A.5.26",
        "category": "Organizacional",
        "title": "Respuesta a incidentes de seguridad de la información",
        "description": "Los incidentes de seguridad de la información deben responderse de acuerdo con los procedimientos documentados y comunicarse oportunamente.",
    },
    {
        "code": "A.5.27",
        "category": "Organizacional",
        "title": "Aprendizaje de los incidentes de seguridad de la información",
        "description": "El conocimiento adquirido a partir de incidentes de seguridad debe utilizarse para fortalecer y mejorar los controles de seguridad.",
    },
    {
        "code": "A.5.28",
        "category": "Organizacional",
        "title": "Recolección de evidencia",
        "description": "La organización debe definir y aplicar procedimientos para la identificación, recolección, adquisición y preservación de evidencia relacionada con incidentes de seguridad.",
    },
    {
        "code": "A.5.29",
        "category": "Organizacional",
        "title": "Seguridad de la información durante una interrupción",
        "description": "La organización debe planificar cómo mantener la seguridad de la información en el nivel requerido durante situaciones de contingencia o interrupción.",
    },
    {
        "code": "A.5.30",
        "category": "Organizacional",
        "title": "Preparación de las TIC para la continuidad del negocio",
        "description": "La continuidad de las TIC debe planificarse, implementarse, mantenerse y probarse en función de los objetivos de continuidad del negocio y requisitos de continuidad de TIC.",
    },
    {
        "code": "A.5.31",
        "category": "Organizacional",
        "title": "Requisitos legales, estatutarios, reglamentarios y contractuales",
        "description": "Los requisitos legales, estatutarios, reglamentarios y contractuales aplicables a la seguridad de la información deben identificarse, documentarse y mantenerse actualizados.",
    },
    {
        "code": "A.5.32",
        "category": "Organizacional",
        "title": "Derechos de propiedad intelectual",
        "description": "La organización debe implementar procedimientos adecuados para proteger los derechos de propiedad intelectual y el cumplimiento con licencias de software.",
    },
    {
        "code": "A.5.33",
        "category": "Organizacional",
        "title": "Protección de registros",
        "description": "Los registros deben protegerse contra pérdida, destrucción, falsificación, acceso no autorizado y divulgación indebida de acuerdo con requisitos legales y de negocio.",
    },
    {
        "code": "A.5.34",
        "category": "Organizacional",
        "title": "Privacidad y protección de datos personales (PII)",
        "description": "La organización debe garantizar la privacidad y la protección de los datos de carácter personal conforme a las leyes y reglamentaciones aplicables.",
    },
    {
        "code": "A.5.35",
        "category": "Organizacional",
        "title": "Revisión independiente de la seguridad de la información",
        "description": "El enfoque de la organización para gestionar la seguridad de la información y su implementación deben revisarse de forma independiente a intervalos planificados.",
    },
    {
        "code": "A.5.36",
        "category": "Organizacional",
        "title": "Cumplimiento de políticas y normas de seguridad",
        "description": "Los administradores y responsables deben revisar periódicamente la conformidad del procesamiento de información y los procedimientos con las políticas y normas de seguridad.",
    },
    {
        "code": "A.5.37",
        "category": "Organizacional",
        "title": "Procedimientos operativos documentados",
        "description": "Los procedimientos operativos para las instalaciones de procesamiento de información deben documentarse y ponerse a disposición de todo el personal que los requiera.",
    },

    # -------------------------------------------------------------
    # A.6: Controles de personas (8 controles)
    # -------------------------------------------------------------
    {
        "code": "A.6.1",
        "category": "Personas",
        "title": "Selección y verificación de antecedentes",
        "description": "Las verificaciones de antecedentes de todos los candidatos para el empleo deben llevarse a cabo de acuerdo con las leyes y reglamentos pertinentes y proporcionales a los riesgos.",
    },
    {
        "code": "A.6.2",
        "category": "Personas",
        "title": "Términos y condiciones del empleo",
        "description": "Los acuerdos contractuales de empleo deben establecer las responsabilidades del empleado y de la organización en materia de seguridad de la información.",
    },
    {
        "code": "A.6.3",
        "category": "Personas",
        "title": "Concienciación, formación y educación en seguridad",
        "description": "El personal de la organización y las partes interesadas pertinentes deben recibir una formación y actualizaciones adecuadas en materia de concienciación sobre seguridad.",
    },
    {
        "code": "A.6.4",
        "category": "Personas",
        "title": "Proceso disciplinario",
        "description": "Debe existir un proceso disciplinario formalizado y comunicado para tomar medidas contra el personal que haya cometido infracciones de seguridad de la información.",
    },
    {
        "code": "A.6.5",
        "category": "Personas",
        "title": "Responsabilidades tras la terminación o cambio de empleo",
        "description": "Las responsabilidades y deberes de seguridad de la información que sigan siendo válidos tras la terminación o cambio de empleo deben definirse, comunicarse y hacerse cumplir.",
    },
    {
        "code": "A.6.6",
        "category": "Personas",
        "title": "Acuerdos de confidencialidad o no divulgación",
        "description": "Los acuerdos de confidencialidad o no divulgación que reflejen las necesidades de la organización para la protección de la información deben identificarse, documentarse y revisarse.",
    },
    {
        "code": "A.6.7",
        "category": "Personas",
        "title": "Trabajo remoto",
        "description": "Deben implementarse medidas de seguridad cuando los miembros del personal realicen trabajo remoto para proteger la información accedida o procesada fuera de las instalaciones.",
    },
    {
        "code": "A.6.8",
        "category": "Personas",
        "title": "Notificación de eventos de seguridad de la información",
        "description": "La organización debe proporcionar un mecanismo para que el personal informe oportunamente los eventos de seguridad observados o sospechados a través de canales designados.",
    },

    # -------------------------------------------------------------
    # A.7: Controles físicos (14 controles)
    # -------------------------------------------------------------
    {
        "code": "A.7.1",
        "category": "Físico",
        "title": "Perímetros de seguridad física",
        "description": "Los perímetros de seguridad deben definirse y utilizarse para proteger las áreas que contienen información sensible o crítica e instalaciones de procesamiento.",
    },
    {
        "code": "A.7.2",
        "category": "Físico",
        "title": "Entrada física",
        "description": "Las áreas seguras deben estar protegidas por controles de entrada apropiados para garantizar que solo se permita el acceso al personal autorizado.",
    },
    {
        "code": "A.7.3",
        "category": "Físico",
        "title": "Aseguramiento de oficinas, salas e instalaciones",
        "description": "La seguridad física para oficinas, salas e instalaciones debe diseñarse e implementarse de forma acorde con los activos albergados.",
    },
    {
        "code": "A.7.4",
        "category": "Físico",
        "title": "Monitorización de la seguridad física",
        "description": "Las instalaciones deben ser monitorizadas continuamente mediante sistemas de vigilancia o guardias para detectar accesos físicos no autorizados.",
    },
    {
        "code": "A.7.5",
        "category": "Físico",
        "title": "Protección contra amenazas físicas y ambientales",
        "description": "Debe diseñarse e implementarse protección contra desastres naturales y otras amenazas físicas o ambientales provocadas por el hombre.",
    },
    {
        "code": "A.7.6",
        "category": "Físico",
        "title": "Trabajo en áreas seguras",
        "description": "Deben diseñarse e implementarse medidas de seguridad para trabajar en áreas seguras con el fin de evitar accesos indebidos.",
    },
    {
        "code": "A.7.7",
        "category": "Físico",
        "title": "Escritorio limpio y pantalla limpia",
        "description": "Deben definirse y aplicarse adecuadamente reglas de escritorio limpio para papeles y medios de almacenamiento extraíbles y de pantalla limpia para instalaciones de procesamiento.",
    },
    {
        "code": "A.7.8",
        "category": "Físico",
        "title": "Emplazamiento y protección de equipos",
        "description": "El equipo debe ubicarse de manera segura y protegerse para reducir los riesgos derivados de peligros ambientales y oportunidades de acceso no autorizado.",
    },
    {
        "code": "A.7.9",
        "category": "Físico",
        "title": "Seguridad de los activos fuera de las instalaciones",
        "description": "Los activos fuera de las instalaciones deben protegerse teniendo en cuenta los diferentes riesgos de trabajar fuera de las instalaciones de la organización.",
    },
    {
        "code": "A.7.10",
        "category": "Físico",
        "title": "Medios de almacenamiento",
        "description": "Los medios de almacenamiento deben gestionarse durante su ciclo de vida de adquisición, uso, transporte y eliminación de acuerdo con el esquema de clasificación.",
    },
    {
        "code": "A.7.11",
        "category": "Físico",
        "title": "Servicios de suministro e infraestructuras de soporte",
        "description": "Las instalaciones de procesamiento de información deben protegerse contra fallos de energía y otras perturbaciones causadas por fallos en servicios de suministro.",
    },
    {
        "code": "A.7.12",
        "category": "Físico",
        "title": "Seguridad del cableado",
        "description": "El cableado que transporta energía, datos o servicios de soporte de información debe protegerse contra intercepciones, interferencias o daños.",
    },
    {
        "code": "A.7.13",
        "category": "Físico",
        "title": "Mantenimiento de equipos",
        "description": "Los equipos deben mantenerse correctamente para garantizar su continua disponibilidad e integridad.",
    },
    {
        "code": "A.7.14",
        "category": "Físico",
        "title": "Eliminación segura o reutilización de equipos",
        "description": "Los elementos de los equipos que contengan medios de almacenamiento deben verificarse para garantizar que cualquier información confidencial haya sido borrada o destruida.",
    },

    # -------------------------------------------------------------
    # A.8: Controles tecnológicos (34 controles)
    # -------------------------------------------------------------
    {
        "code": "A.8.1",
        "category": "Tecnológico",
        "title": "Dispositivos de usuario final",
        "description": "La información almacenada, procesada o transmitida por dispositivos de usuario final debe protegerse mediante políticas y configuraciones de seguridad.",
    },
    {
        "code": "A.8.2",
        "category": "Tecnológico",
        "title": "Derechos de acceso privilegiado",
        "description": "La asignación y el uso de derechos de acceso privilegiado deben restringirse, gestionarse y controlarse estrictamente.",
    },
    {
        "code": "A.8.3",
        "category": "Tecnológico",
        "title": "Restricción de acceso a la información",
        "description": "El acceso a la información y a las funciones de las aplicaciones debe restringirse de acuerdo con la política de control de acceso establecida.",
    },
    {
        "code": "A.8.4",
        "category": "Tecnológico",
        "title": "Acceso al código fuente",
        "description": "El acceso de lectura y escritura al código fuente, herramientas de desarrollo y bibliotecas debe gestionarse y controlarse adecuadamente.",
    },
    {
        "code": "A.8.5",
        "category": "Tecnológico",
        "title": "Autenticación segura",
        "description": "Deben implementarse tecnologías y procedimientos de autenticación segura basados en la criticidad y clasificación de la información (ej. MFA).",
    },
    {
        "code": "A.8.6",
        "category": "Tecnológico",
        "title": "Gestión de capacidad",
        "description": "El uso de recursos debe supervisarse y ajustarse en función de los requisitos de capacidad actuales y previstos para garantizar el rendimiento del sistema.",
    },
    {
        "code": "A.8.7",
        "category": "Tecnológico",
        "title": "Protección contra malware",
        "description": "Debe implementarse protección contra malware respaldada por una adecuada concienciación de los usuarios y defensas automatizadas.",
    },
    {
        "code": "A.8.8",
        "category": "Tecnológico",
        "title": "Gestión de vulnerabilidades técnicas",
        "description": "La información sobre las vulnerabilidades técnicas de los sistemas de información debe obtenerse oportunamente, evaluando la exposición y aplicando parches.",
    },
    {
        "code": "A.8.9",
        "category": "Tecnológico",
        "title": "Gestión de la configuración",
        "description": "Las configuraciones, incluidas las configuraciones de seguridad de hardware, software, servicios y redes, deben establecerse, documentarse, aplicarse y monitorizarse.",
    },
    {
        "code": "A.8.10",
        "category": "Tecnológico",
        "title": "Eliminación de información",
        "description": "La información almacenada en los sistemas de información, dispositivos o medios de almacenamiento debe eliminarse cuando ya no sea necesaria conforme a políticas.",
    },
    {
        "code": "A.8.11",
        "category": "Tecnológico",
        "title": "Enmascaramiento de datos",
        "description": "El enmascaramiento de datos (seudonimización, anonimización) debe utilizarse de acuerdo con la política de control de acceso y requisitos de privacidad.",
    },
    {
        "code": "A.8.12",
        "category": "Tecnológico",
        "title": "Prevención de fuga de datos (DLP)",
        "description": "Deben aplicarse medidas de prevención de fuga de datos a los sistemas, redes y otros dispositivos que procesen o almacenen información sensible.",
    },
    {
        "code": "A.8.13",
        "category": "Tecnológico",
        "title": "Copias de seguridad de la información",
        "description": "Deben realizarse copias de seguridad periódicas de la información, el software y los sistemas, y probarse periódicamente de acuerdo con la política de copias.",
    },
    {
        "code": "A.8.14",
        "category": "Tecnológico",
        "title": "Redundancia de los recursos de procesamiento",
        "description": "Las instalaciones de procesamiento de información deben implementarse con redundancia suficiente para cumplir con los requisitos de disponibilidad.",
    },
    {
        "code": "A.8.15",
        "category": "Tecnológico",
        "title": "Registro y monitorización (Logging)",
        "description": "Los registros que registran eventos, actividades de usuarios, excepciones y fallos deben generarse, protegerse contra manipulación y revisarse periódicamente.",
    },
    {
        "code": "A.8.16",
        "category": "Tecnológico",
        "title": "Actividades de monitorización",
        "description": "Las redes, sistemas y aplicaciones deben ser monitorizados para detectar comportamientos anómalos o sospechosos y tomar las medidas oportunas.",
    },
    {
        "code": "A.8.17",
        "category": "Tecnológico",
        "title": "Sincronización de relojes",
        "description": "Los relojes de los sistemas de procesamiento de información de la organización deben sincronizarse con fuentes de tiempo de referencia aprobadas (NTP).",
    },
    {
        "code": "A.8.18",
        "category": "Tecnológico",
        "title": "Uso de programas de utilidad privilegiados",
        "description": "El uso de programas de utilidad que puedan ser capaces de eludir los controles del sistema y de las aplicaciones debe restringirse y controlarse estrictamente.",
    },
    {
        "code": "A.8.19",
        "category": "Tecnológico",
        "title": "Instalación de software en sistemas operacionales",
        "description": "Deben establecerse e implementarse procedimientos para controlar de forma segura la instalación de software en los sistemas operacionales.",
    },
    {
        "code": "A.8.20",
        "category": "Tecnológico",
        "title": "Seguridad de las redes",
        "description": "Las redes y los dispositivos de red deben protegerse, gestionarse y controlarse para salvaguardar la información en los sistemas y aplicaciones.",
    },
    {
        "code": "A.8.21",
        "category": "Tecnológico",
        "title": "Seguridad de los servicios de red",
        "description": "Los mecanismos de seguridad, los niveles de servicio y los requisitos de gestión de los servicios de red deben identificarse e incluirse en los acuerdos de red.",
    },
    {
        "code": "A.8.22",
        "category": "Tecnológico",
        "title": "Segregación en redes",
        "description": "Los grupos de servicios de información, usuarios y sistemas deben segregarse en redes lógicas o físicas diferenciadas.",
    },
    {
        "code": "A.8.23",
        "category": "Tecnológico",
        "title": "Filtrado web",
        "description": "El acceso a sitios web externos debe gestionarse para reducir la exposición a contenidos maliciosos o no autorizados.",
    },
    {
        "code": "A.8.24",
        "category": "Tecnológico",
        "title": "Uso de criptografía",
        "description": "Deben definirse e implementarse reglas para el uso eficaz de la criptografía, incluida la gestión de claves criptográficas, para proteger la información.",
    },
    {
        "code": "A.8.25",
        "category": "Tecnológico",
        "title": "Ciclo de vida de desarrollo seguro",
        "description": "Deben establecerse y aplicarse reglas para el desarrollo seguro de software y sistemas en todo el ciclo de vida de desarrollo de software (SDLC).",
    },
    {
        "code": "A.8.26",
        "category": "Tecnológico",
        "title": "Requisitos de seguridad en aplicaciones",
        "description": "Los requisitos de seguridad de la información deben identificarse, especificarse y aprobarse al desarrollar o adquirir aplicaciones.",
    },
    {
        "code": "A.8.27",
        "category": "Tecnológico",
        "title": "Arquitectura y principios de ingeniería de sistemas seguros",
        "description": "Los principios para la ingeniería de sistemas seguros deben establecerse, documentarse, mantenerse y aplicarse a cualquier actividad de desarrollo de sistemas.",
    },
    {
        "code": "A.8.28",
        "category": "Tecnológico",
        "title": "Codificación segura",
        "description": "Los principios de codificación segura deben aplicarse al desarrollo de software para evitar vulnerabilidades de software habituales (OWASP).",
    },
    {
        "code": "A.8.29",
        "category": "Tecnológico",
        "title": "Pruebas de seguridad en desarrollo y aceptación",
        "description": "Los procesos de prueba de seguridad deben definirse e implementarse durante el ciclo de vida de desarrollo y en la fase de aceptación previa al despliegue.",
    },
    {
        "code": "A.8.30",
        "category": "Tecnológico",
        "title": "Desarrollo externalizado",
        "description": "La organización debe supervisar, monitorizar y revisar las actividades de desarrollo de software subcontratadas para verificar el cumplimiento de seguridad.",
    },
    {
        "code": "A.8.31",
        "category": "Tecnológico",
        "title": "Separación de entornos de desarrollo, prueba y producción",
        "description": "Los entornos de desarrollo, prueba y producción deben separarse y protegerse para evitar accesos no autorizados y cambios en los sistemas operacionales.",
    },
    {
        "code": "A.8.32",
        "category": "Tecnológico",
        "title": "Gestión del cambio",
        "description": "Los cambios en las instalaciones de procesamiento de información y en los sistemas de información deben someterse a procedimientos formales de control de cambios.",
    },
    {
        "code": "A.8.33",
        "category": "Tecnológico",
        "title": "Información sobre pruebas",
        "description": "Los datos de prueba deben seleccionarse, protegerse y gestionarse adecuadamente evitando el uso de datos personales reales no enmascarados.",
    },
    {
        "code": "A.8.34",
        "category": "Tecnológico",
        "title": "Protección de los sistemas de información durante las pruebas de auditoría",
        "description": "Las pruebas de auditoría y otras actividades de aseguramiento que involucren la evaluación de sistemas operacionales deben planificarse y acordarse para minimizar interrupciones.",
    },
]
