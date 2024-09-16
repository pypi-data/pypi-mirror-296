import click
from conways_game_of_life.game_of_life import run_game

@click.command()
def main():
    """
    Launch Conway's Game of Life.
    """
    print("Launching Conway's Game of Life...")
    run_game()

if __name__ == "__main__":
    main()
