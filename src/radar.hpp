/// @file radar.hpp
/// @brief radar connect and control header file

#ifndef radar_hpp
#define radar_hpp

#include <memory>

#include <boost/asio.hpp>

#include <reg.hpp>
#include <vector>
#include <data.hpp>

namespace radar{

/// @brief  packageT
using packageT = std::vector<uint8_t>;

class Radar {
public:
	enum State{
		NOT_ACTIVE = 0,
		ACTIVE = 1,
	};
private:
	using socketT = boost::asio::ip::udp::socket;
	using endpointT = boost::asio::ip::udp::endpoint;
private:
    // Make Package
    // @param[in] reg - control register of radar
    // @param[in] std::vector<char> - data 
    // @return packageT - package with 
    packageT MakePackage(char reg, const std::vector<uint8_t>& data);
public:
	// Radar constructor
	// Connect to radar and setup default settings
	Radar();

    // Radar destructor
    // disconnect radar
    ~Radar();

	// Radar Turn On
	void RadarTurnOn();

	// Radar Turn Off
	void RadarTurnOff();

    // Init Default Values
    void InitDefaultValues();

	// Set Distance
	void SetDistance();

	// Set Local Interference Filter
	// TODO: ?????
	void SetLocalInterferenceFilter();

	// Set Scan Speed
	// TODO: ??????
	void SetScanSpeed();

	// Set Target Boost
	// TODO: ??????
	void SetTargetBoost();

	// Set Interference Rejection
	// TODO: ??????
	void SetInterferenceRejection();

	// Set Automatic Gain
	// TODO: ??????
	void SetAutomaticGain();

	// Keep radar alive
	// !!! We must to do it, because otherwise radar will turn off itself
	void KeepAlive();

	// Get state of Radar
	// @return State of radar
	State GetState();

	// Wait and get Data from Radar
	// @return data
	Data GetData(); 

private:
	boost::asio::io_service ios_; //< main input-output service
	endpointT control_endpoint_; //< endpoitn for control radar socket
	std::shared_ptr<socketT> control_socket_; //< socket for control radar
	endpointT data_endpoint_; //< endpoint for data socket
	std::shared_ptr<socketT> data_socket_; //< socket for getting data
	State state_; //< state of radar
};

} //namespace radar
#endif