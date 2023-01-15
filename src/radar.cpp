/// @file radar.cpp
/// @brief radar connection and control implementation
#include <iostream>

#include <radar.hpp>
#include <def.hpp>
#include <reg.hpp>
#include <util.hpp>
using namespace radar;

Radar::Radar() {
    LOG_DEBUG("Radar::Radar() start");
    LOG_DEBUG("init and connect sockets");
	// init endpoints
	control_endpoint_ = endpointT(boost::asio::ip::address::from_string(
        radar::defines::control_ip_address), 
        radar::defines::control_port);
	data_endpoint_ = endpointT(boost::asio::ip::address::from_string(
        radar::defines::data_ip_address),
        radar::defines::data_port);

	// init sockets 
	control_socket_ = std::make_shared<socketT>(ios_, control_endpoint_.protocol());
	data_socket_ = std::make_shared<socketT>(ios_, data_endpoint_.protocol());

	// connect sockets
	control_socket_->connect(control_endpoint_);
	data_socket_->connect(data_endpoint_);

    LOG_DEBUG("Radar::Radar() end");
}


packageT Radar::MakePackage(char reg, const std::vector<uint8_t>& data){
    LOG_DEBUG("Radar::MakePackage start");
    packageT ret(2+data.size());
    ret.at(0) = reg;
    ret.at(1) = RAD_CHECKSUM;
    std::size_t ret_it{2};
    for(const auto&it: data){
        ret.at(ret_it) = it;
    }
    LOG_DEBUG("Radar::MakePackage end");
    return ret;
}

void Radar::RadarTurnOn() {
    LOG_DEBUG("Radar::RadarTurnOn start");
	const packageT first_package = MakePackage(RAD_TURN_ON_OFF_0, {0x01} );
    const packageT second_package = MakePackage(RAD_TURN_ON_OFF_1, {0x01} );

    control_socket_->send_to(boost::asio::buffer(first_package), control_endpoint_);
    control_socket_->send_to(boost::asio::buffer(second_package), control_endpoint_);

    state_ = State::ACTIVE;
    LOG_DEBUG("Radar::RadarTurnOn end");
}

void Radar::RadarTurnOff() {
    LOG_DEBUG("Radar::RadarTurnOff start");
	const packageT first_package = MakePackage(RAD_TURN_ON_OFF_0, {0x00});
    const packageT second_package = MakePackage(RAD_TURN_ON_OFF_1, {0x00});

    control_socket_->send_to(boost::asio::buffer(first_package), control_endpoint_);
    control_socket_->send_to(boost::asio::buffer(second_package), control_endpoint_);
	state_ = State::NOT_ACTIVE;
    LOG_DEBUG("Radar::RadarTurnOff end");
}


void Radar::InitDefaultValues() {
    //take values from def.hpp and set in
}

void Radar::SetDistance()
{
    LOG_DEBUG("Radar::SetDistance start");
    const packageT package = MakePackage(RAD_ZOOMLEVEL, {0x98, 0x3A});

    control_socket_->send_to(boost::asio::buffer(package), control_endpoint_);
    LOG_DEBUG("Radar::SetDistance end");
}

void Radar::SetLocalInterferenceFilter()
{}

void Radar::SetScanSpeed()
{}

void Radar::SetTargetBoost()
{}

void Radar::SetInterferenceRejection()
{}

void Radar::SetAutomaticGain()
{}

void Radar::KeepAlive(){
    LOG_DEBUG("Radar::KeepAlive start");
    const packageT package = MakePackage(RAD_KEEP_ALIVE, {0});
    control_socket_->send_to(boost::asio::buffer(package), control_endpoint_);
    LOG_DEBUG("Radar::KeepAlive end");
}

Radar::State Radar::GetState() {
	return state_;
}

Radar::~Radar() {
    LOG_DEBUG("Radar:~Radar start");
    RadarTurnOff();
    LOG_DEBUG("Radar:~Radar end");
}


Data Radar::GetData(){
    LOG_DEBUG("Radar::GetData() start");
    char buffer[defines::data_size];
    std::size_t bytes_recieved = data_socket_->receive_from(boost::asio::buffer(buffer), data_endpoint_);
    if(bytes_recieved != radar::defines::data_size){
        LOG_ERR("get less bytes than %u : %ld", defines::data_size, bytes_recieved);
    }
    LOG_DEBUG("Radar::GetData() end");
    return Data{buffer, defines::data_size};
}
