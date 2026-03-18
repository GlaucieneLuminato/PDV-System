const API_URL = "http://127.0.0.1:8000/api/produtos/";

async function carregarProdutos(){
    try{
        const resposta = await fetch(API_URL);
        const produtos = await resposta.json();

        const tabela = document.querySelector("#productModal");
        tabela.innerHTML = "";

        produtos.forEach(produto =>{

            const card = `
            <div class="product-card">
            <div class="product-image">
            <i class="bi bi-box"></i>
            </div>

            <span class="product-category">
                        Produto
            </span>

            <h5 class="product-title">
                    ${produto.nome}
            </h5>

            <p class="product-sku">
                    ID:${produto.id}
            </p>

            <div class="product-details">

            <span class="product-price">
                    R$ ${produto.preco}
            </span>

            <div class="product-stock">
            <span class="stock-indicator stock-high"></span>
                    ${produto.estoque} em estoque
            </div>
            </div>
            </div>
            `;

            container.innerHTML += card;
        });

    }catch(error){

        console.error("Erro ao carregar produto:", error);
    }}

    carregarProdutos();

