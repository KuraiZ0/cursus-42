# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_different_errors.py                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/11 09:59:39 by ialmani           #+#    #+#             #
#    Updated: 2025/12/11 10:37:24 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


def garden_operator():
    try:
        print("Testing ValueError...")
        int("abc")
        print("No error.")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")
    try:
        print("Testing ZeroDivisionError...")
        42 / 0
        print("No error.")
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero\n")
    try:
        print("Testing FileNotFoundError...")
        open("sneh.txt", "r")
        print("No error.\n")
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file 'sneh.txt'\n")
    try:
        print("Testing KeyError...")
        test3 = {"existing_plant": "rose"}
        print(test3["plant_green"])
    except KeyError:
        print("Caught KeyError: 'missing plant'\n")
    try:
        print("Testing multiple errors together...")
        int("abc")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continue!\n")


def test_error_types():
    garden_operator()
    print("\nAll error types tested successfully!\n")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")
    test_error_types()
