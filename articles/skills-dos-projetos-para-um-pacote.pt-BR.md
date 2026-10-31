---
title: "As skills dos meus projetos estão virando um pacote para Codex e Claude"
language: pt-BR
status: draft
---

Recebi uma pergunta sobre quais skills uso com o Codex para desenvolver código, criar automações e trabalhar com agentes em análises mais complexas. Fui fazer o inventário. Uma parte estava nas skills globais. Outra estava dentro dos projetos, nos hooks do Git e no código do Ralph Starter.

Daí veio a ideia de organizar uma coleção pública, que também funcione com Claude Code, e explicar o método por trás de cada skill.

O [Addy Osmani](https://github.com/addyosmani/agent-skills) e o [Matt Pocock](https://github.com/mattpocock/skills) já mantêm coleções nesse formato. Gostei da distribuição: pastas pequenas, instruções legíveis e um propósito que dá para entender antes de instalar.

Minha primeira versão reúne 11 workflows. O pacote está em preparação local, com publicação e avaliação nos dois agentes ainda pendentes.

## Comecei pelos modos de falha

Uma skill útil precisa mudar uma decisão durante o trabalho. Para selecionar as minhas, usei os problemas que cada workflow tenta evitar.

Em debugging, o agente pode corrigir um módulo parecido e deixar intacto o caminho que o usuário reportou. Em review, pode repetir a justificativa de quem escreveu o código. Em um loop de implementação, pode confundir uma sequência de tentativas com progresso.

Isso virou instruções concretas:

- `evidence-driven-debugging`: reproduzir o cenário e seguir o caminho entre interface, request, resposta e renderização.
- `critical-adversarial-review`: revisar uma revisão específica e sustentar cada finding com localização, gatilho e impacto.
- `gauntlet-loop`: estabelecer baseline, implementar, criticar, procurar regressões e registrar a decisão de cada rodada.
- `quality-gates`: verificar se a régua realmente mede o comportamento esperado.

Gosto especialmente da última. Um gate de regressão ganha credibilidade quando você aplica uma mudança deliberadamente quebrada e observa o teste falhar pelo motivo esperado. Se a mudança nem chegou a ser aplicada, o experimento ficou inconclusivo. Se faltou uma medição, o resultado continua desconhecido.

São detalhes pequenos. Eles mudam o significado de um check verde.

## Review crítico precisa de liberdade para discordar

No review adversarial, o revisor recebe o artefato, o contrato e o contexto necessário para avaliar a mudança. Precisa formar o próprio julgamento sobre o resultado.

A saída que me interessa tem uma forma simples: onde está o problema, qual entrada o dispara, o que deveria acontecer, o que acontece e como verificar. Uma reprodução ainda não executada fica identificada como hipótese.

Também tirei qualquer incentivo para preencher uma cota de findings. Pedir dez bugs em uma alteração pequena só cria pressão para inventar defeitos. O revisor pode terminar sem um problema comprovado e explicar quais verificações ficaram pendentes.

## Research inclui saber o que um post permite concluir

Uso bastante pesquisa em redes sociais para encontrar relatos, exemplos e problemas que a documentação deixa de fora. Isso entrou em `source-backed-research` junto com a pesquisa técnica.

Cada fonte precisa carregar o que ela sustenta. Um post pode documentar a experiência de uma pessoa. Curtidas medem uma forma de interação com aquele conteúdo. Uma amostra escolhida manualmente precisa ter o critério de seleção registrado.

Para comparar ferramentas, combino esse material com documentação e código quando estão disponíveis. Registro data, versão e a diferença entre observação, relato da fonte e inferência minha. Dá trabalho, mas permite voltar a uma conclusão quando o produto muda.

## O que extraí do Ralph Starter

O [Ralph Starter](https://github.com/rubenmarcus/ralph-starter) já tem skills próprias, várias ligadas às integrações do produto. Nesta coleção, extraí três métodos do executor e da coordenação:

| Skill | Decisão que organiza |
| --- | --- |
| `spec-to-plan` | Qual comportamento observável define que a tarefa terminou? |
| `validated-coding-loop` | Qual evidência orienta a próxima tentativa e quando o loop deve parar? |
| `agent-worktree-orchestration` | Quem pode escrever onde e como comparar os candidatos? |

A inspeção encontrou um exemplo bom da diferença entre intenção e implementação. No [`swarm.ts` da revisão analisada](https://github.com/rubenmarcus/ralph-starter/blob/ee9c7946c386bb9cecc4001a052e29ffa53f8f9a/src/loop/swarm.ts), o comentário descreve um juiz LLM para o modo `consensus`. O código seleciona entre os resultados bem-sucedidos pelo número de iterações.

Por isso a skill pede uma régua explícita de aceitação. Menos iterações pode ser uma informação de custo; a correção precisa da própria evidência.

A skill de colaboração veio de outro contexto, meu trabalho com ECDSA. Generalizei os handoffs, a reprodução independente e a resolução de hipóteses conflitantes. Os detalhes de circuitos e métricas daquele domínio ficaram no projeto original.

## AEO com aeo.js também entrou

A skill `aeo` usa o [aeo.js](https://github.com/rubenmarcus/aeo.js) para auditar e implementar as superfícies públicas de descoberta de um site: política de crawlers, URLs canônicas, sitemap, conteúdo legível por máquinas e dados estruturados.

Ela começa pela configuração existente. Se outra integração já gera `robots.txt` e sitemap, precisamos preservar esse dono e desabilitar os geradores sobrepostos. A política de acesso também precisa continuar refletindo a intenção do projeto.

Na validação, arquivo gerado e resposta servida são etapas distintas. Um `schema.json` no build pede uma verificação adicional de como os dados chegam à página. O score do auditor descreve os critérios da ferramenta; citações em respostas e ganhos de tráfego precisam de observações próprias.

Até a versão merece inspeção. Na revisão usada como referência, o `package.json` diz `0.0.17`, enquanto a constante exibida pelo CLI diz `0.0.14`. Registrei o commit junto dos comandos para deixar a referência reproduzível.

## Uma coleção pequena dá para revisar

Também incluí hooks de qualidade para o Git, com um exemplo de scanner de secrets no conteúdo staged. Instalar a skill mantém o exemplo inativo; configurar um hook é uma tarefa explícita, que precisa preservar o workflow existente.

O pacote compartilha os mesmos arquivos `SKILL.md` entre os agentes e separa os metadados de distribuição. Os checks estruturais verificam referências e manifests. Os cenários de avaliação registram o que ainda precisa ser exercitado com Codex e Claude.

Para começar, escolha um problema recorrente do seu projeto. Escreva a evidência que faria você aceitar a solução e rode a skill em uma tarefa pequena. Guarde o resultado, inclusive quando o agente ignorar uma instrução. É esse material que vai orientar a próxima versão.
