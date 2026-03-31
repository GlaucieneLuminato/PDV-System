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

const resposta = await fetch("https://pdv-system-c359.onrender.com/api/login/", {
    method: "POST",
    headers: {
        "Content-Type":"application/json"
    },
    body: JSON.stringify({
        username: username,
        password: password 
    })
});
const data = await resposta.json();

if (data.tipo === "admin"){
    window.location.href = "admin.html";
}else {
    window.location.href = "dashboard.html"
}

console.log("TOKEN:", localStorage.getItem("access"));

const userResponse = await fetch("https://pdv-system-c359.onrender.com/api/me/", {
    headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`
    }
});

const userData = await userResponse.json();
console.log(userData);

console.log("STATUS:", userResponse.status);

const userData = await userResponse.json();

console.log("USER DATA:", userData);





