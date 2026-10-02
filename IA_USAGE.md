# Uso de Inteligência Artificial

> Resumo : **a IA gerou a maior parte do código; o meu trabalho foi
> planejar com ela, executar, testar, estudar cada trecho até conseguir
> entender completamente a lógica, organizar o Git e documentar.
> usei do desafio também para recordar alguns conceitos da stack.

## Linha do tempo

| Data | O que aconteceu |
|---|---|
| Ter 29/09 | Planejamento com a IA, setup do ambiente, commit inicial |
| Qua 30/09 | Consulta ao ViaCEP, persistência, histórico, tratamento de erros, validação estrita do CEP |
| Qui 01/10 | Segurança, frontend em React, testes automatizados, README e este documento |

Tempo total aproximado gasto: ** 12h, contando estudo**.
Distribuição: **60% estudando/entendendo o código, 25% executando e testando, 15% Git/documentação**.

## 1. Ferramentas utilizadas

- **Claude (Anthropic):** planejamento do projeto, geração do código, fluxo de Git (branches e PRs), revisão de segurança, testes e rascunho de documentação.
- **Gemini (Google):** ferramenta de estudo. Usei para pedir explicações linha a linha do código gerado, tirar dúvidas de Python (relembrar de forma aprofundada conceitos como decorators, `classmethod`) e resolver problemas de ambiente (nvm, versão do Node). Também usei o Gemini para pesquisa inicial (documentação do ViaCEP, boas práticas de README, Git, boas práticas de programação e arquitetura).
- Não usei GitHub Copilot nem outras ferramentas além do vscode puro apenas com extensões sem ia.

## 2. Em quais etapas usei IA

| Etapa | Ferramenta | Branch |
|---|---|---|
| Planejamento e escolha da stack | Gemini | Claude `main` |
| Consulta ao ViaCEP (schemas, serviço, rota) | Claude (código), Gemini (explicação, depuração do código parte a parte) | `feat/consulta-viacep` |
| Persistência com SQLAlchemy | Claude, Gemini | `feat/persistencia` |
| Histórico paginado | Claude, Gemini | `feat/historico` |
| Tratamento de erros e logging | Claude, Gemini | `fix/tratamento-erros` |
| Segurança (regex, rate limit, headers) | Claude, Gemini | `fix/seguranca` |
| Frontend em React | Claude, Gemini (tenho uso mais recente de javascript/React)| `feat/frontend-react` |
| Testes automatizados | Claude | `test/api` |
| README e este documento | Claude(fiz alterações pertinentes bem como também revisei parte a parte do documento) | `docs/readme` |

## 3. Exemplos de prompts

Prompts reais, copiados das minhas conversas:

1. **Planejamento (Claude):** *"preciso de uma rápida revisão de conceitos de python relacionados a utilização de Fast/API antes de começarmos"*
2. **Fluxo de Git (Claude):** *"vamos trabalhar com branches, preciso que você verifique o padrão de mercado utilizado para nomear branchs, bem como boas práticas… vamos reformular o passo a passo e refazer explicando as etapas"*
3. **Segurança (Claude):** *"antes de prosseguirmos, vamos revisar algumas práticas relacionadas a segurança para que possamos deixar o serviço mais robusto e previnir ataques, quero que você se preocupe com ataques tipo DDoS, negação de serviço, script injection, SQL injection, entre outros que não mencionei mas que são pertinentes para o nosso projeto"*
4. **Frontend (Claude):** *"vamos prosseguir, eu gostaria de utilizar React no projeto, diferente do que você sugeriu anteriormente, vou lhe dar total autonomia para desenvolver o front e farei apenas correções se necessário ou se for preciso alterar algum visual"*
5. **Estudo (Gemini):** *"explique mais detalhadamente datetime, pydantic, BaseModel, field_validator… eu estou achando muito superficial suas explicações sobre a utilização destas bibliotecas, lembre que eu não as utilizo a algum tempo e preciso entender o potencial e utilização correta de todas elas"*
6. **Estudo (Gemini):** *"como eu executo curl -s -X POST … com o meu servidor rodando, onde eu coloco este código?"*
7. **Ambiente (Gemini):** *"npm run dev … SyntaxError: The requested module 'node:util' does not provide an export named 'styleText'"* (era o Node 18; resolvi instalando o Node 22 com nvm), me explique o erro detalhadamente e como corrigi-lo (seja especifico)
8. **Pesquisa (Gemini):** pedi uma pesquisa em 7 frentes: documentação do ViaCEP, backend com FastAPI/Spring Boot, persistência com SQLite/PostgreSQL, interface em React/HTML, modelos de documentação de uso de IA, padrões de Git/README e arquitetura limpa com tratamento de erros após isso verifiquei os pontos fortes e fracos de cada resultado que ele me apontou.

## 4. Como validei as respostas

Não aceitei nada sem executar. Em cada branch:

- **Executei o código e testei manualmente** os cenários de sucesso, CEP inexistente (`99999999`), formato inválido (`abc`, `123`), timeout forçado e rede desligada.
- **Conferi o banco com `sqlite3`** para garantir que consultas com erro **não** gravam registros.
- **Testei payloads de ataque** (`1; DROP TABLE consultas;--`, dígitos Unicode largos, hifens no meio) e o rate limit (10 requisições passam, a 11ª recebe `429`).
- **Testei XSS na tela:** inseri um registro com `<img src=x onerror=alert(1)>` no banco e confirmei que o React o exibe como texto.
- **Rodei a suíte de testes:** 27 testes passando (`pytest -v`), quebrei algumas partes do código de propósito para validar a eficiência dos testes.
- **Segui o README do zero** em uma pasta limpa nos sistemas kali linux e windows para verificar se seria possivel reproduzir tudo do zero.
- **Cruzei fontes:** usei o Gemini para explicar o que o Claude gerou e comparei as duas explicações bem como também utilizei da documentação de algumas bibliotecas e frameworks na internet para fortalecer ainda mais a autenticidade das explicações.

## 5. Sugestões da IA que aproveitei

- Stack: Python + FastAPI + SQLite + React (Vite).
- Arquitetura em camadas: rotas, serviço, repositório, schemas e models.
- Exceções próprias no serviço do ViaCEP, com `504` para timeout e `502` para as demais falhas do serviço externo.
- Tratamento da "pegadinha" do ViaCEP: CEP inexistente volta `200` com `{"erro": true}`.
- Mapeamento `localidade` → `cidade` e alias `dataConsulta` no JSON (ASSIM COMO O DESAFIO TINHA PROPOSTO) mantendo `snake_case` no Python (pedi ao python que utiliza-se PEP 8 assim como outros padrões de estilo de cada linguagem).
- Paginação no histórico (`limite` e `offset`).
- Logging com níveis e `rollback` em falha de gravação.
- Segurança: regex estrita para o CEP, rate limiting (`slowapi`), headers de segurança e CSP (questionei a IA sobre algumas falhas comuns de segurança que identifiquei no código).
- Prefixo `/api` e proxy do Vite (evita CORS em desenvolvimento e simplificar o desenvolvimento do desafio).
- Testes com banco SQLite em memória e ViaCEP simulado (mock), sem acessar a internet.
- Fluxo de Git com uma branch e um Pull Request por funcionalidade.

## 6. Sugestões descartadas, adiadas ou erros da IA que corrigi

**Descartado ou adiado:**.
- **Autenticação, DDoS volumétrico e HTTPS:** fora do escopo do desafio (são infraestrutura ou evolução futura); ficaram documentados no README.
- **SQLAlchemy assíncrono e Alembic:** descartados por complexidade; o volume do projeto não justifica.
- **Do material de pesquisa do Gemini:** não adotei CORS middleware (usei proxy do Vite), `pytest-asyncio` e `respx` (usei `asyncio.run` e `httpx.MockTransport`, com menos dependências), nem uma pasta `repositories/` separada (usei um único `repository.py`).
- **Fingerprint e cookies de identificação:** conversei com o Gemini sobre o tema, mas ficou fora do projeto por não fazer parte dos requisitos (e envolve LGPD).

**Erros da IA que foram encontrados e corrigidos:**
- **Validador de CEP:** o primeiro código usava `isdigit()` e `replace("-", "")`, que aceitam dígitos Unicode e hifens fora de lugar (ex.: `5-9-0-0-0-0-0-0`). Foi trocado por regex ASCII estrita (commit `fix: valida CEP com regex estrita`). Também confirmei que o `curl` com `5-9-0-0-0-0-0-0` passava no validador antigo e passou a dar `422`.
- **Contagem de testes:** a IA estimou "cerca de 30"; o `pytest` mostrou 27. Conferi a contagem pela saída real bem como fiz a checagem de alguns que acreditei serem de maior relevancia ou o código não estava tão simples de ser avaliado.
- **Explicações do Gemini nem sempre batiam com o meu código** (por exemplo, descreveu a listagem com `db.query(...)`, enquanto o projeto usa `select()`). Por isso confirmei no código real antes de confiar na explicação.
- **Sugestão do Gemini para silenciar o aviso do `pytest`** com um `filterwarnings` apontando para uma classe do Starlette: não apliquei, porque o aviso é inofensivo (afeta só os testes) e não quis arriscar quebrar a configuração com pouco tempo para a entrega.

## 7. O que desenvolvi ou ajustei manualmente

**Sou transparente quanto a isto:** não escrevi o código do zero. utilizei o código gerado pela IA, executei, quebrei, corrigi e estudei cada arquivo até conseguir explicá-lo e me certificar que não haviam falhas na logica.

O que fiz com as minhas mãos:

- Configurei o ambiente do zero (Python `venv`, Node via nvm), incluindo resolver o erro do Node 18 vs. Vite.
- Criei o repositório e conduzi o **fluxo de Git**: 7 branches, 7 Pull Requests com merge commit, e as mensagens dos commits (algumas no padrão Conventional Commits, outras descritivas, conforme o cap. abaixo).
- Executei e interpretei todos os testes manuais em cada etapa de branchs (`curl`, `sqlite3`, rate limit, XSS).
- Adicionei comentários no código para me ajudar a entender funções ou partes do código muito densas e para fazer possíveis manutenções posteriormente
- Estudei os conceitos por trás de cada trecho e revisei conceitos que já não estavam tão claros para mim por causa de tempo sem ter praticado com a stack (decorators, `, `async/await`, injeção de dependência, ORM, hooks do React...) e fiz perguntas até entendê-los.

## 8. Aprendizados e limitações

- Aprendi principalmente conceitos sobre testes automatizados que nunca havia me aprofundado ou utilizado anteriormente.
- Percebi alguns erros cometidos pela IA (validador, contagem de testes, explicações divergentes do código real) e que **validar executando** É indispensável principalmente antes de mergear uma branch com a main.
- Limitação: o ritmo foi muito rápido e há partes que ainda estou consolidando, como SQLAlchemy. 


## Registro cronológico (commits reais)

| Branch / PR | Commit |
|---|---|
| `main` | commit inicial |
| `feat/consulta-viacep` (#1) | schemas de validação, serviço que consome o ViaCEP e rota de consulta |
| `feat/persistencia` (#2) | arquivos de configuração e interação com o banco |
| `feat/historico` (#3) | consulta/listagem no banco de dados |
| `fix/tratamento-erros` (#4) | logging + tratamento de erros; `chore: adiciona configuração de logging` |
| `fix/seguranca` (#5) | `fix: valida CEP com regex estrita`; segurança implementada pela IA, revisada e idealizada por mim |
| `feat/frontend-react` (#6) | frontend em React com auxílio de IA |
| `test/api` (#7) | testes automatizados criados com IA |
| `feat/ajustes-extras` (#8) | cookie de visitante com consentimento, minhas buscas com paginação, scroll infinito nas buscas gerais e limpeza do campo de CEP |
| `docs/readme` (#9) | README e este documento |



