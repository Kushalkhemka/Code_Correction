def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1

    return max(dp.values()) if dp else 0


if __name__ == "__main__":
    # Simple tests
    print(lcs_length('witch', 'sandwich'))  # expected output: 2
    print(lcs_length('meow', 'homeowner'))    # expected output: 4
