# Contribuindo

Este guia tem o objetivo de dar um *overview* de como contribuir com este projeto. Vale ressaltar que qualquer contribuição é bem-vinda, você não precisa necessariamente ter conhecimento em programação. [Reportar problemas e sugerir melhorias][1] pode ser uma forma bacana de iniciar.

## Quero contribuir com sugestões e melhorias

Para isso, basta criar uma [nova issue][1] para que possamos discutir sobre.

## Quero reportar um problema

Crie uma [nova issue][1], bem detalhada, explicando qual é o problema e qual seria o comportamento esperado. Explique como reproduzir o problema e (se aplicável) use *screenshots*, isso pode facilitar a identificação do problema e sua possível correção.

## Quero contribuir programando

Para começar com o desenvolvimento, você precisa ter somente o [Python (3.9+)][2] instalado e o [Poetry][3] — para isolar o ambiente e instalar as dependências. Ainda que não tenha conhecimento em Python, pode nos chamar no servidor do Discord e/ou na própria issue que daremos um *help*. 😺

### Getting Started

- [Instale a última versão do Python 3.9][2] (lembre de marcar para adicionar o Python à variável de ambiente `PATH`, ou você pode fazer isso posteriormente, manualmente).
- Depois de instalado, [instale também o Poetry][3]. Para isso, use o comando:

```sh
pip install poetry
```

Nós recomendamos setar a configuração `virtualenvs.in-project` do Poetry para criar o ambiente virtual no mesmo diretório do projeto (do contrário, será criado no `%homepath%` do usuário). Então, especifique para criar virtual enviroment no mesmo diretório:

```sh
poetry config virtualenvs.in-project true
```

- Clone este repositório e instale as dependências:

```sh
git clone https://github.com/cationhq/cationbot

cd cationbot
poetry install
```

- Antes de executar a aplicação, é necessário criar uma conta de bot e [obter um token de acesso do Discord][5]. Você pode seguir [este guia][6] para criar uma conta de teste e um servidor próprio para executar o bot. Depois de obter o token, renomeie o arquivo `.env.example` para `.env` e altere o valor da variável `TOKEN` para o token disponibilizado pelo Discord.

- Quando você executou o `poetry install`, um diretório `.venv` foi criado no diretório raiz. É onde o "ambiente isolado" do Python está, com nossas dependências. Para "executar" este ambiente isoaldo, primeiro entre no shell desse ambiente e execute a aplicação:

```sh
poetry shell
python -m cationbot

INFO:discord.client:logging in using static token
INFO:discord.gateway:Shard ID None has sent the IDENTIFY payload.
INFO:discord.gateway:Shard ID None has connected to Gateway: ...
```

- Seu bot estará online, basta obter o link de instalação do bot (fornecido no [portal de desenvolvedor do Discord][5]) e adicionar o bot ao seu canal. Se necessário, peça ajuda.

### Pull Requests

- Sempre crie sua *branch* a partir da [`development`][7], que é nossa *branch* base de desenvolvimento.
- Mantenha sua branch sempre atualizada com a nossa `development`. Alguns links úteis: [Como configurar o `remote` do fork](https://docs.github.com/pt/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork) // [Como sincronizar um fork](https://docs.github.com/pt/github/collaborating-with-issues-and-pull-requests/syncing-a-fork)
- Quando for enviar o pull request, detalhe bem o que está sendo alterado. Isso torna a revisão de código mais simples e faz com que suas contribuições sejam mergeadas mais rapidamente.

### E por último... mas também importante

1. Teste o que você faz! É sério, teste faz bem e causa menos dores de cabeça. 😿 Se alterou algum comportamento e/ou adicionou novas *features*, garanta que você também está entregando os testes unitários que validem esse novo estado do código. Se necessário, peça ajuda.

2. Nós utilizamos alguns recursos para manter a padronização de código. Se você utiliza o VScode, basta instalar as dependências recomendadas que serão exibidas na primeira vez que abrir este repositório no editor. Você pode ver no arquivo `.vscode/extensions.json` as extensões que recomendamos.

*— cationdevs.*

[1]:https://github.com/cationhq/cationbot/issues
[2]:https://www.python.org/downloads/
[3]:https://python-poetry.org/docs/#installation
[4]:https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean
[5]:https://discord.com/developers/applications
[6]:https://discordpy.readthedocs.io/en/latest/discord.html
[7]:https://github.com/cationhq/cationbot/tree/development
