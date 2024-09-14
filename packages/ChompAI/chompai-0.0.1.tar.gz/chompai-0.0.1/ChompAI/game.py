import os
import numpy as np

def read_p_positions(p_positions_file):
    '''
    Given the file path of p_positions list, read the p_positions into memory.
    '''
    p_positions = list()    
    with open(p_positions_file, 'r') as fhand:
        for line in fhand:
            p_position = line.split(',')
            if len(p_position) > 1:
                p_position = [int(i) for i in p_position]
                p_position = tuple(p_position)
                p_positions.append(p_position)
    
    return p_positions

def refine_p_positions(p_positions, board_size_x, board_size_y):
    '''
    Given the p_positions list from a larger board, calculate the p_positions list for the sub-board of the large board.
    '''
    p_positions_refined = list()
    for p_position in p_positions:
        if (np.amax(p_position) <= board_size_x) and (np.sum(p_position[board_size_y:]) == 0):
            p_positions_refined.append(p_position[:board_size_y])
    
    return p_positions_refined

def board_to_state(board):
    '''
    Given a game state on chomp board in numpy array format, return a state in tuple format.
    '''
    size_y, size_x = np.shape(board)
    state = list()
    for k in range(size_y):
        state.append(np.sum(board[k]))
    state = tuple(state)
    return state

def state_to_board(state, size_x, size_y):
    '''
    Given a state in tuple format, return a game state on chomp board in numpy array format.
    '''
    board = np.zeros((size_y, size_x), dtype = int)
    for i in range(size_y):
        board[i,:state[i]] = 1
    return board

def board_tructation(board, action):
    '''
     Given a game state on chomp board in numpy array format and an action of player, return the resulted game state.
    '''
    board_trucated = board.copy()
    board_trucated[action[0]:,action[1]:] = 0
    return board_trucated

def AI_strategy(board, p_positions):
    '''
    Given a game state on Chomp board in numpy array format, find the optimal action strategy.
    '''
    # Change the state from numpy array format to tuple format
    state = board_to_state(board)
    size_y, size_x = np.shape(board)
    # If the state is not in p_positions, the AI must have an optimal strategy
    if state not in p_positions:
        strategy_candidates = list()
        resulted_p_positions = list()
        for i in range(size_y):
            for j in range(size_x):
                if board[i][j] == 1:
                    board_trucated = board_tructation(board = board, action = (i,j))
                    state_truncated = board_to_state(board_trucated)
                    if tuple(state_truncated) in p_positions:
                        strategy_candidates.append((i,j))
                        resulted_p_positions.append(tuple(state_truncated))
        # Choose the optimal strategy , which ends the game most fast, among the strategy candidates
        #strategy_optimal_index = 0
        #strategy_optimal = strategy_candidates[strategy_optimal_index]

        # Choose the optimal strategy , which ends the game most slow, among the strategy candidates
        strategy_optimal_index = -1
        strategy_optimal = strategy_candidates[strategy_optimal_index]

        size_p_positions_minimal = np.sum(resulted_p_positions[strategy_optimal_index])
        for i in range(len(strategy_candidates)):
            if np.sum(resulted_p_positions[i]) < size_p_positions_minimal:
                strategy_optimal_index = i
                strategy_optimal = strategy_candidates[strategy_optimal_index]
                size_p_positions_minimal = np.sum(resulted_p_positions[strategy_optimal_index])
    # If the state is in positions, the AI should enlongate the game as much as possible and wait the opponent to make mistakes by choosing a strategy that reduces the size of board minimum
    # Always choose the board grid with maximum i and j where board[i][j] == 1
    else:
        # Initialize the optimal strategy
        y_optimal = 0
        strategy_optimal = (y_optimal, state[0]-1)
        for i in range(size_y):
            if (board[i][state[0]-1] == 1) and (i > y_optimal):
                y_optimal = i
        strategy_optimal = (y_optimal, state[0]-1)

    return strategy_optimal

def best_move(board):
    p_positions_file = os.path.join(os.path.dirname(__file__), 'p_positions_12x12.txt')
    p_positions = read_p_positions(p_positions_file)
    p_positions = refine_p_positions(p_positions, board.shape[1], board.shape[0])
    return AI_strategy(board, p_positions)
