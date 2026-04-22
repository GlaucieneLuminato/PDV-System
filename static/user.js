const API_BASE = "https://pdv-system-c359.onrender.com";

const API_USERS = API_BASE + "/api/users/";
const API_ME = API_BASE + "/api/me/";
const API_LOGIN = API_BASE + "/api/token/";
const API_REFRESH = API_BASE + "/api/token/refresh/";

// ===================== ESTADO =====================
let users = [];

// ===================== TOKEN =====================
function getToken() {
    return localStorage.getItem("access");
}

// ===================== LOGIN =====================
async function login(event) {
    event.preventDefault();

    const username = document.getElementById("usuario").value.trim();
    const password = document.getElementById("senha").value.trim();

    console.log("LOGIN:", username, password);

    try {
        const response = await fetch(API_LOGIN, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Erro login:", data);
            alert("Usuário ou senha inválidos!");
            return;
        }

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        const userResponse = await fetch(API_ME, {
            headers: {
                "Authorization": `Bearer ${data.access}`
            }
        });

        if (!userResponse.ok) {
            console.error("Erro ao buscar perfil:", userResponse.status);
            return;
        }

        const userData = await userResponse.json();
        localStorage.setItem("tipo", userData.tipo);

        window.location.href = "/dashboard/";

    } catch (error) {
        console.error("Erro login:", error);
        alert("Erro ao conectar com servidor");
    }
}
// ===================== PROTEÇÃO DE ROTAS =====================
function verificarLogin() {
    const token = getToken();

    if (!token) {
        window.location.href = "login.html";
    }
}

document.addEventListener("DOMContentLoaded", verificarLogin);

// ===================== USUÁRIOS =====================
async function carregarUsuarios() {
    try {
        const resposta = await fetch(API_USERS, {
            headers: {
                "Authorization": `Bearer ${getToken()}`
            }
        });

        if (!resposta.ok) {
            console.error("Erro ao carregar usuários");
            return;
        }

        users = await resposta.json();
        renderUsers(users);

    } catch (error) {
        console.error("Erro:", error);
    }
}

async function saveUser() {
    const user = {
        username: document.getElementById("userName").value,
        email: document.getElementById("userEmail").value,
        password: document.getElementById("userPassword").value,
        role: document.getElementById("userRole").value,
    };

    try {
        const resposta = await fetch(API_USERS, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(user)
        });

        if (resposta.ok) {
            mostrarToast("Usuário criado com sucesso");
            carregarUsuarios();
        } else {
            mostrarToast("Erro ao criar usuário", "error");
        }

    } catch (error) {
        console.error("Erro:", error);
    }
}

// ===================== RENDER USUÁRIOS =====================
function renderUsers(lista) {
    const tbody = document.getElementById("usersTableBody");

    if (!tbody) return;

    tbody.innerHTML = "";

    lista.forEach(user => {

        const statusBadge = user.status === "active"
            ? `<span class="badge bg-success">Ativo</span>`
            : `<span class="badge bg-secondary">Inativo</span>`;

        const roleName = {
            admin: "Administrador",
            manager: "Gerente",
            operator: "Operador",
            viewer: "Visualizador"
        };

        const linha = `
        <tr>
            <td>${user.username || "-"}</td>
            <td>${user.email || "-"}</td>
            <td>${roleName[user.role] || user.role}</td>
            <td>${statusBadge}</td>
            <td>${user.last_access || "-"}</td>
            <td>
                <i class="bi bi-pencil" style="cursor:pointer"
                   onclick="editarUser(${user.id})"></i>

                <i class="bi bi-trash" style="cursor:pointer; color:red;"
                   onclick="deletarUser(${user.id})"></i>
            </td>
        </tr>
        `;

        tbody.innerHTML += linha;
    });
}

// ===================== TOAST =====================
function mostrarToast(mensagem, tipo = "success") {
    Toastify({
        text: mensagem,
        duration: 3000,
        gravity: "top",
        position: "right",
        background: tipo === "success" ? "#28a745" : "#dc3545",
    }).showToast();
}

// ===================== INIT =====================
document.addEventListener("DOMContentLoaded", () => {
    verificarLogin();
    carregarUsuarios();
});

// expõe funções globais
window.login = login;
window.saveUser = saveUser;