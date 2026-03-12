const API_URL = "http://127.0.0.1:8000/api/produtos/";

let carrinho = [];

async function carregarProdutos(){
    try{
        const resposta = await fetch(API_URL);
        const produtos = await resposta.json();
        console.log(produtos);
        console.log("API conectada BABY!!");

        const tabela = document.querySelector("#tabela-produtos");
        tabela.innerHTML = "";

        produtos.forEach(produto => {
            const linha = `
            <tr>
                <td>${produto.nome}</td>
                <td>${produto.id}</td>
                <td>-</td>
                <td>${produto.estoque}</td>
                <td>-</td>
                <td>R$ ${produto.preco}</td>
                <td>ativo</td>
                <td>
                <button onClick="adicionarCarrinho(${produto.id})" style="border:none;background:none">
                <i class="bi bi-cart-plus"></i>
                </button>
                </td>
            </tr>
            `;
            tabela.innerHTML  += linha
        });
    } catch(erro){
        console.error("Erro ao carregar produto:", erro);
    }
}

function adicionarCarrinho(id){
    carrinho.push(id);
    console.log("Carrinho:",carrinho);
}

carregarProdutos();

