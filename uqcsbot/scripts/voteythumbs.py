from uqcsbot import bot, Command
from functools import partial


VOTEYTHUMBS_STRIP_PREFIXES = [
    '@channel',
    '@here',
    '@everyone',
    ':'  # intentionally last
]


def strip(message: str, prefixes=VOTEYTHUMBS_STRIP_PREFIXES):
    while True:
        # keep going until you didn't strip anything last pass
        for prefix in prefixes:
            if message.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        else:
            break
    return message


@bot.on('message')
async def voteythumbs(evt: dict):
    if "!voteythumbs" not in evt.get("text", ""):
        return
    evt["text"] = strip(evt["text"])
    cmd = Command.from_message(bot, evt)
    if cmd is None:
        return
    if not cmd.has_arg() and "!voteythumbs" in evt["text"]:
        await bot.run_async(bot.post_message, cmd.channel, "Invalid voteythumbs command")
    if not cmd.has_arg():
        bot.logger.error("Invalid voteythumbs command")
        return
    cmd.arg = strip(cmd.arg)

    result = await bot.run_async(bot.post_message, cmd.channel, f"Starting vote: {cmd.arg}")
    add_reaction = partial(
        bot.run_async,
        bot.api.reactions.add,
        channel=cmd.channel.id,
        timestamp=result['ts'],
    )
    for emoji in ["thumbsup", "thumbsdown", "eyes"]:
        res = await add_reaction(name=emoji)
        if not res.get('ok'):
            bot.logger.error(f"Voteythumbs error adding \"{emoji}\": {res}")
            return
