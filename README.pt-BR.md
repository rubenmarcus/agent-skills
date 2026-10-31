# Skills do Ruben para agentes

[English](README.md)

11 workflows para Codex e Claude Code, extraídos dos meus projetos e reescritos como instruções reutilizáveis. Debugging, review adversarial, loops de melhoria, pesquisa com fontes, colaboração, hooks Git e AEO.

**Versão 0.1.0, licença MIT.** Os checks de estrutura e exemplos isolados passaram. A avaliação comportamental completa com os dois agentes continua pendente. A distribuição é por Git e metadados de plugin; não há release no npm.

## Escolha pelo problema

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

## Um primeiro teste

```text
Use critical-adversarial-review para revisar BASE..HEAD.
O endpoint deve preservar a paginação quando o filtro muda.
Leia o diff e os callers, sem alterar arquivos.
Informe localização, entrada que dispara a falha, resultado esperado,
resultado observado e reprodução mínima. Identifique hipóteses ainda
não executadas. Aceito zero findings.
```

Troque `BASE..HEAD` pelas revisões reais. Para testar um gate, use `quality-gates` numa cópia descartável, aplique uma alteração deliberadamente quebrada e confira se o gate reprova pelo motivo esperado. Para pesquisa, forneça as versões e fontes de partida e peça o registro das inferências separado dos relatos.

## Validação e limites

Node.js 20+ executa o check estrutural sem dependências npm. Python 3 executa o fixture do hook.

```sh
npm run check
npm run check:hook
claude plugin validate . --strict
npm pack --ignore-scripts --pack-destination /tmp
```

`check` verifica metadados, referências, manifests e cenários. `check:hook` usa um scanner falso para verificar argumentos e propagação dos códigos de saída; ele não mede a detecção do gitleaks. Os [cenários de avaliação](evals/scenarios.json) ainda precisam ser executados e registrados com versões dos agentes, revisão, permissões e resultados.

A skill de AEO verifica implementação e respostas observadas. Ranking, citações e tráfego precisam de evidência própria. Análises de crédito e outras decisões com consequências precisam de requisitos, dados e avaliação do domínio; a coleção não foi validada como sistema de decisão.

## Origem e licença

Métodos derivados dos meus workflows no CORO SOLTO, Ralph Starter, pesquisa e aeo.js, com colaboração generalizada do trabalho de ECDSA. A [proveniência](PROVENANCE.md) registra revisões e referências. As novas instruções e exemplos foram preparados com assistência de IA.

MIT para o conteúdo novo desta coleção. Projetos referenciados mantêm suas licenças. Suites de terceiros, código privado, assets de jogo e perfis pessoais de escrita ficam fora do pacote. Os artigos em PT-BR e inglês são mantidos no portfólio do autor.
