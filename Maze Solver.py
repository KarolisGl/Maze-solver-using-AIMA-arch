from search import Problem, astar_search
import tkinter as tk
import random


# Autorius: Ernestas Granauskas Prifs 22/4, Karolis Glodenis Prif 22/1, ChatGPT.com
# Data: 2025-02-23
# Aprašymas: Ši programa įgyvendina labirinto sprendimo problemą naudojant AIMA architektūrą su vizualizacija.

class MazeProblem(Problem):
    def __init__(self, initial, goal, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        super().__init__(initial, goal)

    def actions(self, state):
        row, col = state
        possible_moves = []
        directions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

        for action, (dr, dc) in directions.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
                possible_moves.append(action)

        return possible_moves

    def result(self, state, action):
        directions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
        dr, dc = directions[action]
        return (state[0] + dr, state[1] + dc)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        row, col = node.state
        goal_row, goal_col = self.goal
        return abs(goal_row - row) + abs(goal_col - col)  # Manhattan Distance


class MazeGUI:
    def __init__(self, root, maze, path, start, goal):
        self.root = root
        self.maze = maze
        self.path = path
        self.start = start
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.cell_size = 40
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()
        self.draw_maze()
        self.root.after(500, self.animate_solution)

    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                if (i, j) == self.start:
                    color = "green"  # Start position
                elif (i, j) == self.goal:
                    color = "red"  # Goal position
                else:
                    color = "black" if self.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')

    def animate_solution(self, step=0):
        if step < len(self.path):
            row, col = self.path[step]
            x0, y0 = col * self.cell_size, row * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='black')
            self.root.after(300, self.animate_solution, step + 1)


maze = [
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0]
]

initial_state = (0, 0)
goal_state = (5, 5)
problem = MazeProblem(initial_state, goal_state, maze)
solution_node = astar_search(problem)
solution_path = solution_node.path() if solution_node else []
path = [node.state for node in solution_path]

if solution_path:
    root = tk.Tk()
    root.title("Labirinto Sprendimas")
    gui = MazeGUI(root, maze, path, initial_state, goal_state)
    root.mainloop()
else:
    print("Kelias nerastas!")
