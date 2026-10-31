# Skills do Ruben para agentes

[English](README.md)

11 workflows para Codex e Claude Code, extraídos dos meus projetos e reescritos como instruções reutilizáveis. Debugging, review adversarial, loops de melhoria, pesquisa com fontes, colaboração, hooks Git e AEO.

**Versão 0.1.0, licença MIT.** Os checks de estrutura e um [piloto pequeno com pares de tarefas](evals/pilot/REPORT.md) estão registrados. A avaliação comportamental completa com os dois agentes continua pendente. A distribuição é por Git e metadados de plugin; não há release no npm.

## Escolha pelo problema

Dois pontos de partida vêm direto dos meus projetos: [AEO](skills/aeo/SKILL.md), para integrar aeo.js e verificar a descoberta nas respostas servidas, e [Gauntlet](skills/gauntlet-loop/SKILL.md), para rodadas de melhoria com medidas, como iluminação de mapas. Os outros workflows organizam os checks, a pesquisa e a implementação dessas tarefas.

| Skill | Quando usar |
| --- | --- |
| [critical-adversarial-review](skills/critical-adversarial-review/SKILL.md) | Revisar uma mudança específica e buscar falhas com localização, gatilho e evidência. |
| [gauntlet-loop](skills/gauntlet-loop/SKILL.md) | Repetir construção, crítica e busca de regressões com uma régua explícita. |
| [evidence-driven-debugging](skills/evidence-driven-debugging/SKILL.md) | Seguir o caminho real do erro reportado pelo usuário até sua causa. |
| [quality-gates](skills/quality-gates/SKILL.md) | Verificar se um gate mede o comportamento certo e rejeita uma alteração quebrada. |
| [source-backed-research](skills/source-backed-research/SKILL.md) | Pesquisar documentação, código e redes sociais com fontes e incertezas registradas. |
| [multi-agent-collaboration](skills/multi-agent-collaboration/SKILL.md) | Coordenar handoffs reproduzíveis, responsabilidades e conclusões conflitantes. |
| [spec-to-plan](skills/spec-to-plan/SKILL.md) | Transformar uma tarefa em critérios observáveis e etapas de implementação. |
| [validated-coding-loop](skills/validated-coding-loop/SKILL.md) | Iterar usando diagnósticos reais, checkpoints e condição de parada. |
| [agent-worktree-orchestration](skills/agent-worktree-orchestration/SKILL.md) | Isolar alterações e comparar candidatos segundo critérios de aceite. |
| [git-quality-hooks](skills/git-quality-hooks/SKILL.md) | Configurar checks Git e scanner de secrets sobre o conteúdo staged. |
| [aeo](skills/aeo/SKILL.md) | Auditar e implementar descoberta de conteúdo com aeo.js, respeitando a política de crawlers existente. |

Comece pela skill da tarefa atual. Os workflows de colaboração se aplicam quando o trabalho paralelo foi solicitado ou autorizado.

Os [exemplos de uso](#exemplos-de-uso) trazem cenário, prompt e resultado esperado para cada uma das 11 skills.

## Coleções complementares

As [skills do Matt Pocock](https://github.com/mattpocock/skills) e o [agent-skills do Addy Osmani](https://github.com/addyosmani/agent-skills) cobrem várias das mesmas decisões. Review independente, controles negativos e coordenação de agentes também aparecem nos workflows deles. Mantenho esta coleção como a seleção dos meus projetos; escolha as instruções que combinam com a tarefa e o setup que você já usa.

| Tarefa | Outro workflow para ler |
| --- | --- |
| Reproduzir um bug antes de alterar código | [diagnosing-bugs do Matt](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/diagnosing-bugs/SKILL.md) |
| Revisar um artefato contra o contrato | [doubt-driven-development do Addy](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/doubt-driven-development/SKILL.md) |
| Definir restrições mensuráveis e controles quebrados | [constraint-driven-development do Addy](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/constraint-driven-development/SKILL.md) |
| Configurar checks do repositório antes dos commits | [setup-pre-commit do Matt](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/misc/setup-pre-commit/SKILL.md) |

Os links fixam as revisões inspecionadas. O conteúdo continua nos repositórios de origem. Esta coleção não tem uma comparação de eficácia contra essas suites.

## Instalação

```sh
git clone https://github.com/rubenmarcus/agent-skills.git
cd agent-skills
```

Leia a skill e suas referências antes de habilitá-la. O pacote não executa instaladores automaticamente. O exemplo de hook Git fica inativo até você configurá-lo.

### Codex

Para experimentar uma skill em um projeto existente, copie a pasta escolhida para `.agents/skills/`, a partir da raiz desta coleção:

```sh
target_project=/caminho/absoluto/do/seu-projeto
mkdir -p "$target_project/.agents/skills"
test ! -e "$target_project/.agents/skills/critical-adversarial-review" &&
  cp -R skills/critical-adversarial-review "$target_project/.agents/skills/"
```

Preserve qualquer pasta já instalada. Inicie ou atualize a sessão conforme o cliente e invoque `$critical-adversarial-review` com a revisão e o escopo reais. A [documentação do Codex](https://learn.chatgpt.com/docs/build-skills) descreve a descoberta de skills por projeto. O `plugin.json` fornece metadados para hosts compatíveis; a coleção não foi listada no diretório de plugins da OpenAI.

### Claude Code

Para carregar o checkout em uma sessão:

```sh
claude --plugin-dir /caminho/absoluto/para/agent-skills
```

Ou instale pelo marketplace dentro de uma sessão do Claude:

```text
/plugin marketplace add rubenmarcus/agent-skills
/plugin install rubenmarcus-skills@rubenmarcus
```

Escolha o escopo no cliente. Confira a [documentação do Claude Code](https://code.claude.com/docs/en/discover-plugins) para permissões e escopos disponíveis.

Os mesmos arquivos `SKILL.md` atendem aos dois agentes. Ferramentas, permissões e instruções de projeto continuam vindo do ambiente. A coleção não instala aeo.js nem inicia agentes em segundo plano.

## Exemplos de uso

Cada exemplo traz uma situação, um prompt inicial e o artefato esperado. Troque revisões, rotas, versões, fixtures e limites pelos dados do seu projeto. Os prompts são tarefas para experimentar; os [cenários de avaliação](evals/scenarios.json) registram os checks comportamentais ainda pendentes.

### critical-adversarial-review

Use antes do merge de uma mudança de API, quando precisa de um olhar independente sobre paginação e callers.

```text
Use critical-adversarial-review para revisar BASE..HEAD.
O endpoint deve preservar a paginação quando o filtro muda.
Leia o diff e os callers, sem alterar arquivos.
Informe localização, entrada que dispara a falha, resultado esperado,
resultado observado e reprodução mínima. Identifique hipóteses ainda
não executadas. Aceito zero findings.
```

Resultado esperado: findings com evidência na revisão analisada e limites do que foi verificado.

### gauntlet-loop

Use quando melhorar a iluminação de um mapa do jogo exige várias rodadas de captura, crítica e busca de regressões.

```text
Use gauntlet-loop para melhorar a iluminação deste mapa segundo os
critérios visuais fornecidos. Mantenha o percurso da câmera, viewport e
configuração de captura. Registre o baseline, compare cada candidato com
uma crítica independente e confira as outras cenas de referência.
Respeite o limite de rodadas combinado.
```

Resultado esperado: registro de cada rodada com capturas do baseline e do candidato, regressões e decisão de manter, revisar ou rejeitar. A aprovação visual humana continua explícita.

### evidence-driven-debugging

Use quando o contador de participantes de um dashboard diverge dos registros que deveriam alimentar a tela.

```text
Use evidence-driven-debugging no contador de participantes ativos desta
tela. Siga o valor exibido pelo request, query, registros e renderização.
Confira participantes distintos, contagem de eventos e respostas antigas.
Reproduza a divergência, corrija a causa e execute o mesmo caminho de novo.
```

Resultado esperado: falha reproduzida, causa identificada e evidência de antes e depois na mesma interface e no mesmo caminho dos dados.

### quality-gates

Use quando o CI passa enquanto uma regressão no checkout continua visível.

```text
Use quality-gates para avaliar o gate de regressão do checkout.
Numa cópia descartável, aplique uma alteração deliberadamente quebrada
e confira se o gate reprova pelo motivo esperado. Restaure a cópia depois.
Confirme que a alteração foi aplicada. Exercite também uma medição ausente.
```

Resultado esperado: resultados do baseline válido, do defeito deliberado e da evidência indisponível, com o comportamento medido e os comandos de reprodução.

### source-backed-research

Use antes de escolher uma biblioteca cujo comportamento de retry pode duplicar uma escrita.

```text
Use source-backed-research para comparar os retries destas duas bibliotecas
nas versões fornecidas. Confira documentação oficial e código sobre retries
de escrita e idempotência. Registre URLs, datas, relatos das fontes e
inferências no ledger de evidência. Aponte as perguntas ainda sem resposta.
```

Resultado esperado: comparação com versões e fontes, as premissas da recomendação e a próxima verificação que pode mudar a escolha.

### multi-agent-collaboration

Use quando dois agentes já investigam uma falha intermitente e discordam sobre a causa ser cache ou retries.

```text
Use multi-agent-collaboration para conciliar estas duas investigações.
Mantenha os limites de responsabilidade atuais. Peça a cada agente um
handoff com revisão, configuração, entrada exata, comando, resultado e
caminhos dos artefatos. Escolha o menor experimento que distingue as
duas explicações.
```

Resultado esperado: handoffs reproduzíveis, o experimento que separa as hipóteses e uma conclusão compartilhada com hipóteses rejeitadas e dúvidas restantes.

### spec-to-plan

Use quando uma issue pede "adicionar convites para o time", mas deixa expiração, permissões e aceite repetido em aberto.

```text
Use spec-to-plan nesta issue de convites para o time. Leia os contratos
atuais de autenticação e membros. Identifique decisões sobre expiração,
roles e aceite repetido. Escreva critérios de aceite observáveis e ordene
as etapas de implementação. Aponte decisões de produto que precisam
de resposta.
```

Resultado esperado: plano delimitado com casos de falha, dependências, decisões pendentes e a primeira etapa que pode ser implementada.

### validated-coding-loop

Use quando implementar uma correção acordada para entregas duplicadas de webhook exige várias tentativas de código e validação.

```text
Use validated-coding-loop para implementar a spec aprovada de deduplicação
de webhooks nesta branch. Use os fixtures de entrega e checks fornecidos.
A cada alteração focada, salve o diagnóstico real e um checkpoint.
Cumpra os critérios de aceite dentro do limite combinado. Investigue
falhas repetidas e preserve a próxima ação se a execução parar.
```

Resultado esperado: implementação recuperável, registro das tentativas e evidência de aceite na revisão atual.

### agent-worktree-orchestration

Use quando você autorizou dois candidatos de implementação para uma mudança de cache e quer compará-los sem escritas no mesmo checkout.

```text
Use agent-worktree-orchestration para os dois candidatos de cache
autorizados. Parta do mesmo commit em branches e worktrees separados.
Registre os caminhos permitidos e o limite de cada agente. Compare os
dois com os checks de correção e latência fornecidos. Entregue as duas
revisões e a evidência de seleção a um responsável pela integração.
```

Resultado esperado: mapa de responsabilidades, commits isolados, comparação com as mesmas entradas e handoff de integração verificado.

### git-quality-hooks

Use ao adicionar scanner de secrets no conteúdo staged de um repositório que já usa Husky ou outro gerenciador de hooks.

```text
Use git-quality-hooks para adicionar gitleaks no conteúdo staged deste
repositório. Inspecione core.hooksPath e o gerenciador de hooks existente.
Preserve os checks atuais, oculte os valores nos relatórios e reprove
quando o scanner estiver indisponível. Verifique argumentos e códigos
de saída com fixtures sintéticos isolados.
```

Resultado esperado: hook composto com os checks existentes, instruções de configuração e resultados dos fixtures. O fixture verifica a passagem dos argumentos e erros; a detecção do scanner precisa de evidência própria.

### aeo

Use quando um site Astro tem conteúdo em inglês e português, restrições de crawlers e arquivos de descoberta que precisam apontar para rotas reais.

```text
Use aeo para auditar a descoberta EN/PT deste site com a versão fixada
de aeo.js. Confira quem gera robots e sitemap, URLs canônicas e JSON-LD.
Corrija as lacunas observadas preservando a política de crawlers.
Faça o build e verifique as rotas públicas e os arquivos de descoberta
habilitados no preview autorizado.
```

Resultado esperado: auditoria e evidência das respostas servidas para URLs canônicas, dados estruturados e arquivos de descoberta, com lacunas restantes registradas.

## Validação e limites

Node.js 20+ executa o check estrutural sem dependências npm. Python 3 executa o fixture do hook.

```sh
npm run check
npm run check:hook
claude plugin validate . --strict
npm pack --ignore-scripts --pack-destination /tmp
```

`check` verifica metadados, referências, manifests e cenários. `check:hook` usa um scanner falso para verificar argumentos e propagação dos códigos de saída; ele não mede a detecção do gitleaks. Os [cenários de avaliação](evals/scenarios.json) ainda precisam ser executados e registrados com versões dos agentes, revisão, permissões e resultados.

O [piloto com três tarefas](evals/pilot/REPORT.md) comparou o texto da skill com a tarefa sem skill em sessões novas do Claude. Após um esclarecimento das ferramentas aplicado aos dois lados, gate e rota empataram (5/5 e 4/4); AEO passou em 5/5 com a skill e 4/5 sem ela. O baseline ainda servia um rascunho não publicado. As 12 sessões das duas rodadas congeladas estão registradas, incluindo cinco sem pontuação na primeira após comandos negados. Uma execução por lado em cada rodada não estabelece eficácia geral; a descoberta automática e o plano separado de 22 casos continuam sem avaliação.

A skill de AEO verifica implementação e respostas observadas. Ranking, citações e tráfego precisam de evidência própria. Análises de crédito e outras decisões com consequências precisam de requisitos, dados e avaliação do domínio; a coleção não foi validada como sistema de decisão.

## Origem e licença

Métodos derivados dos meus workflows no CORO SOLTO, Ralph Starter, pesquisa e aeo.js, com colaboração generalizada do trabalho de ECDSA. A [proveniência](PROVENANCE.md) registra revisões e referências. As novas instruções e exemplos foram preparados com assistência de IA.

MIT para o conteúdo novo desta coleção. Projetos referenciados mantêm suas licenças. Suites de terceiros, código privado, assets de jogo e perfis pessoais de escrita ficam fora do pacote. Os artigos em PT-BR e inglês são mantidos no portfólio do autor.
