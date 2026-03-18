const API_URL = "http://127.0.0.1:8000/api/produtos/"

async function carregarProdutos(){
    try{
        const container = document.querySelector("#tabela-produtos");

        if(!container){
            console.warn("Elemento tabela-produtos não encontrado!");
            return;
        }
        const resposta = await fetch(API_URL);
        const produtos = await resposta.json();

        container.innerHTML = "";

        produtos.forEach(produto => {
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
            <span class="badge-stock">
            <i class="bi bi-check-circle-fill text-sucess me-1"></i>
                ativo
            </span>
            </td>

            <td class="action-icons">
            <i class="bi bi-eye"></i>
            <i class="bi bi-pencil"></i>
            </td>
            </tr>
            
            `;
            container.innerHTML += linha;
        });
    } catch(error){
        console.error("Erro ao carregar produto:", error);
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    carregarProdutos();
});