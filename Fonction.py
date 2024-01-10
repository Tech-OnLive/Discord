async def on_reaction_add(reaction, user):
    required_role_name = "DIGGERS/LFDM"

    if isinstance(user, discord.Member):
        if any(role.name == required_role_name for role in user.roles):
            if reaction.emoji == "📌" and user != client.user:
                message = reaction.message
                message_data = {
                    'content': message.content
                }

                # Enregistre les données dans un fichier JSON
                with open('MessageDuJour.json', 'a') as f:
                    json.dump(message_data, f)
                    f.write('\n')

async def on_message(message):
    required_role_name = "DIGGERS/LFDM"

    # Vérifie si l'auteur du message a le rôle requis
    if isinstance(message.author, discord.Member):
        if any(role.name == required_role_name for role in message.author.roles):
            if message.content == '!auj':
                try:
                    # Ouvre et lit le fichier des message enregistrés
                    with open('MessageDuJour.json', 'r') as f:
                        response = ''
                        for line in f:
                            message_data = json.loads(line)
                            response += f"{message_data['content']}\n"

                    # Envoie un message avec tous les messages enregistrés
                    if response:
                        await message.channel.send(response)
                    else:
                        await message.channel.send("Pas de message enregistré aujourd'hui.")
                except FileNotFoundError:
                    await message.channel.send("Pas de fichier avec les messages.")
                except Exception as e:
                    await message.channel.send(f"Erreur: {e}")  
