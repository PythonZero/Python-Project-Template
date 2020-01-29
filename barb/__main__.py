from barb import load_config, start_logging, ErrorManager

if __name__ == "__main__":
    load_config()
    start_logging()

    run() # your code goes here
    ErrorManager.raise_first()
