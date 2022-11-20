/// @file main.cpp
/// @brief main file with main loop
#include <iostream>
#include <thread>

#include <radar.hpp>

using namespace radar;

enum Status{
    Ok = 0,
    Exception = 1,
    InvalidException = 2,
}

/// @brief  main function with main loop
/// @return status code
int main(){
    bool stopFlag = false;
    try{
        Radar radar;
        radar.RadarTurnOn();
        radar.InitDefaultValues();
        while(!stopFlag){
            Data data = radar.GetData();
            // processing data
            // drawing data
            radar.KeepAlive();
        }
    }
    catch (const std::exception& e){
        std::cerr << e.what() << std::endl;
        return Status::Exception;
    }
    catch( ... ){
        std::cerr << "catch unknown exception" << std::endl;
        return Status::InvalidException;
    }

}