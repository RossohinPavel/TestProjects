def set():
    try:
        from dotenv import load_dotenv
        from pathlib import Path

        load_dotenv(Path(__file__).parent.parent.joinpath('.env'))

    except:
        pass
