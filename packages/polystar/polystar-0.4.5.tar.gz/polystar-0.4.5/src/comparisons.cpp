/* This file is part of polystar.

Copyright © 2020 Greg Tucker <greg.tucker@stfc.ac.uk>

polystar is free software: you can redistribute it and/or modify it under the
terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

polystar is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with polystar. If not, see <https://www.gnu.org/licenses/>.            */

#include <string>
#include "comparisons.hpp"

/* \brief Produce a std::string representation of an enumerated comparison

\param c A polystar::cmp enumerated value
\return A string representation of c
*/
template<>
std::string polystar::to_string<polystar::cmp>(const polystar::cmp& c){
  using namespace polystar;
  std::string repr;
  switch(c)
  {
  case cmp::lt:    repr = "<";     break;
  case cmp::gt:    repr = ">";     break;
  case cmp::le:    repr = "<=";    break;
  case cmp::ge:    repr = ">=";    break;
  case cmp::eq:    repr = "==";    break;
  case cmp::nle:   repr = "!<=";   break;
  case cmp::nge:   repr = "!>=";   break;
  case cmp::neq:   repr = "!=";    break;
  case cmp::le_ge: repr = "<=|>="; break;
  default: repr = "unknown comparator";
  }
  return repr;
}

/* \brief Produce a std::string representation of an enumerated operation

\param o A polystar::ops enumerated value
\return A string representation of o
*/
template<>
std::string polystar::to_string<polystar::ops>(const polystar::ops& o){
  using namespace polystar;
  std::string repr;
  switch(o)
  {
  case ops::plus:  repr = "+";  break;
  case ops::minus: repr = "-";  break;
  case ops::times: repr = "*";  break;
  case ops::rdiv:  repr = "/";  break;
  case ops::ldiv:  repr = "\\"; break;
  default: repr = "unknown operator";
  }
  return repr;
}
