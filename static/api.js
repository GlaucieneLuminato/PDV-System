const API_BASE = "https://pdv-system-c359.onrender.com";

const API_PRODUTOS = `${API_BASE}/api/produtos/`;
const API_VENDAS = `${API_BASE}/api/vendas/`;
const API_USERS = `${API_BASE}/api/users/`;
const API_LOGIN = `${API_BASE}/api/token/`;
const API_REFRESH = `${API_BASE}/api/token/refresh/`;

// ================= TOKEN =================
function getToken(){
    return localStorage.getItem("access");
}

// ================= FETCH SEGURO =================
async function safeFetch(url, options = {}) {
    const response = await fetch(url, options);

    let data;

    try {
        data = await response.json();
    } catch {
        console.error("Resposta não é JSON:", response);
        throw new Error("Resposta inválida do servidor");
    }

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(data?.detail || "Erro na requisição");
    }

    return data;
}

// ================= LOGIN CHECK =================
function verificarLogin(){
    const token = getToken();

    if(!token){
        alert("Você precisa estar logado");
        window.location.href = "login.html";
    }
}

// ================= TOAST =================
function mostrarToast(mensagem, tipo = "success"){
    Toastify({
        text: mensagem,
        duration: 3000,
        gravity: "top",
        position: "right",
        background: tipo === "success" ? "#28a745" : "#dc3545",
    }).showToast();
}

// ================= PRODUTOS =================
let listaProdutos = [];
let produtoEditandoId = null;

async function carregarProdutos(){
    try{
        const data = await safeFetch(API_PRODUTOS, {
            headers: {
                "Authorization": `Bearer ${getToken()}`
            }
        });

        listaProdutos = data;
        renderizarProdutos(data);

    } catch(error){
        console.error("Erro ao carregar produtos:", error);
    }
}

function renderizarProdutos(produtos){
    const container = document.querySelector("#tabela-produtos");
    if(!container) return;

    container.innerHTML = "";

    produtos.forEach(produto => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${produto.nome}</td>
            <td>${produto.sku}</td>
            <td>${produto.categoria}</td>
            <td>${produto.estoque}</td>
            <td>R$ ${produto.preco_custo}</td>
            <td>R$ ${produto.preco}</td>
            <td>${produto.estoque <= 5 ? "Baixo" : "OK"}</td>
            <td>
                <button class="btn btn-sm btn-warning">Editar</button>
                <button class="btn btn-sm btn-danger">Excluir</button>
            </td>
        `;

        tr.querySelector(".btn-warning").onclick = () => editarProduto(produto);
        tr.querySelector(".btn-danger").onclick = () => deletarProduto(produto.id);

        container.appendChild(tr);
    });
}

// ================= CRUD =================
async function criarProduto(produto){
    try{
        await safeFetch(API_PRODUTOS, {
            method: "POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(produto)
        });

        mostrarToast("Produto criado");
        carregarProdutos();

    } catch(error){
        mostrarToast(error.message, "error");
    }
}

async function atualizarProduto(id, produto){
    try{
        await safeFetch(`${API_PRODUTOS}${id}/`, {
            method: "PUT",
            headers:{
                "Content-Type":"application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(produto)
        });

        mostrarToast("Produto atualizado");
        carregarProdutos();

    } catch(error){
        mostrarToast(error.message, "error");
    }
}

async function deletarProduto(id){
    if(!confirm("Deseja excluir?")) return;

    try{
        await safeFetch(`${API_PRODUTOS}${id}/`, {
            method: "DELETE",
            headers:{
                "Authorization": `Bearer ${getToken()}`
            }
        });

        mostrarToast("Produto removido");
        carregarProdutos();

    } catch(error){
        mostrarToast(error.message, "error");
    }
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", ()=>{
    verificarLogin();

    if(document.querySelector("#tabela-produtos")){
        carregarProdutos();
    }
});