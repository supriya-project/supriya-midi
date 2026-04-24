#include <string>
#include <vector>

#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/tuple.h>

#include <RtMidi.h>

namespace nb = nanobind;
using namespace nb::literals;

struct CallbackHandle {
    nb::handle callback;
    nb::handle data;

    ~CallbackHandle() {
        ~callback;
        ~data;
    }
};


void callback_function(double timeStamp, std::vector<unsigned char> *message, void *userData) {
    nb::gil_scoped_acquire gil;
    auto* handle = static_cast<CallbackHandle*>(userData);
    try {
        nb::borrow<nb::callable>(handle->callback)(message, timeStamp, nb::borrow(handle->data));
    } catch (nb::python_error &e) {
        e.discard_as_unraisable(__func__);
    }
}

void error_callback_function(RtMidiError::Type type, const std::string &errorText, void *userData) {
    nb::gil_scoped_acquire gil;
    auto* handle = static_cast<CallbackHandle*>(userData);
    nb::borrow<nb::callable>(handle->callback)(type, errorText, nb::borrow(handle->data));
}

// Module definition

NB_MODULE(rtmidi_ext, m) {
    m.doc() = R"pbdoc(
        Low-level Python/RtMidi bindings.

        ..  note:: 

            Please use the higher-level classes defined in :py:mod:`supriya_midi.core` instead.
    )pbdoc";
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
        .def(
            "set_error_callback",
            [](RtMidi &self, nb::callable callback, nb::object data) {
                auto* handle = new CallbackHandle();
                handle->callback = nb::handle(callback);
                handle->data = nb::handle(data);
                self.setErrorCallback(&error_callback_function, handle);
            },
            nb::arg("callback"), nb::arg("data") = nb::none()
        )
        .def("set_port_name", &RtMidi::setPortName, nb::arg("port_name"))
        ;
    nb::class_<RtMidiIn, RtMidi>(m, "RtMidiIn")
        .def(nb::init<RtMidi::Api, const std::string&, unsigned int>(), nb::arg("api") = RtMidi::Api::UNSPECIFIED, nb::arg("client_name") = "RtMidi Input Client", nb::arg("queue_size_limit") = 1024)
        .def("cancel_callback", &RtMidiIn::cancelCallback)
        .def("get_current_api", &RtMidiIn::getCurrentApi)
        .def("get_message", [](RtMidiIn &self) { std::vector<unsigned char> message; double timeStamp = self.getMessage(&message); return std::make_tuple(message, timeStamp); })
        .def("ignore_types", &RtMidiIn::ignoreTypes, nb::arg("sysex") = true, nb::arg("timing") = true, nb::arg("active_sense") = true)
        .def("set_buffer_size", &RtMidiIn::setBufferSize, nb::arg("size") = 1024, nb::arg("count") = 4)
        .def(
            "set_callback",
            [](RtMidiIn &self, nb::callable callback, nb::object data) {
                auto* handle = new CallbackHandle();
                handle->callback = nb::handle(callback);
                handle->data = nb::handle(data);
                self.setCallback(&callback_function, handle);
            },
            nb::arg("callback"), nb::arg("data") = nb::none()
        );
        ;
    nb::class_<RtMidiOut, RtMidi>(m, "RtMidiOut")
        .def(nb::init<RtMidi::Api, const std::string&>(), nb::arg("api") = RtMidi::Api::UNSPECIFIED, nb::arg("client_name") = "RtMidi Output Client")
        .def("get_current_api", &RtMidiOut::getCurrentApi)
        .def("send_message", nb::overload_cast<const std::vector<unsigned char>*>(&RtMidiOut::sendMessage), nb::arg("message"))
        ;
}
