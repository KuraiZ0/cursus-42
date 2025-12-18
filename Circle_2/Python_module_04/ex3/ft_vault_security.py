# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_vault_security.py                               :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/18 11:35:59 by ialmani           #+#    #+#             #
#    Updated: 2025/12/18 11:36:00 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def secure_excrat():
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")
    print("SECURE EXTRACTION:\n")
    with open('classified_data.txt', 'r') as file:
        content = file.read()
    print(content)
    print()
    print("SECURE PRESERVATION:")
    with open('security_protocols.txt', 'w') as file:
        file.write("Data preserved")
    print(content)
    print("Vault automatically sealed upon completion\n")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    secure_excrat()
    print("All vault operations completed with maximum security.")
