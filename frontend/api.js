const API_URL = "https://127.0.0.1:8000/api/produtos/";

async function carregarProdutos(){
    try{
        const resposta = await fetch(API_URL);
        const produtos = await resposta.json();

        const tabela = document.querySelector("tbody");
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
                <td></td>
            </tr>
            `;
            tabela.innerHTML  += linha
        });
    } catch(erro){
        console.erro("Erro ao carregar produto:", erro);
    }
}

carregarProdutos();