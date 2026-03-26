const API_URL = "https://pdv-system-c359.onrender.com";
const API_BASE = "https://pdv-system-c359.onrender.com";
const API_PRODUTOS = API_BASE + "produtos/";
const API_VENDAS = API_BASE + "vendas/";
const API_USERS = API_BASE + "users/";
const API_LOGIN = API_BASE + "login/";



async function enviarVenda(venda){
    try{
        const resposta = await fetch(API_VENDAS,{
            method:"POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access")}`
            },
            body: JSON.stringify(venda)
        });

        const data = await resposta.json(); 

        console.log("RESPOSTA DO DJANGO:", data);

        if(!resposta.ok){
            console.error("Erro ao salvar venda:", data);
            return;
        }

        console.log("Venda salva com sucesso:", data);
        mostrarToast("Venda registrada!");

    } catch(error){
        console.error("Erro:", error)
    }
}
function verificarLogin(){
    const token = localStorage.getItem("access");

    if(!token){
        alert("Você precisa estar logado");
        window.location.href = "login.html";
        return;
    }
}

function getToken(){
    return localStorage.getItem("access");
}

let produtoEditandoId = null;
let listaProdutos = [];


function mostrarToast(mensagem, tipo = "success"){
    Toastify({
        text: mensagem,
        duration: 3000,
        gravity: "top",
        position: "right",
        background: tipo === "success" ? "#28a745" : "#dc3545",
    }).showToast();
}


function editarProduto(produto){
    produtoEditandoId = produto.id;

    document.getElementById("nome").value = produto.nome;
    document.getElementById("preco_custo").value = produto.preco_custo;
    document.getElementById("preco_venda").value = produto.preco_venda;
    document.getElementById("estoque").value = produto.estoque;
    document.getElementById("sku").value = produto.sku;
    document.getElementById("categoria").value = produto.categoria;

    abrirModalProduto();
}

function renderizarProdutos(produtos){
    const container = document.querySelector("#tabela-produtos");

    if(!container){
        console.warn("Tabela de produtos não existente nessa página")
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
            <td>R$ ${produto.preco_venda}</td>
            <td>${statusEstoque}</td>
            <td>
                <i class="bi bi-pencil" onclick='editarProduto(${JSON.stringify(produto)})'></i>
                <i class="bi bi-trash" onclick="deletarProduto(${produto.id})"></i>
            </td>
        </tr>
        `;

        container.innerHTML += linha;
    });
}


async function deletarProduto(id){
    if(!confirm("Tem certeza que deseja excluir?")) return;

    try{
        const resposta = await fetch(`${API_URL}${id}/`, {
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


function abrirModalProduto(){
    new bootstrap.Modal(document.getElementById('productModal')).show();
}


async function criarProduto(produto){
    try{
        const resposta = await fetch(API_URL, {
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


function salvarProduto(){
    const produto = {
        nome: document.getElementById("nome").value,
        preco: parseFloat(document.getElementById("preco_venda").value) || 0,
        preco_custo: parseFloat(document.getElementById("preco_custo").value) || 0,
        preco_venda: parseFloat(document.getElementById("preco_venda").value) || 0,
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


async function atualizarProduto(id, produto){
    try{
        const resposta = await fetch(`${API_URL}${id}/`, {
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


async function carregarProdutos(){
    try{
        const resposta = await fetch(API_URL,{
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

        listaProdutos = await resposta.json();
        console.log("PRODUTOS CLICADOS:", product);
        renderizarProdutos(listaProdutos);

    } catch(error){
        console.error("Erro ao carregar produto:", error);
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

document.addEventListener("DOMContentLoaded", ()=>{
    verificarLogin();

    if(document.querySelector("#tabela-produtos")){
    carregarProdutos()
}
});

document.addEventListener("DOMContentLoaded", ()=>{
    const hoje = new Date();
    const passado = new Date();

    passado.setDate(hoje.getDate() - 30);

    const formatar = (data) => data.toISOString().split("T")[0];

    document.getElementById("startDate").value = formatar(passado);
    document.getElementById("endDate").value = formatar(hoje);
});


window.deletarProduto = deletarProduto;
window.editarProduto = editarProduto;