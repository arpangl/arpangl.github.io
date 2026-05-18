import sys

def largest_rectangle_in_histogram(heights):
    """Find the largest rectangle in a histogram."""
    stack = []
    max_area = 0
    n = len(heights)
    for i in range(n + 1):
        h = heights[i] if i < n else 0
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

def solve(M, N, grid):
    """Find the largest rectangle of 0s in the grid."""
    # Build histogram heights row by row
    heights = [0] * N
    max_area = 0
    for i in range(M):
        for j in range(N):
            if grid[i][j] == 0:
                heights[j] += 1
            else:
                heights[j] = 0
        max_area = max(max_area, largest_rectangle_in_histogram(heights))
    return max_area

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        M = int(input_data[idx]); idx += 1
        N = int(input_data[idx]); idx += 1
        if M == 0 and N == 0:
            break
        grid = []
        for i in range(M):
            row = []
            for j in range(N):
                row.append(int(input_data[idx])); idx += 1
            grid.append(row)
        results.append(str(solve(M, N, grid)))
    print('\n'.join(results))

if __name__ == '__main__':
    main()
