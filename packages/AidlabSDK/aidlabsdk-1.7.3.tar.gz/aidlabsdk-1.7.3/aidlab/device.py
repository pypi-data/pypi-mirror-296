"""
Created by Szymon Gesicki on 09.05.2020.
"""

import logging
import os
import sys
from ctypes import (CDLL, CFUNCTYPE, POINTER, Structure, c_bool, c_char,
                    c_char_p, c_float, c_int, c_uint8, c_uint16, c_uint32,
                    c_uint64, c_void_p, addressof, py_object, cdll)
from time import time
from typing import Dict, Tuple, Optional, List

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from packaging import version

from .body_position import BodyPosition
from .wear_state import WearState
from .data_type import DataType
from .activity_type import ActivityType

logger = logging.getLogger(__name__)

class AidlabSDKPointer(Structure):
    """AidlabSDK pointer"""

class Device:
    """
    The `Device` class is the main interface for interacting with an Aidlab or Aidmed One.

    This class provides methods for configuring the device and controlling its configuration. 

    It also stores basic information about the device, like its firmware version, serial number,
    hardware version, and MAC address.

    Attributes:
        firmware_revision (str): The firmware version of the device.
        hardware_revision (str): The hardware version of the device.
        serial_number (str): The serial number of the device.
        manufacturer_name (str): The name of the manufacturer of the device.
        address (str): The MAC address of the device.
    """

    name: str | None = None
    firmware_revision: str | None = None
    hardware_revision: str | None = None
    serial_number: str | None = None
    manufacturer_name: str | None = None
    address: str | None = None

    _aidlab_sdk_ptr = None

    _delegate = None

    _COMMAND_CHARACTERISTIC = "51366e80-cf3a-11e1-9ab4-0002a5d5c51b"

    sample_time_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float)
    activity_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint8)
    respiration_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint32)
    accelerometer_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    gyroscope_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    magnetometer_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    battery_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    steps_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint64)
    orientation_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_float, c_float, c_float)
    body_position_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint8)
    quaternion_callback_type = CFUNCTYPE(
        None, c_void_p, c_uint64, c_float, c_float, c_float, c_float)
    wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    heart_rate_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)
    rr_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)
    pressure_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)
    pressure_wear_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    sound_volume_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_uint16)
    exercise_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    received_command_callback_type = CFUNCTYPE(None, c_void_p)
    message_callback_type = CFUNCTYPE(None, c_void_p, c_char_p, c_char_p)
    sync_state_callback_type = CFUNCTYPE(None, c_void_p, c_uint8)
    unsynchronized_size_callback_type = CFUNCTYPE(None, c_void_p, c_uint32, c_float)
    user_event_callback_type = CFUNCTYPE(None, c_void_p, c_uint64)
    did_receive_error_callback_type = CFUNCTYPE(None, c_void_p, c_char_p)
    signal_quality_callback_type = CFUNCTYPE(None, c_void_p, c_uint64, c_int)

    Exercise = {
        0: "pushUp",
        1: "jump",
        2: "sitUp",
        3: "burpee",
        4: "pullUp",
        5: "squat",
        6: "plankStart",
        7: "plankEnd"
    }

    Sync_state = {
        0: "start",
        1: "end",
        2: "stop",
        3: "empty"
    }

    is_connected = False

    ecgFiltrationMethod = {"normal": False, "aggressive": True}

    lib: CDLL

    _device: BLEDevice
    _client: BleakClient
    _uuid_function_map: Dict[Tuple[str, int], callable] = {} # type: ignore

    def __init__(self, device: BLEDevice):

        self._device = device

        self.name = device.name
        self.address = device.address

        self.ecg_c_callback = self.sample_time_callback_type(
            self._ecg_callback)
        self.respiration_c_callback = self.sample_time_callback_type(
            self._respiration_callback)
        self.temperature_c_callback = self.sample_time_callback_type(
            self._temperature_callback)
        self.activity_c_callback = self.activity_callback_type(
            self._activity_callback)
        self.steps_c_callback = self.steps_callback_type(
            self._steps_callback)
        self.accelerometer_c_callback = self.accelerometer_callback_type(
            self._accelerometer_callback)
        self.gyroscope_c_callback = self.gyroscope_callback_type(
            self._gyroscope_callback)
        self.magnetometer_c_callback = self.magnetometer_callback_type(
            self._magnetometer_callback)
        self.quaternion_c_callback = self.quaternion_callback_type(
            self._quaternion_callback)
        self.orientation_c_callback = self.orientation_callback_type(
            self._orientation_callback)
        self.body_position_c_callback = self.body_position_callback_type(
            self._body_position_callback)
        self.heart_rate_c_callback = self.heart_rate_callback_type(
            self._heart_rate_callback)
        self.rr_c_callback = self.rr_callback_type(
            self._rr_callback)
        self.respiration_rate_c_callback = self.respiration_rate_callback_type(
            self._respiration_rate_callback)
        self.wear_state_c_callback = self.wear_state_callback_type(
            self._wear_state_did_change)
        self.sound_volume_c_callback = self.sound_volume_callback_type(
            self._sound_volume_callback)
        self.exercise_c_callback = self.exercise_callback_type(
            self._exercise_callback)
        self.receive_command_c_callback = self.received_command_callback_type(
            self._receive_command_callback)
        self.received_message_c_callback = self.message_callback_type(
            self._received_message_callback)
        self.pressure_c_callback = self.pressure_callback_type(
            self._pressure_callback)
        self.pressure_wear_state_c_callback = self.pressure_wear_state_callback_type(
            self._pressure_wear_state_did_change)
        self.user_event_c_callback = self.user_event_callback_type(
            self._user_event_callback)
        self.did_receive_error_c_callback = self.did_receive_error_callback_type(
            self._did_receive_error_callback)
        self.battery_c_callback = self.battery_callback_type(
            self._battery_callback)
        self.signal_quality_c_callback = self.signal_quality_callback_type(
            self._signal_quality_callback)

        self.sync_state_c_callback = self.sync_state_callback_type(
            self._sync_state_did_change)
        self.unsynchronized_size_c_callback = self.unsynchronized_size_callback_type(
            self._did_receive_unsynchronized_size)
        self._past_ecg_c_callback = self.sample_time_callback_type(
            self._past_ecg_callback)
        self._past_respiration_c_callback = self.sample_time_callback_type(
            self._past_respiration_callback)
        self._past_temperature_c_callback = self.sample_time_callback_type(
            self._past_temperature_callback)
        self._past_activity_c_callback = self.activity_callback_type(
            self._past_activity_callback)
        self._past_steps_c_callback = self.steps_callback_type(
            self._past_steps_callback)
        self._past_accelerometer_c_callback = self.accelerometer_callback_type(
            self._past_accelerometer_callback)
        self._past_gyroscope_c_callback = self.gyroscope_callback_type(
            self._past_gyroscope_callback)
        self._past_magnetometer_c_callback = self.magnetometer_callback_type(
            self._past_magnetometer_callback)
        self._past_quaternion_c_callback = self.quaternion_callback_type(
            self._past_quaternion_callback)
        self._past_orientation_c_callback = self.orientation_callback_type(
            self._past_orientation_callback)
        self._past_body_position_c_callback = self.body_position_callback_type(
            self._past_body_position_callback)
        self._past_heart_rate_c_callback = self.heart_rate_callback_type(
            self._past_heart_rate_callback)
        self._past_rr_c_callback = self.rr_callback_type(
            self._past_rr_callback)
        self._past_respiration_rate_c_callback = self.respiration_rate_callback_type(
            self._past_respiration_rate_callback)
        self._past_sound_volume_c_callback = self.sound_volume_callback_type(
            self._past_sound_volume_callback)
        self._past_pressure_c_callback = self.pressure_callback_type(
            self._past_pressure_callback)
        self._past_user_event_c_callback = self.user_event_callback_type(
            self._past_user_event_callback)
        self._past_signal_quality_c_callback = self.signal_quality_callback_type(
            self._past_signal_quality_callback)

    async def connect(self, delegate):
        """
        Connects to the device.
        """

        self._delegate = delegate

        self._client = BleakClient(self._device, disconnected_callback=self._did_disconnect)

        try:
            await self._client.connect(timeout=10)
        except TimeoutError:
            self._delegate.did_fail_to_connect(self, "TimeoutError")
            return

        self._create()

        # Harvest Device Information
        self.firmware_revision = (await self._client.read_gatt_char("00002a26-0000-1000-8000-00805f9b34fb")).decode('ascii')
        self._set_firmware_revision(self.firmware_revision)

        self.hardware_revision = (await self._client.read_gatt_char("00002a27-0000-1000-8000-00805f9b34fb")).decode('ascii')
        self._set_hardware_revision(self.hardware_revision)

        self.manufacturer_name = (await self._client.read_gatt_char("00002a29-0000-1000-8000-00805f9b34fb")).decode('ascii')
        self.serial_number = (await self._client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")).decode('ascii')

        self._uuid_function_map = {
            self._uuid(DataType.ECG): self._calculate_ecg,
            self._uuid(DataType.RESPIRATION): self._calculate_respiration,
            self._uuid(DataType.SKIN_TEMPERATURE): self._calculate_temperature,
            self._uuid(DataType.MOTION): self._calculate_motion,
            self._uuid(DataType.ACTIVITY): self._calculate_activity,
            self._uuid(DataType.ORIENTATION): self._calculate_orientation,
            self._uuid(DataType.STEPS): self._calculate_steps,
            self._uuid(DataType.HEART_RATE): self._calculate_heart_rate,
            self._uuid(DataType.SOUND_VOLUME): self._calculate_sound_volume,
            self._uuid(DataType.RR): self._calculate_heart_rate, # Same as HEART_RATE
        }

        await self.set_time(int(time()))
        
        # We always want to notify the command line
        await self._client.start_notify(self._COMMAND_CHARACTERISTIC, self._did_receive_raw_cmd_value)

        if version.parse(self.firmware_revision) >= version.parse("3.6.0"):
            await self._client.start_notify("00002a19-0000-1000-8000-00805f9b34fb", self._did_receive_state_of_charge)
        else:
            await self._client.start_notify("47366e80-cf3a-11e1-9ab4-0002a5d5c51b", self._did_receive_state_of_charge)


        self.is_connected = True
        await self._delegate.did_connect(self)

    async def disconnect(self):
        """
        Disconnect from the device.
        """
        await self._client.disconnect()

    async def collect(self, data_types: list[DataType], data_types_to_store: Optional[List[DataType]] = None):
        """Start collecting data from the device.
        """
        if version.parse(self.firmware_revision) >= version.parse("3.6.0"):
            await self._collect(data_types, data_types_to_store)
        else:
            await self._collect_legacy(data_types)

    async def start_synchronization(self):
        """Start sending data from internal memory.
        """
        await self.send("sync start")

    async def stop_synchronization(self):
        """Stop sending data from internal memory.
        """
        await self.send("sync stop")

    async def set_time(self, timestamp: int):
        """Sets the time on the device.
        """
        message = [b for b in timestamp.to_bytes(4, "little")]
        await self._client.write_gatt_char("00002a2b-0000-1000-8000-00805f9b34fb",
                                     bytearray(message), True)

    def set_ecg_filtration_method(self, method: str = "normal"):
        """
        Set ECG filtration method (e.g. to change LED brightness).
        
        This method provides you the flexibility to adjust the electrocardiogram (ECG) filtration to
        your specific needs. Depending on your specific use case, you might prefer a more aggressive
        filtration to reduce noise or a normal filtration to retain more details in the signal.
        """
        self.lib.AidlabSDK_set_aggressive_ecg_filtration(self.ecgFiltrationMethod.get(method, False),
                                            self._aidlab_sdk_ptr)

    async def send(self, command: str):
        """
        Sends a command to the device (e.g. to change LED brightness).
        """

        if version.parse(self.firmware_revision) < version.parse("3.6.0"):
            logger.error("Sending is supported since firmware 3.6.0")
            return

        write_value = self._get_command(command)
        size = write_value[3] | (write_value[4] << 8)
        message = [write_value[i] for i in range(size)]
        await self._send(message, size)

    def _create(self):
        self.lib = self._load_aidlab_sdk()

        # Setting up type of variables and return values
        self._setup_ctypes()

        self._aidlab_sdk_ptr = self.lib.AidlabSDK_create()

        instance_ptr = c_void_p(addressof(py_object(self)))

        self.lib.AidlabSDK_set_mtu(20, self._aidlab_sdk_ptr)

        self.lib.AidlabSDK_set_context(instance_ptr, self._aidlab_sdk_ptr)

        self.lib.AidlabSDK_init_callbacks(
            self.ecg_c_callback,
            self.respiration_c_callback,
            self.temperature_c_callback,
            self.accelerometer_c_callback,
            self.gyroscope_c_callback,
            self.magnetometer_c_callback,
            self.battery_c_callback,
            self.activity_c_callback,
            self.steps_c_callback,
            self.orientation_c_callback,
            self.quaternion_c_callback,
            self.respiration_rate_c_callback,
            self.wear_state_c_callback,
            self.heart_rate_c_callback,
            self.rr_c_callback,
            self.sound_volume_c_callback,
            self.exercise_c_callback,
            self.receive_command_c_callback,
            self.received_message_c_callback,
            self.user_event_c_callback,
            self.pressure_c_callback,
            self.pressure_wear_state_c_callback,
            self.body_position_c_callback,
            self.did_receive_error_c_callback,
            self.signal_quality_c_callback,
            self._aidlab_sdk_ptr)

        self.lib.AidlabSDK_init_synchronization_callbacks(
            self.sync_state_c_callback,
            self.unsynchronized_size_c_callback,
            self._past_ecg_c_callback,
            self._past_respiration_c_callback,
            self._past_temperature_c_callback,
            self._past_heart_rate_c_callback,
            self._past_rr_c_callback,
            self._past_activity_c_callback,
            self._past_respiration_rate_c_callback,
            self._past_steps_c_callback,
            self._past_user_event_c_callback,
            self._past_sound_volume_c_callback,
            self._past_pressure_c_callback,
            self._past_accelerometer_c_callback,
            self._past_gyroscope_c_callback,
            self._past_quaternion_c_callback,
            self._past_orientation_c_callback,
            self._past_magnetometer_c_callback,
            self._past_body_position_c_callback,
            self._past_rr_c_callback,
            self._past_accelerometer_c_callback,
            self._aidlab_sdk_ptr)

    async def _collect(self, data_types: list[DataType], data_types_to_store: list[DataType] | None):
        if data_types_to_store is None:
            data_types_to_store = []

        write_value = self._get_collect_command(
            [signal.value for signal in data_types],
            [signal.value for signal in data_types_to_store]
        )
        size = write_value[3] | (write_value[4] << 8)
        message = [write_value[i] for i in range(size)]
        await self._send(message, size)

    async def _collect_legacy(self, data_types: list[DataType]):

        # Remove unsupported data types in older firmware
        data_types = [data_type for data_type in data_types if data_type != DataType.PRESSURE]

        # Map data types to their respective UUIDs
        data_types_uuids = [self._uuid(data_type) for data_type in data_types]

        # Remove duplicates
        data_types_uuids = list(set(data_types_uuids))

        for data_type_uuid in data_types_uuids:
            await self._client.start_notify(data_type_uuid[0], self._handle_notification)

    def _calculate_temperature(self, data: bytearray):
        self.lib.processTemperaturePackage((c_uint8 * len(data))(*data),
                                           len(data), self._aidlab_sdk_ptr)

    def _calculate_respiration(self, data: bytearray):
        self.lib.processRespirationPackage((
            c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_ecg(self, data: bytearray):
        self.lib.processECGPackage((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _did_receive_state_of_charge(self, _: BleakGATTCharacteristic, data: bytearray):
        self.lib.AidlabSDK_process_battery_package((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_motion(self, data: bytearray):
        self.lib.processMotionPackage((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _calculate_activity(self, data: bytearray):
        self.lib.processActivityPackage((c_uint8 * len(data))(*data),
                                        len(data),
                                        self._aidlab_sdk_ptr)

    def _calculate_orientation(self, data: bytearray):
        self.lib.processOrientationPackage(
            (c_uint8 * len(data))(*data),
            len(data),
            self._aidlab_sdk_ptr)

    def _calculate_steps(self, data: bytearray):
        self.lib.processStepsPackage((c_uint8 * len(data))(*data),
                                     len(data), self._aidlab_sdk_ptr)

    def _calculate_heart_rate(self, data: bytearray):
        self.lib.processHeartRatePackage((c_uint8 * len(data))(*data),
                                         len(data), self._aidlab_sdk_ptr)

    def _calculate_sound_volume(self, data: bytearray):
        self.lib.processSoundVolumePackage(
            (c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _did_receive_raw_cmd_value(self, _: BleakGATTCharacteristic, data: bytearray):
        """Calculate raw command data from raw data"""
        logger.debug("Received command: %s", str(data))
        self.lib.AidlabSDK_process_command((c_uint8 * len(data))(*data), len(data), self._aidlab_sdk_ptr)

    def _set_firmware_revision(self, firmware_revision):
        """Set firmware revision"""""
        firmware_revision_utf8 = firmware_revision.encode('utf-8')

        # Create c_uint8 array from encoded string
        firmware_revision_array = (c_uint8 * len(firmware_revision))(*firmware_revision_utf8)

        self.lib.AidlabSDK_set_firmware_revision(
            firmware_revision_array, len(firmware_revision), self._aidlab_sdk_ptr)

    def _set_hardware_revision(self, hardware_revision: str):
        data = (c_uint8 * len(hardware_revision))(*hardware_revision.encode('utf-8'))
        self.lib.AidlabSDK_set_hardware_revision(data, len(hardware_revision), self._aidlab_sdk_ptr)

    def _setup_ctypes(self):
        self.lib.AidlabSDK_create.argtypes = None
        self.lib.AidlabSDK_create.restype = POINTER(AidlabSDKPointer)

        self.lib.AidlabSDK_destroy.argtypes = [c_void_p]
        self.lib.AidlabSDK_destroy.restype = None

        self.lib.AidlabSDK_set_mtu.argtypes = [c_uint32, c_void_p]
        self.lib.AidlabSDK_set_mtu.restype = None

        self.lib.AidlabSDK_set_context.argtypes = [c_void_p, c_void_p]
        self.lib.AidlabSDK_set_context.restype = None

        self.lib.AidlabSDK_set_hardware_revision.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.AidlabSDK_set_hardware_revision.restype = None

        self.lib.AidlabSDK_set_firmware_revision.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.AidlabSDK_set_firmware_revision.restype = None

        self.lib.AidlabSDK_process_battery_package.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.AidlabSDK_process_battery_package.restype = None

        self.lib.AidlabSDK_process_command.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.AidlabSDK_process_command.restype = None

        self.lib.AidlabSDK_get_command.argtypes = [POINTER(c_uint8), c_void_p]
        self.lib.AidlabSDK_get_command.restype = POINTER(c_uint8)

        self.lib.AidlabSDK_get_collect_command.argtypes = [POINTER(c_uint8),
                                                 c_int,
                                                 POINTER(c_uint8),
                                                 c_int,
                                                 c_void_p]
        self.lib.AidlabSDK_get_collect_command.restype = POINTER(c_uint8)

        self.lib.AidlabSDK_set_aggressive_ecg_filtration.argtypes = [c_bool, c_void_p]
        self.lib.AidlabSDK_set_aggressive_ecg_filtration.restype = None
        
        # Legacy

        self.lib.processECGPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processECGPackage.restype = None

        self.lib.processTemperaturePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processTemperaturePackage.restype = None

        self.lib.processMotionPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processMotionPackage.restype = None

        self.lib.processRespirationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processRespirationPackage.restype = None

        self.lib.processActivityPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processActivityPackage.restype = None

        self.lib.processStepsPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processStepsPackage.restype = None

        self.lib.processOrientationPackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processOrientationPackage.restype = None

        self.lib.processHeartRatePackage.argtypes = [POINTER(c_uint8), c_int, c_void_p]
        self.lib.processHeartRatePackage.restype = None

    def _user_event_callback(self, _, timestamp):
        self._delegate.did_detect_user_event(self, timestamp)

    def _did_receive_error_callback(self, _, log_text):
        logger.error("[LIB] %s", log_text.decode("utf-8"))
        self._delegate.did_receive_error(self, log_text.decode("utf-8"))

    def _exercise_callback(self, _, exercise):
        exercise = self.Exercise.get(exercise, "None")
        self._delegate.did_detect_exercise(self, exercise)

    def _ecg_callback(self, _, timestamp, value):
        self._delegate.did_receive_ecg(self, timestamp, value)

    def _respiration_callback(self, _, timestamp, value):
        self._delegate.did_receive_respiration(self, timestamp, value)

    def _battery_callback(self, _, state_of_charge):
        self._delegate.did_receive_battery_level(self, state_of_charge)

    def _temperature_callback(self, _, timestamp, value):
        self._delegate.did_receive_skin_temperature(self, timestamp, value)

    def _accelerometer_callback(self, _, timestamp, ax, ay, az):
        self._delegate.did_receive_accelerometer(self, timestamp, ax, ay, az)

    def _gyroscope_callback(self, _, timestamp, gx, gy, gz):
        self._delegate.did_receive_gyroscope(self, timestamp, gx, gy, gz)

    def _magnetometer_callback(self, _, timestamp, mx, my, mz):
        self._delegate.did_receive_magnetometer(self, timestamp, mx, my, mz)

    def _orientation_callback(self, _, timestamp, roll, pitch, yaw):
        self._delegate.did_receive_orientation(self, timestamp, roll, pitch, yaw)

    def _quaternion_callback(self, _, timestamp, qw, qx, qy, qz):
        self._delegate.did_receive_quaternion(self, timestamp, qw, qx, qy, qz)

    def _body_position_callback(self, _, timestamp, body_position: int):
        self._delegate.did_receive_body_position(self, timestamp, BodyPosition(body_position))

    def _activity_callback(self, _, timestamp, activity: int):
        self._delegate.did_receive_activity(self, timestamp, ActivityType(activity))

    def _steps_callback(self, _, timestamp, value):
        self._delegate.did_receive_steps(self, timestamp, value)

    def _heart_rate_callback(self, _, timestamp, heart_rate):
        self._delegate.did_receive_heart_rate(self, timestamp, heart_rate)

    def _rr_callback(self, _, timestamp, rr):
        self._delegate.did_receive_rr(self, timestamp, rr)

    def _respiration_rate_callback(self, _, timestamp, value):
        self._delegate.did_receive_respiration_rate(self, timestamp, value)

    def _pressure_callback(self, _, timestamp, value):
        self._delegate.did_receive_pressure(self, timestamp, value)

    def _pressure_wear_state_did_change(self, _, wear_state):
        self._delegate.pressure_wear_state_did_change(self, WearState(wear_state))

    def _wear_state_did_change(self, _, wear_state):
        self._delegate.wear_state_did_change(self, WearState(wear_state))

    def _sound_volume_callback(self, _, timestamp, sound_volume):
        self._delegate.did_receive_sound_volume(self, timestamp, sound_volume)

    def _receive_command_callback(self):
        self._delegate.did_receive_command(self)

    def _received_message_callback(self, _, process, message):
        self._delegate.did_receive_message(self, process, message.decode("utf-8"))

    def _signal_quality_callback(self, _, timestamp, value):
        self._delegate.did_receive_signal_quality(self, timestamp, value)

    # Synchronization

    def _past_user_event_callback(self, _, timestamp):
        self._delegate.did_receive_past_user_event(self, timestamp)

    def _past_ecg_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_ecg(self, timestamp, value)

    def _past_respiration_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_respiration(self, timestamp, value)

    def _past_temperature_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_skin_temperature(self, timestamp, value)

    def _past_accelerometer_callback(self, _, timestamp, ax, ay, az):
        self._delegate.did_receive_past_accelerometer(self, timestamp, ax, ay, az)

    def _past_gyroscope_callback(self, _, timestamp, gx, gy, gz):
        self._delegate.did_receive_past_gyroscope(self, timestamp, gx, gy, gz)

    def _past_magnetometer_callback(self, _, timestamp, mx, my, mz):
        self._delegate.did_receive_past_magnetometer(self, timestamp, mx, my, mz)

    def _past_orientation_callback(self, _, timestamp, roll, pitch, yaw):
        self._delegate.did_receive_past_orientation(self, timestamp, roll, pitch, yaw)

    def _past_quaternion_callback(self, _, timestamp, qw, qx, qy, qz):
        self._delegate.did_receive_past_quaternion(self, timestamp, qw, qx, qy, qz)

    def _past_activity_callback(self, _, timestamp, activity: int):
        self._delegate.did_receive_past_activity(self, timestamp, ActivityType(activity))

    def _past_body_position_callback(self, _, timestamp, body_position):
        self._delegate.did_receive_past_body_position(self, timestamp, BodyPosition(body_position))

    def _past_pressure_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_pressure(self, timestamp, value)

    def _past_steps_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_steps(self, timestamp, value)

    def _past_heart_rate_callback(self, _, timestamp, heart_rate):
        self._delegate.did_receive_past_heart_rate(self, timestamp, heart_rate)

    def _past_rr_callback(self, _, timestamp, rr):
        self._delegate.did_receive_past_rr(self, timestamp, rr)

    def _past_respiration_rate_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_respiration_rate(self, timestamp, value)

    def _past_sound_volume_callback(self, _, timestamp, sound_volume):
        self._delegate.did_receive_past_sound_volume(self, timestamp, sound_volume)

    def _past_signal_quality_callback(self, _, timestamp, value):
        self._delegate.did_receive_past_signal_quality(self, timestamp, value)

    def _sync_state_did_change(self, _, sync_state):
        sync_state = self.Sync_state.get(sync_state, "empty")
        self._delegate.sync_state_did_change(self, sync_state)

    def _did_receive_unsynchronized_size(self, _, unsynchronized_size, sync_bytes_per_second):
        self._delegate.did_receive_unsynchronized_size(self,
                                                       unsynchronized_size,
                                                       sync_bytes_per_second)

    def _uuid(self, data_type: DataType):
        orientation_handle: int = 58 if version.parse("3.0.0") < version.parse(self.firmware_revision) else 55
        motion_handle: int = 61 if version.parse("3.0.0") < version.parse(self.firmware_revision) else 58

        uuids: Dict[DataType, Tuple[str, int]]  = {
            DataType.ECG:              ("46366e80-cf3a-11e1-9ab4-0002a5d5c51b", 16),
            DataType.RESPIRATION:      ("48366e80-cf3a-11e1-9ab4-0002a5d5c51b", 19),
            DataType.SKIN_TEMPERATURE: ("45366e80-cf3a-11e1-9ab4-0002a5d5c51b", 25),
            DataType.ACTIVITY:         ("61366e80-cf3a-11e1-9ab4-0002a5d5c51b", 49),
            DataType.STEPS:            ("62366e80-cf3a-11e1-9ab4-0002a5d5c51b", 52),
            DataType.SOUND_VOLUME:     ("52366e80-cf3a-11e1-9ab4-0002a5d5c51b", 31),
            DataType.HEART_RATE:       ("00002a37-0000-1000-8000-00805f9b34fb", 45),

            DataType.ORIENTATION:      ("63366e80-cf3a-11e1-9ab4-0002a5d5c51b", orientation_handle),
            DataType.MOTION:           ("49366e80-cf3a-11e1-9ab4-0002a5d5c51b", motion_handle),

            # Same as HEART_RATE
            DataType.RR:               ("00002a37-0000-1000-8000-00805f9b34fb", 45),
            # Same as ORIENTATION
            DataType.BODY_POSITION:    ("63366e80-cf3a-11e1-9ab4-0002a5d5c51b", orientation_handle),
            # Same as RESPIRATION
            DataType.RESPIRATION_RATE: ("48366e80-cf3a-11e1-9ab4-0002a5d5c51b", 19)
        }

        if data_type in uuids:
            return uuids[data_type]

        raise ValueError("Invalid DataType: {}".format(data_type))

    def _load_aidlab_sdk(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if 'linux' in sys.platform:
            library_name = "aidlabsdk-linux-gnueabihf.so" if os.uname()[4][:3] == 'arm' else "aidlabsdk-linux-gnu.so"
        elif 'win32' in sys.platform:
            library_name = "aidlabsdk.dll"
        elif 'darwin' in sys.platform:
            library_name = "aidlabsdk.dylib"
        else:
            raise RuntimeError("Unsupported operating system: {}".format(sys.platform))

        library_path = os.path.join(script_dir, library_name)
        return cdll.LoadLibrary(library_path)

    async def _send(self, message, size: int):
        max_cmd_length: int = 20

        for i in range(round(int(size/max_cmd_length) + (size % max_cmd_length > 0))):
            message_byte = bytearray(message[i*max_cmd_length:(i+1)*max_cmd_length])
            logger.debug("Sending bytes: %s", str(message_byte))
            await self._client.write_gatt_char(self._COMMAND_CHARACTERISTIC,
                                         message_byte, True)

    def _get_command(self, message):
        data_array = (c_uint8 * (len(message)+1))(*message.encode('utf-8'))
        return self.lib.AidlabSDK_get_command(data_array, self._aidlab_sdk_ptr)

    def _get_collect_command(self, realtime, sync):
        realtime_ = (c_uint8 * len(realtime))(*realtime)
        sync_ = (c_uint8 * len(sync))(*sync)
        return self.lib.AidlabSDK_get_collect_command(realtime_,
                                            len(realtime),
                                            sync_,
                                            len(sync),
                                            self._aidlab_sdk_ptr)

    def _handle_notification(self, sender: BleakGATTCharacteristic, data: bytearray):
        for (uuid, handle), func in self._uuid_function_map.items():
            if sender.handle == handle or sender.uuid.upper() == uuid.upper():
                func(data)
                return

    def _did_disconnect(self, _: BleakClient):
        if not self.is_connected:
            return
        
        self.lib.AidlabSDK_destroy(self._aidlab_sdk_ptr)
        self.is_connected = False
        self._delegate.did_disconnect(self)
