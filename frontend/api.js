const API_URL = "http://127.0.0.1:8000/api/produtos/"

async function carregarProdutos(){
    try{
        const container = document.querySelector("#gridView");

        if(!container){
            console.error("Elemento #gridView não encontrado!");
            return;
        }
        const resposta = await fetch(API_URL);
        const produtos = await resposta.json();

        container.innerHTML = "";

        produtos.forEach(produtos => {
            const card = `
            <div class="product-card">
            <h5>${produtos.nome}</h5>
            <p>Preço: £ ${produtos.preco}</p>
            <p>Estoque: ${produtos.estoque}</p>
            </div>
            `;
            container.innerHTML += card;
        });
    } catch(error){
        console.error("Erro ao carregar produto:", error);
    }
}

window.onload = carregarProdutos;