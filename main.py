import random
import matplotlib.pyplot as plt

def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(card_list):
    card_sum = sum(card_list)

    if card_sum == 21 and len(card_list) == 2:
        return 0  # 0 represents blackjack

    # If over 21 and has Ace, convert Ace from 11 to 1
    if card_sum > 21:
        ace_count = card_list.count(11)
        while card_sum > 21 and ace_count > 0:
            card_list.remove(11)
            card_list.append(1)
            card_sum = sum(card_list)
            ace_count -= 1

    return card_sum

def simulate_game():
    """
    Simulates a single game of Blackjack without any user input.
    Returns the result: 'player', 'dealer', 'push', or 'blackjack'
    """
    # Deal initial cards
    player_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]

    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)

    # Check for immediate blackjack
    if player_score == 0:
        return 'blackjack' if dealer_score != 0 else 'push'
    if dealer_score == 0:
        return 'dealer'

    # Player's turn - use basic strategy
    while player_score < 17 and player_score > 0:  # Simple strategy: stand on 17+
        player_cards.append(deal_card())
        player_score = calculate_score(player_cards)
        if player_score > 21:
            return 'dealer'  # Player busts

    # Dealer's turn
    while dealer_score < 17 and dealer_score > 0:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)
        if dealer_score > 21:
            return 'player'  # Dealer busts

    # Compare scores
    if player_score > dealer_score:
        return 'player'
    elif dealer_score > player_score:
        return 'dealer'
    else:
        return 'push'


def run_simulation(num_games=10000):
    """
    Runs multiple simulations and returns statistics.
    """
    results = {
        'player': 0,
        'dealer': 0,
        'push': 0,
        'blackjack': 0
    }

    for _ in range(num_games):
        result = simulate_game()
        results[result] += 1

    # Calculate percentages
    total_games = num_games
    results['player_pct'] = (results['player'] / total_games) * 100
    results['dealer_pct'] = (results['dealer'] / total_games) * 100
    results['push_pct'] = (results['push'] / total_games) * 100
    results['blackjack_pct'] = (results['blackjack'] / total_games) * 100

    return results


def analyze_strategy():
    """Runs the simulation and prints analysis."""
    print("Blackjack simulation")
    results = run_simulation(10000)  # Run 10000 games

    print("--==-- SIMULATION RESULTS --==--")
    print(f"Games simulated: {sum([results['player'], results['dealer'], results['push'], results['blackjack']])}")
    print(f"Player wins: {results['player']} ({results['player_pct']:.1f}%)")
    print(f"Dealer wins: {results['dealer']} ({results['dealer_pct']:.1f}%)")
    print(f"Pushes: {results['push']} ({results['push_pct']:.1f}%)")
    print(f"Player Blackjacks: {results['blackjack']} ({results['blackjack_pct']:.1f}%)")

    # Calculate house edge
    house_edge = results['dealer_pct'] - results['player_pct']
    print(f"House edge: {house_edge:.1f}%")

    return results



analyze_strategy()

def create_visualization():
    """Creates and saves a visualization of simulation results."""
    results = run_simulation(10000)

    # Data for plotting
    labels = ['Player Wins', 'Dealer Wins', 'Pushes', 'Blackjacks']
    values = [
        results['player_pct'],
        results['dealer_pct'],
        results['push_pct'],
        results['blackjack_pct']
    ]
    colors = ['lightgreen', 'lightcoral', 'lightblue', 'gold']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors, edgecolor='black', alpha=0.7)

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')

    plt.title('Blackjack Outcomes: 10,000 Hand Simulation (Stand on 17+)', fontsize=14, fontweight='bold')
    plt.ylabel('Percentage of Outcomes (%)')
    plt.ylim(0, 55)
    plt.grid(axis='y', alpha=0.3)

    house_edge = results['dealer_pct'] - results['player_pct']
    plt.annotate(f'House Edge: {house_edge:.1f}%',
                 xy=(1, results['dealer_pct']),
                 xytext=(10, 0), textcoords='offset points',
                 ha='left', va='center', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

    plt.tight_layout()
    plt.savefig('blackjack_simulation.png', dpi=300, bbox_inches='tight')
    plt.show()


create_visualization()
