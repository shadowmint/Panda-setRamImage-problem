cmake_minimum_required (VERSION 2.6)
project (AR)

# CMake package modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")

# Collect source files
file(GLOB_RECURSE SOURCES src/*.c)

# Code type
set(CMAKE_C_FLAGS "-std=c99")
set (CMAKE_OSX_ARCHITECTURES "i386")

# Debug mode?
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -pedantic -Wimplicit-function-declaration -Wreturn-type -Wstrict-prototypes -Wextra -g")

# Deps: self
set(INCLUDE_DIRS "${PROJECT_SOURCE_DIR}/include")

# Build library
add_library (ar SHARED ${SOURCES})
include_directories(${INCLUDE_DIRS})
target_link_libraries(ar ${EXTRA_LIBRARIES})

# Export
get_property(ar_location TARGET ar PROPERTY LOCATION)
set(LIBRARIES "${ar_location};${EXTRA_LIBRARIES}")
configure_file(arConfig.cmake.in "${CMAKE_BINARY_DIR}/arConfig.cmake")
message("Located library in: " + ${ar_location})

# Export for python tests
configure_file(pyar.py.in "${PROJECT_SOURCE_DIR}/lib/pyar/lib.py")

# Collect test files
file(GLOB_RECURSE TEST_PROJECTS tests/CMakeLists*)
if(TEST_PROJECTS)
  enable_testing()
  foreach(TEST ${TEST_PROJECTS})
    string(REGEX REPLACE "CMakeLists.txt" "" TEST_DIR ${TEST})
    add_subdirectory(${TEST_DIR})
  endforeach(TEST)
endif(TEST_PROJECTS)
