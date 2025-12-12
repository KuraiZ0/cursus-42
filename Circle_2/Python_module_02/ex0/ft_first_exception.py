# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_first_exception.py                              :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/10 21:39:04 by ialmani           #+#    #+#             #
#    Updated: 2025/12/10 21:39:09 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


def check_temperature(temp_str):
    temp_str = str(input("Enter the temperature: "))
    try:
        temp = int(temp_str)
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number.")
        return None
    if temp > 40:
        print(f"Error: {temp}°C is too hot for plants (max 40°C).")
    elif temp < 0:
        print(f"Error: {temp}°c is too cold for plants (min 0°C).")
    else:
        print(f"Temperature {temp}°C is perfect for plants!")
        return temp


def test_temperature_input():
    check_temperature("25")
    print()
    check_temperature("abc")
    print()
    check_temperature("100")
    print()
    check_temperature("-50")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    print()
    test_temperature_input()
    print("All tests completed - program didn't crash!")
