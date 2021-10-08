# Deploy

Este arquivo contém as instruções de deploy deste bot na plataforma [Heroku][1]. 😸

## Discord

Antes de pensar no deploy, precisamos obter um token de acesso fornecido pelo Discord.
Para isto, acesse o [portal de desenvolvedores][2] e clique em "_New Application_" para criar um novo app. Dê um nome (pode ser cationbot mesmo) e prossiga.

No _dashboard_ da sua aplicação, no menu lateral, clique em "_Bot_". Em seguida, clique em "_Add Bot_" e quando o Discord pedir a confirmação, simplesmente
clique em "_Yes, do it_".

### Obtendo o token de acesso

Na guia de "_Bot_", na sessão "_Build-A-Bot_", clique em "Copy" para copiar o token de acesso.
Guarde este token pois precisaremos dele mais tarde.

### Convidando o bot para o servidor

No menu lateral, acesse o "_OAuth2_". Na sessão "_scopes_", selecione somente a opção **bot**.
Na sessão "_bot permissions_", selecione **Administrador**. Uma vez selecionada as duas opções, você verá um link semelhante a este:

```
https://discord.com/api/oauth2/authorize?client_id=<ID_DA_SUA_APLICAÇÃO>&permissions=0&scope=bot
```

É com este link que você convidará o bot para o servidor. Basta colar na URL do seu navegador e, 
quando perguntado onde adicionar o bot, você escolha o canal correspondente.


## Heroku

Uma vez que a aplicação está criada no [portal de desenvolvedores do Discord][2], agora é a hora de publicar a aplicação no Heroku.

Depois de acessar a sua conta, clique no botão "_New_" para criar uma aplicação, dê um nome
(precisa ser único e não precisa necessariamente ser cationbot ou qualquer coisa parecida) e confirme. Pode deixar a região do Estados Unidos mesmo.

No _dashboard_ da sua aplicação, vá em "_Settings_" e em seguida, procure por **buildpacks**.
Clique em "_Add buildpack_" e nas opções selecionadas, escolha o Python.

Ainda na aba de _Settings_, procure por "_Config Vars_" e clique em "_Reveal config vars_". Aqui estão as variáveis de ambiente que você precisa criar:

| Nome da variável | Descrição |
|--------------------|------------|
| TOKEN | Token de acesso fornecido pelo Discord |
| ADMINISTRATORS_ROLE_ID | ID do cargo de administrador do servidor |
| MODERATORS_ROLE_ID | ID do cargo de moderadores do servidor |
| MEMBERS_ROLE_ID | ID do cargo de membros do servidor |
| GUILD_ID | ID do servidor |
| RULES_CHANNEL_ID | ID do canal de regras do servidor |
| RULES_MESSAGE_ID | ID da mensagem na qual os usuários irão reagir com ✅ para ganhar o cargo de membro automaticamente |
| ROLES_CHANNEL_ID | ID do canal de cargos do servidor |
| ROLES_MESSAGE_ID | ID da mensagem na qual os usuários irão reagir para ganhar os cargos automaticamente |
| EMOJI_ROLES | Um objeto contendo o nome do emoji associado ao cargo que irá ser adicionado ou removido, exemplo: `{"clang":821604198453477386,"clojure":821606189778731019,"🎮":829101432330387498}`
| SUGGESTIONS_CHANNEL_ID | ID do canal de sugestões |
| SUGGESTIONS_USEFULL_EMOJI | Reação usada para votar de forma positiva, ex: 👍 |
| SUGGESTIONS_USELESS_EMOJI | Reação usada para votar de forma negativa, ex: 👎 |
| DEFAULT_DM_RESPONSE | Mensagem automática a ser retornada caso alguém envie uma DM para o bot |
| CHANGE_PRESENCE_IN_MINUTES | Tempo em minutos para alterar automaticamente o _presence_ do bot |
| PREFIX | Prefixo para os comandos (embora nenhum tenha sido implementado ainda), ex: `!` |

Depois de definida as variáveis, vá para a aba "_Deploy_" e clique em "Connect to GitHub".
Selecione o repositório contendo o código do bot e habilite os _deploys_ automáticos sempre que rolar merge na branch `main`.
Marque também a opção "_Wait for CI to pass before deploy_" para só fazer o deploy se todos os passos do CI passarem com sucesso.

E é isso! 😸 Você pode disparar um build manualmente ou realizar algum commit na branch `main` para que o build automático aconteça.

> **PS**: se por acaso o bot não funcionar, acesse a aba "_Resources_" e habilite o toggle (que pode estar desligado) para o worker.

[1]:https://www.heroku.com/ 
[2]:https://discord.com/developers/applications/
