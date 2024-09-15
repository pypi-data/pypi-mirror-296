import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.text import Text

from elia_chat.database.database import get_session
from elia_chat.database.models import MessageDao, ChatDao


async def import_chatgpt_data(file: Path) -> None:
    console = Console()

    with open(file, "r") as f:
        data = json.load(f)

    console.print("[green]Loaded and parsed JSON.")

    def output_progress(
        imported_count: int, total_count: int, message_count: int
    ) -> Text:
        style = "green" if imported_count == total_count else "yellow"
        return Text.from_markup(
            f"Imported [b]{imported_count}[/] of [b]{total_count}[/] chats.\n"
            f"[b]{message_count}[/] messages in total.",
            style=style,
        )

    message_count = 0
    with Live(output_progress(0, len(data), message_count)) as live:
        async with get_session() as session:
            for chat_number, chat_data in enumerate(data, start=1):
                chat = ChatDao(
                    title=chat_data.get("title"),
                    model="gpt-3.5-turbo",
                    started_at=datetime.fromtimestamp(
                        chat_data.get("create_time", 0) or 0
                    ),
                )
                session.add(chat)
                await (
                    session.commit()
                )  # Make sure to commit so that chat.id is assigned

                for _message_id, message_data in chat_data["mapping"].items():
                    message_info = message_data.get("message")
                    if message_info:
                        metadata = message_info.get("metadata", {})
                        model = "gpt-3.5-turbo"
                        if metadata:
                            model = metadata.get("model_slug")
                            chat.model = (
                                "gpt-4-turbo" if model == "gpt-4" else "gpt-3.5-turbo"
                            )
                            session.add(chat)
                            await session.commit()

                        role = message_info["author"]["role"]
                        chat_id = chat.id
                        message = MessageDao(
                            chat_id=chat_id,
                            role=role,
                            content=str(message_info["content"].get("parts", [""])[0]),
                            timestamp=datetime.fromtimestamp(
                                message_info.get("create_time", 0) or 0
                            ),
                            model=model,
                            meta=metadata,
                        )
                        session.add(message)
                        message_count += 1
                        live.update(
                            output_progress(chat_number, len(data), message_count)
                        )

                await session.commit()


if __name__ == "__main__":
    path = Path("resources/conversations.json")
    import asyncio

    asyncio.run(import_chatgpt_data(path))
