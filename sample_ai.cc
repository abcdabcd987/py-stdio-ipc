#include <ctime>
#include <cstdlib>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

struct Result {
    int id, say, hand;
    Result(int _id, int _say, int _hand): id(_id), say(_say), hand(_hand) {}
};
inline void end() {
    std::cout << "END\n" << std::flush;
}

std::vector<Result> history;
int myid;

int main(int argc, char** argv) {
    // if the judge gives a seed, then use it
    if (argc == 2) {
        unsigned given_seed = 0;
        for (char *pc = argv[1]; *pc; ++pc)
            given_seed = given_seed*10 + (*pc - '0');
        srand(given_seed);
        std::cerr << "given seed = " << given_seed << std::endl;
    } else {
        srand(static_cast<unsigned>(time(0)));
    }

    std::string op;
    for (;;) {
        int id, say, hand;
        std::cin >> op;               // read an operation

        if (op == "message") {        // history
            std::cin >> id >> say >> hand;
            history.push_back(Result(id, say, hand));

        } else if (op == "action") {  // make a decision
            hand = rand() % 6;
            say = rand()%(10-hand)+hand;
            std::cout << say << " " << hand << std::endl;
            end(); // remember to end the response with "END\n"
                   // and remember to flush

        } else if (op == "id") {      // get my id
            std::cin >> myid;

        } else if (op == "endgame") { // good game
            break;
        }
    }
}