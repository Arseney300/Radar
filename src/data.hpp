/// @file data.hpp
/// @brief main data package
///
#ifndef data_hpp
#define data_hpp

#include <array>
#include <cstdint>
#include <vector>

#include <def.hpp>
#include <util.hpp>
namespace radar{

/// @brief Frame Header class
/// at this moment, FrameHeader isn't using in the program
/// contains 8 bytes
class FrameHeader{
public:

    /// @brief default constructor
    FrameHeader() = default;

    /// @brief Constructor
    /// @param[in] rawdata ref on rawdata
    /// FrameHeader haven't shift
    template <typename T>
    FrameHeader(const T& rawdata){
        LOG_DEBUG("FrameHeader constructor start");
        for(std::size_t i = 0; i < data_.size(); i++){
            data_[i] = rawdata[i];
        }
        LOG_DEBUG("FrameHeader constructor end");
    };

    /// @brief Get access to data
    /// @return reference on data of FrameHeader
    constexpr const auto& Get(){
        return data_;
    }
    
private:
#pragma message("move 8 bytes of data_ size in FrameHeader to defines")
    std::array<uint8_t, 8> data_; //<data array
};

/// @brief Line Header class
/// contains 24 bytes
class LineHeader{
public:

    /// @brief default constructor
    LineHeader() = default;

    /// @brief Constructor
    /// @param[in] rawdata ref on rawdata
    /// @param[in] shift shift value
    template<typename T_SHIFT = std::size_t, typename T>
    LineHeader(const T& rawdata, T_SHIFT shift){
        LOG_DEBUG("LineHeader constructor start");
        std::size_t i = shift;
        for(std::size_t data_it = 0; i < shift+24; i++, data_it++){
            data_[data_it] = rawdata[i];
        }
        LOG_DEBUG("LineHeader constructor end");
    }

    /// @brief Get access to data
    /// @return reference on data of LineHeader
    constexpr const auto& Get() const{
        return data_;
    }
private:
#pragma message("move 24 bytes of data_ size in LineHeader to defines")
    std::array<uint8_t, 24> data_;
};


/// @brief Line Data class
/// contains 512 bytes
class LineData{
public:

    /// @brief default constructor
    LineData() = default;

    /// @brief Constructor
    /// @param[in] rawdata ref on rawdata
    /// @param[in] shift shift value
    template<typename T_SHIFT = std::size_t, typename T>
    LineData(const T& rawdata, T_SHIFT shift){
        LOG_DEBUG("LineData constructor start");
        std::size_t i = shift;
        for(std::size_t data_it = 0; i < shift+512; i++, data_it++){
            data_[data_it] = rawdata[i];
        }
        LOG_DEBUG("LineData constructor end");
    }

    /// @brief Get access to data
    /// @return reference on data of LineData
    constexpr const auto& Get() const{
        return data_;
    }
private:
#pragma message("move 512 bytes of data_ size in LineData to defines")
    std::array<uint8_t, 512> data_; //< data
};

/// @brief Line class
/// contaits LineHeader and LineData
class Line{
public:

    /// @brief default constructor
    Line() = default;

    /// @brief Constructor
    /// @param[in] rawdata ref on rawdata
    /// @param[in] shift shift value
    template<typename T_SHIFT = std::size_t, typename T>
    Line(const T& rawdata, T_SHIFT shift){
        LOG_DEBUG("Line constructor start");
        std::size_t shift_ = shift;
        header_ = LineHeader{rawdata, shift_};
        shift_+=24;
        data_ = LineData{rawdata, shift_};
        LOG_DEBUG("Line constructor end");
    }

    /// @brief Get header of line
    /// @return ref on header
    constexpr const auto& GetHeader() const{
        return header_;
    }

    /// @brief Get data on file
    /// @return ref on data
    constexpr const auto& GetData() const{
        return data_;
    }
private:
    LineHeader header_; //< header
    LineData data_; //< data
};

/// @brief Main Data class
/// have one frame header
/// and a lot of lines, each line have one header and one data
class Data{
public:

    /// @brief defaulct constructor
    Data() = default;

    /// @brief Data Constructor
    /// @param[in] rawdata ref on rawdata
    template <typename T>
    Data(const T& rawdata, std::size_t data_size)
    {
        LOG_DEBUG("Data constructor start");
        std::size_t shift{0};
        //frameHeader_ = FrameHeader{rawdata};
        shift+=8; // size of FrameHeader
        while(shift <= data_size){
            lines_.push_back(Line{rawdata, shift});
            shift+=(24+512);
        }
        LOG_DEBUG("Data constructor end");
    }

    auto begin(){
        return std::begin(lines_);
    }
    
    auto end(){
        return std::end(lines_);
    }

    const auto cbegin(){
        return std::cbegin(lines_);
    }

    const auto cend(){
        return std::cend(lines_);
    }
private:
    FrameHeader frameHeader_; //<frame header
#pragma message("maybe: calc and add specific size of lines")
#pragma message("32")
    std::vector<Line> lines_; //< lines
};

} // namespace radar
#endif