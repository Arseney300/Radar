#include <decoder.hpp>
#include <util.hpp>
namespace radar{

unsigned int GetRawAngle(const LineHeader& header){
    uint8_t first = header.Get().at(9);
    uint8_t second = header.Get().at(8);
    
    unsigned int value = ( first << 8 ) | second;
    LOG_DEBUG("GetRawAngle: first(9 byte in header) hex value: %02X, second(8 byte in header) hex value: %02X, result: %u", first, second, value);
    return value; 
}

angleDegT CalcAngle(unsigned int rawangle){
    angleDegT angle = rawangle*360/4096 - 90;
    return angle;
}

namespace{
    long double DegreeToRad(double degree)
    {
        return (long double)(degree * (M_PIl / 180));
    }
}

coordinatesT CalcCoordinates(const angleDegT& angle ){
    long double rad = DegreeToRad(angle);
    return {std::cos(rad),std::sin(rad)};
}

}