/// @file data.hpp
/// @brief main data package
///
#ifndef data_hpp
#define data_hpp

#include <array>
#include <cstdint>

#include <def.hpp>

namespace radar{

/// @brief Main Data class
/// as i read from python sources, data is 65536 bytes array
/// data contains
/// 8 bytes: one FrameHeader
/// and Lines
/// one line:
/// 24 bytes: LineHeader
/// 512 bytes: LineData
class Data{
public:
    /// @brief Data constructor
    Data() = default;

    /// @brief Get size of data
    /// @return std::size_t size of data
    constexpr std::size_t GetSize(){
        return data_.size();
    }

    /// @brief Get access to std::array
    /// @return link on the data_ array
    constexpr auto& GetArray(){
        return data_;
    }

private:
    std::array<uint8_t, defines::data_size> data_; //< data array
};

} // namespace radar
#endif