# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_archive_creation.py                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/18 10:36:59 by ialmani           #+#    #+#             #
#    Updated: 2025/12/18 10:37:00 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

data = [
    '[ENTRY 001] New quantum algorithm discovered',
    '[ENTRY 002] Efficiency increased by 347%',
    '[ENTRY 003] Archived by Data Archivist trainee'
]


def write_txt():
    print("Initializing new storage unit: new_discovery.txt")
    file = open('new_discovery.txt', 'w')
    print("Storage unit created successfully...\n")
    print("Inscribing preservation data...")
    for name in data:
        file.write(name + '\n')
        print(name)
    file.close()
    print("\nData inscription complete. Storage unit sealed.")
    print(f"Archive '{file.name}' ready for long-term preservation.")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    write_txt()
