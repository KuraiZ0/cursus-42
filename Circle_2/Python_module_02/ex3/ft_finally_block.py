# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_finally_block.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/11 13:13:36 by ialmani           #+#    #+#             #
#    Updated: 2025/12/11 14:28:31 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


def water_plant(plant_list):
    print("Opening watering system")
    try:
        for plant in plant_list:
            if plant is None:
                raise ValueError(f"Cannot water {plant} - invalid plant!")
            print(f"Watering {plant}")
    except Exception as e:
        print(f"Error: {e}")
        return
    finally:
        print("Closing watering system (cleanup)")
    print("Watering completed successfully!")


def test_watering_system():
    print("Testing with error...")
    bad_list = ['tulip', None]
    water_plant(bad_list)


if __name__ == "__main__":
    my_list = ['tomato', 'lettuce', 'carrots']
    print("=== Garden Watering System ===")
    print()
    print("Testing normal watering...")
    water_plant(my_list)
    print()
    test_watering_system()
    print("Cleanup always happens, even with errors!")
