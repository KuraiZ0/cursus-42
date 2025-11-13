#!/bin/bash

# test_push_swap_debug.sh
# Usage: ./test_push_swap_debug.sh ./push_swap_executable

PUSH_SWAP=$1

if [ -z "$PUSH_SWAP" ]; then
    echo "Usage: $0 ./push_swap_executable"
    exit 1
fi

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Tests
tests=(
    "2 1 3 6 5"
    "3 2 1"
    "1 2 3 4"
    "5 4 3 2 1"
    "10 3 7 2 8 1"
    "6 5 4 3 2 1"
    "8 1 3 2 7 5"
    "9 4 2 6 1 3 5 7 8"
)

echo -e "=== PUSH_SWAP DEBUG TESTER ==="

for t in "${tests[@]}"; do
    echo -e "\n${YELLOW}Test pile: $t${NC}"
    echo "Operations:"

    # Récupérer les opérations générées par push_swap
    ops=$($PUSH_SWAP $t)
    echo "$ops"

    # Appliquer les opérations pour vérifier le tri et afficher A/B à chaque étape
    python3 - <<EOF
A = list(map(int, "$t".split()))
B = []

print("\nStep by step:")
for i, op in enumerate("""$ops""".splitlines(), start=1):
    if op == "sa" and len(A) > 1:
        A[0], A[1] = A[1], A[0]
    elif op == "sb" and len(B) > 1:
        B[0], B[1] = B[1], B[0]
    elif op == "ss":
        if len(A) > 1: A[0], A[1] = A[1], A[0]
        if len(B) > 1: B[0], B[1] = B[1], B[0]
    elif op == "pa" and B:
        A.insert(0, B.pop(0))
    elif op == "pb" and A:
        B.insert(0, A.pop(0))
    elif op == "ra" and len(A) > 1:
        A.append(A.pop(0))
    elif op == "rb" and len(B) > 1:
        B.append(B.pop(0))
    elif op == "rr":
        if len(A) > 1: A.append(A.pop(0))
        if len(B) > 1: B.append(B.pop(0))
    elif op == "rra" and len(A) > 1:
        A.insert(0, A.pop())
    elif op == "rrb" and len(B) > 1:
        B.insert(0, B.pop())
    elif op == "rrr":
        if len(A) > 1: A.insert(0, A.pop())
        if len(B) > 1: B.insert(0, B.pop())

    print(f"{i:02d}: {op:5} | A: {A} | B: {B}")

if A == sorted(A) and not B:
    print("\n✅ Pile triée")
else:
    print("\n❌ Pile non triée")
EOF

    echo "------------------------"
done
