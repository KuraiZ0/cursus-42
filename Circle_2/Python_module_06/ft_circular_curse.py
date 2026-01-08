from alchemy.grimoire import record_spell, validate_ingredients


def ing_valid() -> None:
    print("Testing ingredient validation:")
    print(f'validate_ingredients("fire air"):'
          f' {validate_ingredients("fire air")}')
    print(f'validate_ingredients("dragon scales"):'
          f' {validate_ingredients("dragon scales")}')


def spell_valid() -> None:
    print("Testing spell recording with validation:")
    print(f'record_spell("Fireball", "fire air"):'
          f' {record_spell("Fireball", "fire air")}')
    print(f'record_spell("Dark Magic", "shadow"):'
          f' {record_spell("Dark Magic", "shadow")}')


def late() -> None:
    from alchemy.grimoire import record_spell
    print("Testing late import technique:")
    print(f'record_spell("Lightning", "air"):'
          f' {record_spell("Lightning", "air")}')


if __name__ == "__main__":
    print("=== Circular Curse Breaking ===\n")
    ing_valid()
    print()
    spell_valid()
    print()
    late()
    print()
    print("Circular dependency curse avoided using late imports!")
    print("All spells processed safely!")
