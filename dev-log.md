📅 DEV LOG — HOJE  18/03/2026

✅ O que foi feito

🔌 Integração Frontend + Backend

- API do Django conectada corretamente ao frontend
- Endpoint funcionando: "/api/produtos/"
- Dados sendo consumidos via "fetch()"

---

🧠 Correções importantes

1. ❌ Erro de HTTPS

- Problema: "ERR_SSL_PROTOCOL_ERROR"
- Solução: trocar "https://" por "http://"

---

2. ❌ Erro de digitação

- "console.erro" → corrigido para "console.error"

---

3. ❌ Elemento não encontrado ("gridView")

- Causa: HTML diferente do esperado
- Solução: identificar que o layout mudou para tabela

---

4. 🔄 Mudança de layout (GRID → TABELA)

- Antes: "#gridView"
- Agora: "#tabela-produtos"
- Renderização alterada de "<div>" para "<tr>"

---

5. ❌ Problema de múltiplos arquivos

- Existiam dois "produtos.html" e dois "api.js"
- Correção:
  - removidos arquivos duplicados do backend
  - mantido apenas o frontend correto

---

6. 🧠 Bug silencioso (dados não apareciam)

- Causa: JS apontando para ID errado
- Correção: alinhamento com "#tabela-produtos"

---

7. 🚨 Cache do navegador (CRÍTICO)

- Problema: alterações não apareciam
- Causa: status "304 Not Modified"
- Solução:
  - "Ctrl + Shift + R"
  - versionamento de script ("?v=2")

---

📊 Testes realizados

- ✔ API retornando dados corretamente
- ✔ Produtos sendo exibidos na tabela
- ✔ Novo produto (iPhone) aparecendo após atualização
- ✔ Integração confirmada funcionando

---

💾 Ajustes de dados

- Produtos antigos estavam com:
  - "preco_custo = 0"
  - "preco_venda = 0"
- Correção manual via Django Admin

---

🚀 STATUS ATUAL

✅ Sistema funcionando
✅ Integração OK
✅ Renderização OK
⚠️ Ajustes visuais pendentes

---

📅 PLANO — AMANHÃ  19/03/2026

🎯 1. Implementar lógica de estoque dinâmico

Regra:

- estoque ≤ 2 → 🔴 crítico
- estoque ≤ 5 → 🟡 baixo
- estoque > 5 → 🟢 normal

---

🧠 Implementação (no JS)

Criar lógica dentro do "forEach":

let statusHTML = "";
let barraClasse = "";
let porcentagem = 0;

if (produto.estoque <= 2) {
    statusHTML = `<span class="badge-stock badge-lowstock">
        <i class="bi bi-exclamation-triangle-fill me-1"></i>crítico
    </span>`;
    barraClasse = "critical";
    porcentagem = 15;

} else if (produto.estoque <= 5) {
    statusHTML = `<span class="badge-stock badge-lowstock">
        <i class="bi bi-exclamation-triangle-fill me-1"></i>baixo
    </span>`;
    barraClasse = "warning";
    porcentagem = 40;

} else {
    statusHTML = `<span class="badge-stock">
        <i class="bi bi-check-circle-fill text-success me-1"></i>ativo
    </span>`;
    barraClasse = "";
    porcentagem = 80;
}

---

🎨 Aplicar no HTML

Substituir:

<td>${statusHTML}</td>

e:

<div class="stock-fill ${barraClasse}" style="width: ${porcentagem}%"></div>

---

🧪 Testes amanhã

- Criar produto com estoque:
  - 1 → deve aparecer crítico 🔴
  - 3 → deve aparecer baixo 🟡
  - 10 → deve aparecer normal 🟢

---

💡 Melhorias futuras (opcional)

- puxar "estoque_minimo" do backend
- calcular automaticamente o status
- formatar moeda (R$ 1.499,00)
- botão de atualização manual
- atualização automática com "setInterval"

---

🧠 OBSERVAÇÃO IMPORTANTE

Hoje foi resolvido um problema de:

✔ cache
✔ duplicidade de arquivos
✔ integração
✔ renderização

👉 Isso é experiência real de desenvolvimento.

---

✨ PRÓXIMO PASSO

Continuar evolução visual + lógica de negócio no frontend.