from Maho_bot import Maho

def main():
    token = input('Enter Discord bot token for Maho: ')

    client = Maho()
    client.run(token)

if __name__ == "__main__":
    main()