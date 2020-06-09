import asyncio
import itertools
import logging
import os
import re
import tempfile

import click
import pyqrcode

import kyros

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logging.getLogger("kyros").setLevel(logging.ERROR)
logger = logging.getLogger("wabf")  # noqa


async def amain(phone_number, disable_cache, output_format, output_file):
    whatsapp = await kyros.Client.create()
    cache_filepath = os.path.join(tempfile.gettempdir(), "wabf.s")

    if disable_cache or not await load_cache(whatsapp, cache_filepath):
        qr_data, scanned = await whatsapp.qr_login()
        qr_code = pyqrcode.create(qr_data)
        print(qr_code.terminal(quiet_zone=1))

        try:
            await scanned
        except asyncio.TimeoutError:
            await whatsapp.shutdown()
            return

        if not disable_cache:
            whatsapp.session.save_to_file(cache_filepath)

    logger.info("logged in, wid: %s", whatsapp.session.wid)

    logger.info("generating possible jids...")
    jids = generate_jids(phone_number)
    logger.info("starting bruteforce... (results are shown below)")

    if output_file:
        logger.info("will also write results to %s", output_file)
        output_file = open(output_file, "w")

    for jid in jids:
        print(f"\rcurrently trying: {jid}", end="")
        while True:
            try:
                status = await check(whatsapp, jid)
            except asyncio.TimeoutError:
                continue
            else:
                break

        if status == 200:
            print("\r", end="")
            formatted_output = format_output(jid, output_format)
            if output_file:
                output_file.write(f"{formatted_output}\n")
            logger.info("FOUND: %s", formatted_output)

    print("\r", end="")
    logger.info("finished, shutting down... %s", " " * 10)


async def check(whatsapp, jid):
    message = kyros.websocket.WebsocketMessage(None, ["query", "exist", jid])
    await whatsapp.websocket.send_message(message)

    reply = await whatsapp.websocket.messages.get(message.tag, 4)
    return reply["status"]


async def load_cache(whatsapp, cache_filepath):
    if not os.path.exists(cache_filepath):
        return False

    logger.info("found a session cache file, trying to load...")
    session = kyros.Session.from_file(cache_filepath)

    exc, _ = await whatsapp.ensure_safe(whatsapp.restore_session, session)
    if exc:
        logger.error("failed to load session cache, waiting for qr scan...")
        return False
    return True


def generate_jids(phone_number):
    if phone_number.count("[") != phone_number.count("]") \
            or not re.match(r"^[x\[\]0-9]+$", phone_number):
        raise ValueError("invalid phone number format")

    prog = re.compile(r"(x|\[\d+?\])")
    template = prog.sub("{}", phone_number)

    possible_fills = []
    for unknown in prog.findall(phone_number):
        if unknown == "x":
            possible_fills.append("0123456789")
        else:
            possible_fills.append(unknown.strip("[]"))

    product = itertools.product(*possible_fills)
    for possible_fill in product:
        yield f"{template.format(*possible_fill)}@c.us"


def format_output(jid, output_format):
    templates = {"wa.me": "https://wa.me/{}", "jid": "{}@c.us", "pn": "{}"}
    stripped_jid = jid.rstrip("@c.us")
    return templates[output_format].format(stripped_jid)


@click.command()
@click.argument("phone_number")
@click.option("--disable-cache",
              "-dc",
              is_flag=True,
              help="Disable session caching")
@click.option("--output-format",
              "-f",
              type=click.Choice(["wa.me", "jid", "pn"], case_sensitive=False),
              default="wa.me",
              help="Result output format")
@click.option("--output-file",
              "-o",
              type=str,
              default=None,
              help="Specify output file")
def main(*args, **kwargs):
    logger.info(click.style("wabf \u2014 whatsapp bruteforcer", fg="green"))
    asyncio.run(amain(*args, **kwargs))


if __name__ == "__main__":
    main()  # noqa
