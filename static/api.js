const API_BASE = "https://pdv-system-c359.onrender.com";

const API_PRODUTOS = API_BASE + "/api/produtos/";


const API_VENDAS = API_BASE + "/api/vendas/";
const API_USERS = API_BASE + "/api/users/";

// 👇 ESSAS DUAS LINHAS FALTAM
const API_LOGIN = API_BASE + "/api/token/";
const API_REFRESH = API_BASE + "/api/token/refresh/";
function getToken(){
    return localStorage.getItem("access");
}

function verificarLogin(){
    const token = getToken();

    if(!token){
        alert("Você precisa estar logado");
        window.location.href = "login.html";
        return;
    }
}

let produtoEditandoId = null;
let listaProdutos = [];

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

// ================= VENDAS =================
async function enviarVenda(venda){
    try{
        const resposta = await fetch(API_VENDAS,{
            method:"POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(venda)
        });

        const data = await resposta.json(); 

        if(!resposta.ok){
            console.error("Erro ao salvar venda:", data);
            return;
        }

        mostrarToast("Venda registrada!");

    } catch(error){
        console.error("Erro:", error)
    }
}

// ================= PRODUTOS =================
function editarProduto(produto){
    produtoEditandoId = produto.id;

    document.getElementById("nome").value = produto.nome;
    document.getElementById("preco_custo").value = produto.preco_custo;
    document.getElementById("preco_venda").value = produto.preco || produto.preco_venda;
    document.getElementById("estoque").value = produto.estoque;
    document.getElementById("sku").value = produto.sku;
    document.getElementById("categoria").value = produto.categoria;

    abrirModalProduto();
}

function renderizarProdutos(produtos){
    const container = document.querySelector("#tabela-produtos");

    if(!container){
        console.warn("Tabela de produtos não existe nessa página");
        return;
    }

    container.innerHTML = "";

    produtos.forEach(produto => {

        let statusEstoque = produto.estoque <= 5
            ? `<span class="badge-stock badge-lowstock">baixo</span>`
            : `<span class="badge-stock">ok</span>`;

        const linha = `
        <tr>
            <td>${produto.nome}</td>
            <td>${produto.sku}</td>
            <td>${produto.categoria}</td>
            <td>${produto.estoque}</td>
            <td>R$ ${produto.preco_custo}</td>
            <td>R$ ${produto.preco}</td>
            <td>${statusEstoque}</td>
            <td>
                <i class="bi bi-pencil" onclick='editarProduto(${JSON.stringify(produto)})'></i>
                <i class="bi bi-trash" onclick="deletarProduto('${produto.id}')"></i>
            </td>
        </tr>
        `;

        container.innerHTML += linha;
    });
}

async function carregarProdutos(){
    try{
        const resposta = await fetch(API_PRODUTOS,{
            method: "GET",
            headers:{
                "Authorization": `Bearer ${getToken()}`
            }
        });

        if(resposta.status === 401){
            alert("Sessão expirada");
            localStorage.removeItem("access");
            window.location.href = "login.html";
            return;
        }

        if(!resposta.ok){
            console.error("Erro ao buscar produtos");
            return;
        }

        listaProdutos = await resposta.json();
        console.log("PRODUTOS:", listaProdutos);

        renderizarProdutos(listaProdutos);

    } catch(error){
        console.error("Erro ao carregar produto:", error);
    }
}

async function criarProduto(produto){
    try{
        const resposta = await fetch(API_PRODUTOS, {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body:JSON.stringify(produto)
        });

        const data = await resposta.json();

        if(resposta.status === 401){
            alert("Sessão expirada");
            localStorage.removeItem("access");
            window.location.href = "login.html";
            return;
        }

        if(!resposta.ok){
            console.error("ERRO DO DJANGO:", data);
            return;
        }

        mostrarToast("Produto criado com sucesso");
        carregarProdutos();
        limparFormulario();

    } catch(error){
        console.error("Erro:", error)
    }
}

async function atualizarProduto(id, produto){
    try{
        const resposta = await fetch(`${API_PRODUTOS}${id}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(produto)
        });

        const data = await resposta.json();

        if(resposta.status === 401){
            alert("Sessão expirada");
            localStorage.removeItem("access");
            window.location.href = "login.html";
            return;
        }

        if(!resposta.ok){
            console.error("Erro ao atualizar:", data);
            return;
        }

        mostrarToast("Produto atualizado com sucesso");

        produtoEditandoId = null;
        carregarProdutos();
        limparFormulario();

    } catch(error){
        console.error("Erro:", error);
    }
}

async function deletarProduto(id){
    if(!confirm("Tem certeza que deseja excluir?")) return;

    try{
        const resposta = await fetch(`${API_PRODUTOS}${id}/`, {
            method: "DELETE",
            headers:{
                "Authorization": `Bearer ${getToken()}`
            }
        });

        if(resposta.status === 401){
            alert("Sessão expirada");
            localStorage.removeItem("access");
            window.location.href = "login.html";
            return;
        }

        if(!resposta.ok){
            console.error("Erro ao deletar");
            return;
        }

        mostrarToast("Produto deletado com sucesso");
        carregarProdutos();

    } catch(error){
        console.error("Erro:", error);
    }
}

function salvarProduto(){
    const produto = {
        nome: document.getElementById("nome").value,
        preco: parseFloat(document.getElementById("preco_venda").value) || 0,
        preco_custo: parseFloat(document.getElementById("preco_custo").value) || 0,
        estoque: parseInt(document.getElementById("estoque").value) || 0,
        sku: document.getElementById("sku").value || "SEM-SKU",
        categoria: document.getElementById("categoria").value || "Outros",
    };

    if(produtoEditandoId){
        atualizarProduto(produtoEditandoId, produto);
    } else {
        criarProduto(produto);
    }
}

function limparFormulario(){
    document.getElementById("nome").value = "";
    document.getElementById("preco_custo").value = "";
    document.getElementById("preco_venda").value = "";
    document.getElementById("estoque").value = "";
    document.getElementById("sku").value = "";
    document.getElementById("categoria").value = "";

    const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
    modal.hide();
}

// ================= BUSCA =================
const busca = document.getElementById("busca");

if(busca){
    busca.addEventListener("input", function(){
        const valor = this.value.toLowerCase();

        const filtrados = listaProdutos.filter(produto =>
            produto.nome.toLowerCase().includes(valor) ||
            produto.categoria.toLowerCase().includes(valor) ||
            produto.sku.toLowerCase().includes(valor)
        );

        renderizarProdutos(filtrados);
    });
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", ()=>{
    verificarLogin();

    if(document.querySelector("#tabela-produtos")){
        carregarProdutos();
    }
});

// ================= GLOBAL =================
window.deletarProduto = deletarProduto;
window.editarProduto = editarProduto;