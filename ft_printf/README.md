🧩 ft_printf

Recreation of the standard printf() function — a 42 school project.

⸻

🧠 Purpose

Reproduce the behavior of the original printf() function while following the strict 42 project requirements.

This project aims to teach:
	•	Handling variadic functions (<stdarg.h>)
	•	Formatting and printing various data types
	•	Building a clean, modular, and reusable static library (.a)

⸻

⚙️ Allowed Functions
	•	write
	•	malloc
	•	free
	•	va_start, va_arg, va_end

⸻

🧩 Supported Conversions

Specifier	Description
%c	Character
%s	String
%p	Pointer (memory address in hexadecimal)
%d / %i	Signed integer
%u	Unsigned integer
%x	Hexadecimal lowercase
%X	Hexadecimal uppercase
%%	Prints the percent symbol


⸻

🧱 Project Structure

ft_printf/
│
├── ft_printf.c
├── print_func.c
├── print_func2.c
├── ft_printf.h
├── libft/
│   ├── (your libft reused here)
│   └── ...
├── Makefile
└── main.c (for testing)


⸻

🛠️ Compilation

Build the library:

make

Clean object files:

make clean

Rebuild everything:

make re


⸻

🚀 Usage

You can include ft_printf in your own project like this:

#include "ft_printf.h"

int main(void)
{
    int count;

    count = ft_printf("Hello %s! Number: %d, Hex: %x\n", "world", 42, 255);
    ft_printf("Printed characters: %d\n", count);
    return (0);
}

Compile a test file:

cc main.c libftprintf.a -o test
./test


⸻

🧾 Example Output

printf : A Hello 42! -42 -42 424242 67932 67932 0x16fceb254 %
ft_printf : A Hello 42! -42 -42 424242 67932 67932 0x16fceb254 %
printf return = 62
ft_printf return = 62


⸻

🧑‍💻 Author

👤 Ilias Almani
📧 iliasalmani@student.42.fr
🏫 42 School — Class of 2025
🦊 GitHub: KuraiZ0

⸻

⭐️ Bonus (Optional)
	•	Support for flags (+, #,  , 0, -)
	•	Width / precision handling
	•	Color output 🌈 (for fun, not part of the official subject)

⸻

🧩 Notes

Project made following the 42 Norm:
	•	No for, do while, switch, goto
	•	No global variables
	•	100% Norminette compliant ✅

⸻

🏁 Evaluation Goals

✅ Compiles without errors or warnings
✅ Identical behavior to the real printf
✅ Correct handling of all required conversions
✅ Accurate return value (character count)

⸻

💬 Pro Tip

“Once you finish ft_printf, you basically understand half of C.” — every 42 student ever 😎
