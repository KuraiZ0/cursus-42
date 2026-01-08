# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_crisis_response.py                              :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/18 12:02:12 by ialmani           #+#    #+#             #
#    Updated: 2025/12/18 12:02:13 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def crisis_alert(file_name):
    """ Trying to access to a file and display errors if crisis occured"""
    try:
        print(f"CRISIS ALERT: Attempting access to '{file_name}'...")
        with open(file_name, 'r') as file:
            file.read()
        print("SUCCESS: Archive recovered - Knowledge preserved for humanity ")
        print("STATUS: Normal operations resumed")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintened")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
    crisis_alert('lost_archive.txt')
    print()
    crisis_alert('protected_file.txt')
    print()
    crisis_alert('standard_archive.txt')
    print("All crisis scenarios handled successfully. Archives secure.")
