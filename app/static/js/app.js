/**
 * UniHub - Frontend Asíncrono y Gestión de Interfaz Dinámica
 */

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar iconos Lucide
    if (window.lucide) {
        lucide.createIcons();
    }

    // Registrar Service Worker para PWA (iOS / Android / Desktop)
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("/static/sw.js")
            .then(reg => console.log("UniHub PWA Service Worker registrado con éxito:", reg.scope))
            .catch(err => console.warn("Error al registrar Service Worker:", err));
    }
});

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl shadow-xl text-sm font-medium transition-all duration-300 transform translate-y-2 opacity-0 ${
        type === "success" ? "bg-emerald-950/90 text-emerald-200 border border-emerald-500/40" :
        type === "error" ? "bg-rose-950/90 text-rose-200 border border-rose-500/40" :
        "bg-indigo-950/90 text-indigo-200 border border-indigo-500/40"
    }`;

    const iconName = type === "success" ? "check-circle-2" : type === "error" ? "alert-circle" : "info";
    toast.innerHTML = `
        <i data-lucide="${iconName}" class="w-5 h-5 flex-shrink-0"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);
    if (window.lucide) lucide.createIcons();

    // Trigger animación de entrada
    requestAnimationFrame(() => {
        toast.classList.remove("translate-y-2", "opacity-0");
        toast.classList.add("translate-y-0", "opacity-100");
    });

    // Auto eliminar a los 3.5 segundos
    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-y-2");
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ==========================================
// MODAL CONTROLS
// ==========================================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");
        if (window.lucide) lucide.createIcons();
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
    }
}

// Cerrar modal al hacer click en el backdrop
window.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-backdrop")) {
        e.target.closest(".modal-root")?.classList.add("hidden");
        e.target.closest(".modal-root")?.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
    }
});

// ==========================================
// API CLIENT WRAPPER (Fetch API)
// ==========================================
async function apiRequest(url, method = "GET", data = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    };
    if (data && (method === "POST" || method === "PUT" || method === "PATCH")) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (response.status === 204) {
            return { success: true };
        }
        const json = await response.json();
        if (!response.ok) {
            throw new Error(json.detail || "Ocurrió un error en el servidor");
        }
        return json;
    } catch (err) {
        console.error("API Error:", err);
        throw err;
    }
}

// ==========================================
// GESTIÓN DE MATERIAS
// ==========================================
function abrirModalCrearMateria() {
    const form = document.getElementById("form-materia");
    if (form) form.reset();
    document.getElementById("materia-modal-title").innerText = "Nueva Materia";
    document.getElementById("materia-id").value = "";
    document.getElementById("materia-color").value = "#3b82f6";
    openModal("modal-materia");
}

function abrirModalEditarMateria(materia) {
    document.getElementById("materia-modal-title").innerText = "Editar Materia";
    document.getElementById("materia-id").value = materia.id;
    document.getElementById("materia-nombre").value = materia.nombre;
    document.getElementById("materia-codigo").value = materia.codigo || "";
    document.getElementById("materia-profesor").value = materia.profesor || "";
    document.getElementById("materia-anio").value = materia.anio || 1;
    document.getElementById("materia-cuatrimestre").value = materia.cuatrimestre || 1;
    document.getElementById("materia-estado").value = materia.estado || "CURSANDO";
    document.getElementById("materia-color").value = materia.color_hex || "#3b82f6";
    document.getElementById("materia-drive").value = materia.drive_url || "";
    openModal("modal-materia");
}

async function guardarMateria(event) {
    event.preventDefault();
    const btn = document.getElementById("btn-submit-materia");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="inline-block animate-spin mr-2">⟳</span> Guardando...`;

    const id = document.getElementById("materia-id").value;
    const data = {
        nombre: document.getElementById("materia-nombre").value.trim(),
        codigo: document.getElementById("materia-codigo").value.trim() || null,
        profesor: document.getElementById("materia-profesor").value.trim() || null,
        anio: parseInt(document.getElementById("materia-anio").value) || 1,
        cuatrimestre: parseInt(document.getElementById("materia-cuatrimestre").value) || 1,
        estado: document.getElementById("materia-estado").value,
        color_hex: document.getElementById("materia-color").value || "#3b82f6",
        drive_url: document.getElementById("materia-drive").value.trim() || null
    };

    try {
        if (id) {
            await apiRequest(`/api/materias/${id}`, "PUT", data);
            showToast("Materia actualizada correctamente");
        } else {
            await apiRequest("/api/materias/", "POST", data);
            showToast("Materia registrada con éxito");
        }
        closeModal("modal-materia");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

async function eliminarMateria(id, nombre) {
    if (!confirm(`¿Estás seguro de que deseas eliminar la materia "${nombre}"? Se borrarán sus horarios y exámenes asociados.`)) {
        return;
    }
    try {
        await apiRequest(`/api/materias/${id}`, "DELETE");
        showToast(`Materia "${nombre}" eliminada`, "info");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    }
}

// Filtro interactivo de materias en la vista
function filtrarMateriasPorEstado(estado, btnElement) {
    // Actualizar botones de filtro
    document.querySelectorAll(".filtro-materia-btn").forEach(b => {
        b.classList.remove("bg-indigo-600", "text-white");
        b.classList.add("bg-slate-800/80", "text-slate-400");
    });
    if (btnElement) {
        btnElement.classList.add("bg-indigo-600", "text-white");
        btnElement.classList.remove("bg-slate-800/80", "text-slate-400");
    }

    const cards = document.querySelectorAll(".card-materia");
    cards.forEach(card => {
        const cardEstado = card.getAttribute("data-estado");
        if (estado === "TODAS" || cardEstado === estado) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

// ==========================================
// GESTIÓN DE HORARIOS
// ==========================================
function abrirModalCrearHorario(materiaId = null) {
    const form = document.getElementById("form-horario");
    if (form) form.reset();
    if (materiaId) {
        const select = document.getElementById("horario-materia-id");
        if (select) select.value = materiaId;
    }
    openModal("modal-horario");
}

async function guardarHorario(event) {
    event.preventDefault();
    const btn = document.getElementById("btn-submit-horario");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="inline-block animate-spin mr-2">⟳</span> Guardando...`;

    const data = {
        materia_id: parseInt(document.getElementById("horario-materia-id").value),
        dia_semana: document.getElementById("horario-dia").value,
        hora_inicio: document.getElementById("horario-inicio").value,
        hora_fin: document.getElementById("horario-fin").value,
        aula: document.getElementById("horario-aula").value.trim() || null
    };

    try {
        await apiRequest("/api/horarios/", "POST", data);
        showToast("Horario de cursada agregado con éxito");
        closeModal("modal-horario");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

async function eliminarHorario(id) {
    if (!confirm("¿Deseas eliminar este bloque horario?")) return;
    try {
        await apiRequest(`/api/horarios/${id}`, "DELETE");
        showToast("Horario eliminado", "info");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    }
}

// ==========================================
// GESTIÓN DE EVALUACIONES Y NOTAS
// ==========================================
function abrirModalCrearEvaluacion(materiaId = null) {
    const form = document.getElementById("form-evaluacion");
    if (form) form.reset();
    if (materiaId) {
        const select = document.getElementById("eval-materia-id");
        if (select) select.value = materiaId;
    }
    openModal("modal-evaluacion");
}

async function guardarEvaluacion(event) {
    event.preventDefault();
    const btn = document.getElementById("btn-submit-evaluacion");
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="inline-block animate-spin mr-2">⟳</span> Guardando...`;

    const notaVal = document.getElementById("eval-nota").value;
    const pesoVal = document.getElementById("eval-peso").value;

    const data = {
        materia_id: parseInt(document.getElementById("eval-materia-id").value),
        titulo: document.getElementById("eval-titulo").value.trim(),
        tipo: document.getElementById("eval-tipo").value,
        fecha: document.getElementById("eval-fecha").value,
        peso_porcentaje: pesoVal ? parseFloat(pesoVal) : 0,
        nota: notaVal !== "" ? parseFloat(notaVal) : null
    };

    try {
        await apiRequest("/api/evaluaciones/", "POST", data);
        showToast("Evaluación programada con éxito");
        closeModal("modal-evaluacion");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

async function actualizarNotaEvaluacion(id, inputElement) {
    const valor = inputElement.value.trim();
    let nota = null;
    if (valor !== "") {
        nota = parseFloat(valor);
        if (isNaN(nota) || nota < 1 || nota > 10) {
            showToast("La nota debe estar entre 1 y 10", "error");
            return;
        }
    }

    try {
        await apiRequest(`/api/evaluaciones/${id}/nota`, "PATCH", { nota });
        showToast(nota !== null ? `Nota guardada (${nota})` : "Nota removida");
        // Refrescar para actualizar promedios y badges dinámicos
        setTimeout(() => window.location.reload(), 500);
    } catch (err) {
        showToast(err.message, "error");
    }
}

async function eliminarEvaluacion(id, titulo) {
    if (!confirm(`¿Eliminar la evaluación "${titulo}"?`)) return;
    try {
        await apiRequest(`/api/evaluaciones/${id}`, "DELETE");
        showToast("Evaluación eliminada", "info");
        setTimeout(() => window.location.reload(), 600);
    } catch (err) {
        showToast(err.message, "error");
    }
}

// Filtro de evaluaciones
function filtrarEvaluaciones(filtro, btnElement) {
    document.querySelectorAll(".filtro-eval-btn").forEach(b => {
        b.classList.remove("bg-indigo-600", "text-white");
        b.classList.add("bg-slate-800/80", "text-slate-400");
    });
    if (btnElement) {
        btnElement.classList.add("bg-indigo-600", "text-white");
        btnElement.classList.remove("bg-slate-800/80", "text-slate-400");
    }

    const rows = document.querySelectorAll(".item-evaluacion");
    rows.forEach(row => {
        const tieneNota = row.getAttribute("data-tiene-nota") === "true";
        const tipo = row.getAttribute("data-tipo");

        if (filtro === "TODAS") {
            row.style.display = "";
        } else if (filtro === "PENDIENTES") {
            row.style.display = !tieneNota ? "" : "none";
        } else if (filtro === "RENDIDAS") {
            row.style.display = tieneNota ? "" : "none";
        } else if (tipo === filtro) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

// ==========================================
// CALCULADORA DE RENDIMIENTO INTERACTIVA
// ==========================================
function simularPromedio() {
    const filasSimuladas = document.querySelectorAll(".simulador-row");
    let sumaProductos = 0;
    let sumaPesos = 0;
    let totalNotas = 0;
    let sumaNotasSimple = 0;

    filasSimuladas.forEach(fila => {
        const inputNota = fila.querySelector(".sim-nota");
        const inputPeso = fila.querySelector(".sim-peso");
        const activo = fila.querySelector(".sim-activo") ? fila.querySelector(".sim-activo").checked : true;

        if (activo && inputNota && inputNota.value !== "") {
            const nota = parseFloat(inputNota.value);
            const peso = inputPeso ? parseFloat(inputPeso.value) || 0 : 0;

            if (!isNaN(nota)) {
                sumaNotasSimple += nota;
                totalNotas += 1;

                if (peso > 0) {
                    sumaProductos += (nota * peso);
                    sumaPesos += peso;
                }
            }
        }
    });

    const displayPonderado = document.getElementById("calc-promedio-ponderado");
    const displaySimple = document.getElementById("calc-promedio-simple");

    if (displaySimple) {
        displaySimple.innerText = totalNotas > 0 ? (sumaNotasSimple / totalNotas).toFixed(2) : "0.00";
    }
    if (displayPonderado) {
        if (sumaPesos > 0) {
            displayPonderado.innerText = (sumaProductos / sumaPesos).toFixed(2);
        } else if (totalNotas > 0) {
            displayPonderado.innerText = (sumaNotasSimple / totalNotas).toFixed(2);
        } else {
            displayPonderado.innerText = "0.00";
        }
    }
}
