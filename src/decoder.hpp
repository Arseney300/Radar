#ifndef decorder_hpp
#define decorder_hpp

#include <data.hpp>
#include <utility>
#define _USE_MATH_DEFINES
#include <math.h>
#include <cmath>
//#pragma STDC FENV_ACCESS ON
namespace radar{

/// a bit of python code:
/*
        angleraw = (lineHeader[9]&0xff)<<8 | (lineHeader[8]&0xff)
        # rr = lineHeader[23]&0xff
        # sstt = (lineHeader[13]&0xff)<<8|(lineHeader[12]&0xff)
        # meter = sstt*10/math.sqrt(2)
        angle=angleraw*360/4096 - 90
*/

#pragma message("todo: move types to external file")

/// @brief angle in degree type
using angleDegT = double;

/// @brief coordinates type
/// coordinates is pair of two values:
///     radsin (for y)
///     radcos (for x)
using coordinatesT = std::pair<long double, long double>;


/// @brief get raw angle value from line header
/// @param[in] header 
/// @return uint raw value of angle
unsigned int GetRawAngle(const LineHeader& header);

/// @brief Calc angle in degrees
/// @param[in] rawangle 
/// @return angleDegT angle in radians
angleDegT CalcAngle(unsigned int rawangle);

/// @brief calc coordinates
/// @param angle 
/// @return coordinatesT
coordinatesT CalcCoordinates(const angleDegT& angle );

}; //!radar
#endif