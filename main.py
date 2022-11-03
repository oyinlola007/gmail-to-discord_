import discord, imaplib, email, asyncio

import cogs.config as config
import cogs.utils as utils

client = discord.Client()


@client.event
async def on_ready():
    """Shows when bot has successfully connected
    """
    print(f"We have logged in as {client.user}")


async def user_metrics_background_task():
    """Background task that runs at intervals
    """
    await client.wait_until_ready()
    while True:
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            (retcode, capabilities) = mail.login(config.GMAIL_USERNAME, config.GMAIL_PASSWORD)
            mail.list()
            mail.select('inbox')
            (retcode, messages) = mail.search(None, '(UNSEEN)')

            channel = client.get_channel(config.DISCORD_CHANNEL)

            if retcode == 'OK':
                for num in messages[0].split():
                    try:
                        typ, data = mail.fetch(num,'(RFC822)')

                        for response_part in data:
                            if isinstance(response_part, tuple):
                                original = email.message_from_bytes(response_part[1])
                                _from = original['From']
                                _subject =  original['Subject']

                                for part in original.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode("utf-8")
                                        embed=discord.Embed(title=_subject, description=f">>> {body}", color=config.EMBED_COLOR)
                                        embed.set_footer(text=_from)
                                        await channel.send(embed=embed)
                                        break

                                    elif part.get_content_type() == "text/html":
                                        body = utils.parse_pdf(str(part))
                                        embed=discord.Embed(title=_subject, description=f">>> {body}", color=config.EMBED_COLOR)
                                        embed.set_footer(text=_from)
                                        await channel.send(embed=embed)

                                typ, data = mail.store(num,'+FLAGS','\\Seen')

                    except:
                        pass
        except:
            pass

        for i in range(config.LOOP_DELAY):
            await asyncio.sleep(1)


client.loop.create_task(user_metrics_background_task())
client.run(config.DISCORD_TOKEN)
