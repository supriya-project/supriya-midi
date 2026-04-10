#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/tuple.h>

#include <RtMidi.h>

#include <string>
#include <vector>

namespace nb = nanobind;
using namespace nb::literals;

void callback_function(double timeStamp, std::vector<unsigned char> *message, void *userData) {
//  {
//      nb::gil_scoped_acquire gil;
//      auto *callback = static_cast<nb::callable*>(userData);
//      (*callback)(message, timeStamp);
//  }
}

void error_callback_function(RtMidiError::Type type, const std::string &errorText, void *userData) {
  {
      nb::gil_scoped_acquire gil;
      auto *callback = static_cast<nb::callable*>(userData);
      (*callback)(type, errorText);
  }
}

// Module definition

NB_MODULE(_midi, m) {
    m.doc() = "RtMidi bindings";
    nb::enum_<RtMidi::Api>(m, "RtMidiAPI", nb::is_arithmetic())
        .value("UNSPECIFIED", RtMidi::UNSPECIFIED)
        .value("MACOSX_CORE", RtMidi::MACOSX_CORE)
        .value("LINUX_ALSA", RtMidi::LINUX_ALSA)
        .value("UNIX_JACK", RtMidi::UNIX_JACK)
        .value("WINDOWS_MM", RtMidi::WINDOWS_MM)
        .value("WEB_MIDI", RtMidi::WEB_MIDI_API)
        .value("RTMIDI_DUMMY", RtMidi::RTMIDI_DUMMY)
        ;
    nb::enum_<RtMidiError::Type>(m, "RtMidiErrorType")
        .value("WARNING", RtMidiError::WARNING)
        .value("DEBUG_WARNING", RtMidiError::DEBUG_WARNING)
        .value("UNSPECIFIED", RtMidiError::UNSPECIFIED)
        .value("NO_DEVICES_FOUND", RtMidiError::NO_DEVICES_FOUND)
        .value("INVALID_DEVICE", RtMidiError::INVALID_DEVICE)
        .value("MEMORY_ERROR", RtMidiError::MEMORY_ERROR)
        .value("INVALID_PARAMETER", RtMidiError::INVALID_PARAMETER)
        .value("INVALID_USE", RtMidiError::INVALID_USE)
        .value("DRIVER_ERROR", RtMidiError::DRIVER_ERROR)
        .value("SYSTEM_ERROR", RtMidiError::SYSTEM_ERROR)
        .value("THREAD_ERROR", RtMidiError::THREAD_ERROR)
        ;
    nb::class_<RtMidi>(m, "RtMidi")
        .def_static("get_api_display_name", &RtMidi::getApiDisplayName, nb::arg("api"))
        .def_static("get_api_name", &RtMidi::getApiName, nb::arg("api"))
        .def_static("get_compiled_api", [](){ std::vector<RtMidi::Api> apis; RtMidi::getCompiledApi(apis); return apis; })
        .def_static("get_compiled_api_by_name", &RtMidi::getCompiledApiByName, nb::arg("name"))
        .def_static("get_version", &RtMidi::getVersion)
        .def("close_port", &RtMidi::closePort)
        .def("get_port_count", &RtMidi::getPortCount)
        .def("get_port_name", &RtMidi::getPortName, nb::arg("port_number") = 0)
        .def("open_port", &RtMidi::openPort, nb::arg("port_number") = 0, nb::arg("port_name") = "RtMidi")
        .def("open_virtual_port", &RtMidi::openVirtualPort, nb::arg("port_name") = "RtMidi")
        .def("set_client_name", &RtMidi::setClientName, nb::arg("client_name"))
        .def("set_error_callback", [](RtMidi &self, nb::callable callback) { self.setErrorCallback(&error_callback_function, &callback); }, nb::arg("callback"))
        .def("set_port_name", &RtMidi::setPortName, nb::arg("port_name"))
        ;
    nb::class_<RtMidiIn, RtMidi>(m, "RtMidiIn")
        .def(nb::init<RtMidi::Api, const std::string&, unsigned int>(), nb::arg("api") = RtMidi::Api::UNSPECIFIED, nb::arg("client_name") = "RtMidi Input Client", nb::arg("queue_size_limit") = 1024)
        .def("cancel_callback", &RtMidiIn::cancelCallback)
        .def("get_current_api", &RtMidiIn::getCurrentApi)
        .def("get_message", [](RtMidiIn &self) { std::vector<unsigned char> message; double timeStamp = self.getMessage(&message); return std::make_tuple(message, timeStamp); })
        .def("ignore_types", &RtMidiIn::ignoreTypes, nb::arg("sysex") = true, nb::arg("timing") = true, nb::arg("active_sense") = true)
        .def("set_buffer_size", &RtMidiIn::setBufferSize, nb::arg("size") = 1024, nb::arg("count") = 4)
        .def("set_callback", [](RtMidiIn &self, nb::callable callback) { self.setCallback(&callback_function, &callback); });
        ;
    nb::class_<RtMidiOut, RtMidi>(m, "RtMidiOut")
        .def(nb::init<RtMidi::Api, const std::string&>(), nb::arg("api") = RtMidi::Api::UNSPECIFIED, nb::arg("client_name") = "RtMidi Output Client")
        .def("get_current_api", &RtMidiOut::getCurrentApi)
        .def("send_message", nb::overload_cast<const std::vector<unsigned char>*>(&RtMidiOut::sendMessage), nb::arg("message"))
        ;
}
