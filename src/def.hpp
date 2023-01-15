/// @file def.hpp
/// @brief main defines of radar

#ifndef def_hpp
#define def_hpp

#include <string>

namespace radar{
namespace defines{

const uint data_size = 17160; //< size of data package

const std::string control_ip_address = "236.6.7.10"; //< control ip address
const uint control_port = 6680; //< control port

const std::string data_ip_address = "236.6.7.8" ; //< data ip address
const uint data_port = 6678; //< data port
} 
}
#endif