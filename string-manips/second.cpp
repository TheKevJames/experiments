#include <iostream>
#include <string>

int main() {
    std::string arg = "";
    std::string vowels = "aeiou";

    for (;;) {
        std::cout << "Enter a word: ";
        std::cin >> arg;

        bool dbl = false;
        for (int i = 0; i < arg.length(); i++) {
            char c = arg[i];
            if (vowels.find(c) != -1) {
                if (dbl == true) {
                    std::cout << c;
                    dbl = false;
                } else {
                    dbl = true;
                }
            }
            std::cout << c;
        }
        std::cout << std::endl;
    }

    return 0;
}
