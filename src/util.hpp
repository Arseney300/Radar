#ifndef util_hpp
#define util_hpp

#pragma message("TODO: remove timed debug installing")
// timed:
#define RADAR_DEBUG
#define RADAR_LOG_LEVEL 0x03

#ifdef RADAR_DEBUG
#define NO_LOG          0x00
#define ERROR_LEVEL     0x01
#define INFO_LEVEL      0x02
#define DEBUG_LEVEL     0x03

#ifndef LOG_LEVEL
#define LOG_LEVEL NO_LOG
#endif

#if RADAR_LOG_LEVEL >= DEBUG_LEVEL
#define LOG_DEBUG(format, args...) fprintf(stdout, format"\n", ## args)
#else
#define LOG_DEBUG(format, ...)
#endif

#if RADAR_LOG_LEVEL >= INFO_LEVEL
#define LOG_INFO(format, args...) fprintf(stdout, format"\n", ## args)
#else
#define LOG_INFO(format, ...)
#endif

#if RADAR_LOG_LEVEL >= ERROR_LEVEL
#define LOG_ERR(format, args...) fprintf(stderr, format"\n", ## args)
#else
#define LOG_ERR(format, ...)
#endif

#endif //!DEBUG

#endif //!util_hpp