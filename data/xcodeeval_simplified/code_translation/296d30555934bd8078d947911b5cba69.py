def main():
    r1, c1, r2, c2 = map(int, input().split())
    rook_moves = 1 if r1 == r2 or c1 == c2 else 2
    if (r1 + c1) % 2 != (r2 + c2) % 2:
        bishop_moves = 0
    elif r1 + c1 == r2 + c2 or r1 - c1 == r2 - c2:
        bishop_moves = 1
    else:
        bishop_moves = 2
    king_moves = max(abs(r1 - r2), abs(c1 - c2))
    print(rook_moves, bishop_moves, king_moves)
if __name__ == "__main__":
    main()