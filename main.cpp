#include <boost/hana.hpp>
#include <iostream>
#include <string>

namespace hana = boost::hana;

// Define a struct with introspection
struct Person {
  BOOST_HANA_DEFINE_STRUCT(Person,
    (std::string, name),
    (int, age),
    (char, type)
  );
};

auto serialize = [](std::ostream& os, auto const& object) {
  hana::for_each(object, hana::fuse([&](auto member, auto value) {
        os << hana::to<char const*>(member) << " = " << value << "\n";
    }));
};

int main() {
  // Create an object of the struct
  Person john{"John", 30, 'm'};
  serialize(std::cout, john);
}
