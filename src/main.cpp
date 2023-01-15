/// @file main.cpp
/// @brief main file with main loop
#include <iostream>
#include <thread>

#include <radar.hpp>
#include <data.hpp>
#include <decoder.hpp>
#include <util.hpp>
using namespace radar;

enum Status{
    Ok = 0,
    Exception = 1,
    InvalidException = 2,
};

/// @brief  main function with main loop
/// @return status code
int main(){
    LOG_INFO("start program");
    bool stopFlag = false;
    try{
        Radar radar;
        LOG_INFO("radar starting");
        radar.RadarTurnOn();
        LOG_INFO("radar start");
        LOG_INFO("init default values");
        radar.InitDefaultValues();
        LOG_INFO("start transmission");
        while(!stopFlag){
            LOG_DEBUG("start of main loop iteration");
            Data data = radar.GetData();
            // processing data
            for(const auto&i: data){
                angleDegT angleDeg = CalcAngle(GetRawAngle(i.GetHeader()));
                coordinatesT coor = CalcCoordinates(angleDeg);

                // drawing data
                // atm haven't drawing, just print values:

                std::cout << "radcos: " << coor.first << " radsin: " << coor.second << std::endl;
            }

            radar.KeepAlive();
            LOG_DEBUG("end of main loop iteration");
        }
        LOG_INFO("Radar stop");
    }
    catch (const std::exception& e){
        LOG_ERR("get exception: %s", e.what());
        return Status::Exception;
    }
    catch( ... ){
        LOG_ERR("catch unknown exception");
        return Status::InvalidException;
    }
}