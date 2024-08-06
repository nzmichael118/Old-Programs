import client
import time

valid_choices = ["higher", "lower", "bank", "swap"]
def main():
    name = str(input("What is your name?: "))
    curr_client = client.Client(name)
    while True:

        if curr_client.game_state.curr_name == curr_client.name:
            print(f"{curr_client.game_state.curr_card},")
            choice = ""
            while choice not in valid_choices:
                choice = input(f"{valid_choices}").lower()
            curr_client.choice = choice
            # Game has latency so wait 2 seconds before checkign server to see
            # state or will get previous state fix with cool animation on gui to
            # make people not realize they are waiting for the server to catch
            # up

            time.sleep(2)
            if curr_client.game_state.curr_name == curr_client.name:
                print("correct")
            else:
                print(f"incorrect {curr_client.game_state.curr_card}")
            
            

    
if __name__ == '__main__':
    main()