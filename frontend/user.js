let users = [];

async function carregarUsuarios(){
    const resposta = await fetch("https://pdv-system-c359.onrender.com/api/users/", {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        }
    });

    users = await resposta.json();
    renderUsers(users);
}


async function saveUser(){
    const user = {
        username: document.getElementById("userName").value,
        email: document.getElementById("userEmail").value,
        password: document.getElementById("userPassword").value,
        role: document.getElementById("userRole").value,
    };

    const resposta = await fetch("https://pdv-system-c359.onrender.com/api/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        },
        body: JSON.stringify(user)
    });

    if(resposta.ok){
        mostrarToast("Usuário criado com sucesso");
        carregarUsuarios();
    } else {
        mostrarToast("Erro ao criar usuário", "error");
    }
}

function renderUsers(lista){
    const tbody = document.getElementById("usersTableBody");

    if(!tbody){
        console.warn("Tabela de usuários não encontrada!");
        return;
    }

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
            <td>${user.name || "-"}</td>
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


function verificarLogin(){
    const token = localStorage.getItem("access");

    if(!token){
        window.location.href = "login.html";
    }
}

document.addEventListener("DOMContentLoaded", verificarLogin);

async function login(event) {
    event.preventDefault();

    const username = document.getElementById("userName").value;
    const password = document.getElementById("userPassword").value;

    try {
        const response = await fetch("https://pdv-system-c359.onrender.com/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Erro:", data);
            alert("Usuário ou senha inválidos!");
            return;
        }

        // 🔐 salva tokens
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        // 👤 pega dados do usuário
        const userResponse = await fetch("https://pdv-system-c359.onrender.com/me/", {
            headers: {
                "Authorization": `Bearer ${data.access}`
            }
        });

        const userData = await userResponse.json();

        console.log("USER DATA:", userData);

        localStorage.setItem("tipo", userData.tipo);

        // 🚀 redireciona
        window.location.href = "dashboard.html";

    } catch (error) {
        console.error("Erro geral:", error);
        alert("Erro ao conectar com servidor");
    }
}



