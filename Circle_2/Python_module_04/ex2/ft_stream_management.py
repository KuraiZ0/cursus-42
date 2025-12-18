# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_stream_management.py                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/18 10:57:54 by ialmani           #+#    #+#             #
#    Updated: 2025/12/18 10:57:55 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#
import sys


def diagnostic(id, status_rep):
    sys.stdout.write(f"[STANDARD] Archive status from {id}: {status_rep}\n")
    sys.stderr.write("[ALERT] System diagnostic:"
                     " Communication channels verified\n")
    sys.stdout.write("[STANDARD] Data transmission complete\n")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
    archiv_id = input("Input Stream active. Enter archivist ID: ")
    status_rep = input("Input Stream active. Enter status report: ")
    print()
    diagnostic(archiv_id, status_rep)
    print("\nThree-channel communication test successful.")
