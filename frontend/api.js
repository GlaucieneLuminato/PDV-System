const API_URL = "http://127.0.0.1:8000/api/produtos/"
function getToken(){
    return localStorage.getItem("access");
}

let produtoEditandoId = null
let listaProdutos = [];




function mostrarToast(mensagem, tipo = "success"){
    Toastify({
        text: mensagem,
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: tipo === "success" ? "#28a745" : "#dc3545",
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

    container.innerHTML = "";

    produtos.forEach(produto => {

        let statusEstoque = "";
        if(produto.estoque <= 5){
            statusEstoque = `
            <span class="badge-stock badge-lowstock">
                <i class="bi bi-exclamation-triangle-fill me-1"></i>baixo
            </span>`;
        } else {
            statusEstoque = `
            <span class="badge-stock">
                <i class="bi bi-check-circle-fill text-success me-1"></i>ok
            </span>`;
        }

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
    const confirmar = confirm("Tem certeza que deseja excluir?");

    if(!confirmar) return;

    try{
        const resposta = await fetch(`${API_URL}${id}/`, {
            method: "DELETE",
            headers:{
                "Authorization": `Bearer ${getToken()}`
            }
        });

        if(!resposta.ok){
            console.error("Erro ao deletar");
            return;
        }

        console.log("Produto deletado");
        mostrarToast("Produto deletado com sucesso");

        carregarProdutos();

    } catch(error){
        console.error("Erro:", error);
    }
}


function abrirModalProduto(){
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    modal.show();
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

        if(!resposta.ok){
            console.error("ERRO DO DJANGO:", data);
            return;
        }

        console.log("Produto criado:", data);
        mostrarToast("Produto criado com sucesso");

        
        carregarProdutos();

        document.getElementById("nome").value = "";
        document.getElementById("preco_custo").value = "";
        document.getElementById("preco_venda").value = "";
        document.getElementById("estoque").value = "";
        document.getElementById("sku").value = "";
        document.getElementById("categoria").value = "";

       
        const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
        modal.hide();

    } catch(error){
        console.error("Erro:", error)
    }
}

function salvarProduto(){
    console.log("CLIQUEI EM SALVAR");

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
        atualizarProduto(produtoEditandoId,produto);
    }else{
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

        if(!resposta.ok){
            console.error("Erro ao atualizar:", data);
            return;
        }

        console.log("Produto atualizado:", data);
          mostrarToast("Produto atualizado com sucesso");

        produtoEditandoId = null;

        carregarProdutos();

        
        document.getElementById("nome").value = "";
        document.getElementById("preco_custo").value = "";
        document.getElementById("preco_venda").value = "";
        document.getElementById("estoque").value = "";
        document.getElementById("sku").value = "";
        document.getElementById("categoria").value = "";

        const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
        modal.hide();

    } catch(error){
        console.error("Erro:", error);
    }
}

async function carregarProdutos(){
    try{
        const container = document.querySelector("#tabela-produtos");

        if(!container){
            console.warn("Elemento tabela-produtos não encontrado!");
            return;
        }

        const resposta = await fetch(API_URL,{
            headers:{
                "Authorization": `Bearer ${getToken()}`
            }
        });
        listaProdutos = await resposta.json();

        listaProdutos = listaProdutos;
        renderizarProdutos(listaProdutos);

    } catch(error){
        console.error("Erro ao carregar produto:", error);
    }
    
            let statusEstoque = "";
            if(produto.estoque <= 5){
                statusEstoque = `
                <span class="badge-stock badge-lowstock">
                    <i class="bi bi-exclamation-triangle-fill me-1"></i>baixo
                </span>`;
            } else {
                statusEstoque = `
                <span class="badge-stock">
                    <i class="bi bi-check-circle-fill text-success me-1"></i>ok
                </span>`;
            }

            const linha =  `
            <tr>
            <td>
            <div class="d-flex align-items-center gap-3">
            <div class="product-img">
            <i class="bi bi-box"></i>
            </div>

            <div>
            <span class="fw-semibold">
                ${produto.nome}
            </span>

            <span class="text-secondary small">
                ${produto.sku || "SEM-SKU"}
            </span>
            </div>
            </div>
            </td>

            <td>
            <span class="badge-stock">
                ${produto.sku || "-"}
            </span>
            </td>

            <td>
                ${produto.categoria || "-"}
            </td>

            <td>
            <div class="stock-indicator">
            <span class="fw-semibold">
                    ${produto.estoque} un
            </span>

            <div class="stock-bar">
            <div class="stock-fill"
                 style="width:50%">
            </div>
            </div>
            </div>
            </td>

            <td> R$ ${produto.preco_custo}</td>
            <td> R$ ${produto.preco_venda || "-"}</td>

            <td>
                ${statusEstoque}
            </td>

            <td class="action-icons">
            <i class="bi bi-eye"></i>
            <i class="bi bi-pencil" style="cursor:pointer"
   onclick='editarProduto(${JSON.stringify(produto)})'></i>
            <i class="bi bi-trash" style="cursor:pointer; color:red;"
   onclick="deletarProduto(${produto.id})"></i>
            </td>
            </tr>
            `;

            container.innerHTML += linha;
        };

    


document.getElementById("busca").addEventListener("input", function(){
    const valor = this.value.toLowerCase();

    const filtrados = listaProdutos.filter(produto =>
        produto.nome.toLowerCase().includes(valor) ||
        produto.categoria.toLowerCase().includes(valor) ||
        produto.sku.toLowerCase().includes(valor)
    );

    renderizarProdutos(filtrados);
});

document.addEventListener("DOMContentLoaded", ()=>{
    carregarProdutos();
});

window.deletarProduto = deletarProduto;
window.editarProduto = editarProduto;