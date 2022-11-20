/// @file radar.cpp
/// @brief radar connection and control implementation
#include <iostream>

#include <radar.hpp>
#include <def.hpp>
#include <reg.hpp>

using namespace radar;

Radar::Radar() {
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

    std::cout << "init and connect sockets" << std::endl;;
}


packageT Radar::MakePackage(char reg, const std::vector<uint8_t>& data){
    packageT ret(2+data.size());
    ret.at(0) = reg;
    ret.at(1) = RAD_CHECKSUM;
    std::size_t ret_it{2};
    for(const auto&it: data){
        ret.at(ret_it) = it;
    }
    return std::move(ret);
}

void Radar::RadarTurnOn() {
	const packageT first_package = MakePackage(RAD_TURN_ON_OFF_0, {0x01} );
    const packageT second_package = MakePackage(RAD_TURN_ON_OFF_1, {0x01} );

    control_socket_->send_to(boost::asio::buffer(first_package), control_endpoint_);
    control_socket_->send_to(boost::asio::buffer(second_package), control_endpoint_);

    state_ = State::ACTIVE;
}

void Radar::RadarTurnOff() {
	const packageT first_package = MakePackage(RAD_TURN_ON_OFF_0, {0x00});
    const packageT second_package = MakePackage(RAD_TURN_ON_OFF_1, {0x00});

    control_socket_->send_to(boost::asio::buffer(first_package), control_endpoint_);
    control_socket_->send_to(boost::asio::buffer(second_package), control_endpoint_);
	state_ = State::NOT_ACTIVE;
}


void Radar::InitDefaultValues() {
    //take values from def.hpp and set in
}

void Radar::SetDistance()
{
    const packageT package = MakePackage(RAD_ZOOMLEVEL, {0x98, 0x3A});

    control_socket_->send_to(boost::asio::buffer(package), control_endpoint_);
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

void Radar::KeepAlive()
{}

Radar::State Radar::GetState() {
	return state_;
}

Radar::~Radar() {
    RadarTurnOff();
}


Data Radar::GetData(){
    Data data;
    std::size_t bytes_recieved = data_socket_->receive_from(boost::asio::buffer(data.GetArray()), data_endpoint_);
    if(bytes_recieved != radar::defines::data_size){
        std::cout << "get less bytes than 65536: " << bytes_recieved << std::endl;
    }
    return std::move(data);
}
