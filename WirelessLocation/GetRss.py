# -*- coding:utf-8 -*-
import datetime
import time
from ctypes import *
from ctypes.wintypes import *
from sys import exit
from RssData import DataBase


def customresize(array, new_size):
    return (array._type_ * new_size).from_address(addressof(array))


wlanapi = windll.LoadLibrary('wlanapi.dll')

ERROR_SUCCESS = 0


class GUID(Structure):          # 定义GUID结构体
    _fields_ = [
        ('Data1', c_ulong),
        ('Data2', c_ushort),
        ('Data3', c_ushort),
        ('Data4', c_ubyte * 8),
    ]


WLAN_INTERFACE_STATE = c_uint                         # WLAN接口的状态
(wlan_interface_state_not_ready,                      # =0 The interface is not ready to operate.
 wlan_interface_state_connected,                      # =1 The interface is connected to a network.
 wlan_interface_state_ad_hoc_network_formed,          # =2 The interface is the first node in an ad hoc network.
 wlan_interface_state_disconnecting,                  # =3 The interface is disconnecting from the current network.
 wlan_interface_state_disconnected,                   # =4 The interface is not connected to any network.
 wlan_interface_state_associating,                    # =5 The interface is attempting to associate with a network.
 wlan_interface_state_discovering,                    # =6 The interface is not covering to any network.
 wlan_interface_state_authenticating                  # =7 The interface is in the process of authenticating.
 ) = map(WLAN_INTERFACE_STATE, range(0, 8))


class WLAN_INTERFACE_INFO(Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),                       # 接口的GUID
        ("strInterfaceDescription", c_wchar * 256),    # 接口的描述信息
        ("isState", WLAN_INTERFACE_STATE)              # 包含一个 WLAN_INTERFACE_STATE 值，标示这个接口的当前状态。
    ]


class WLAN_INTERFACE_INFO_LIST(Structure):              # 枚举处当前系统安装的所有无线网卡的接口信息
    _fields_ = [
        ("NumberOfItems", DWORD),                       # WLAN_INTERFACE_INFO 中包含的单元的个数。
        ("Index", DWORD),                               # 当前单元的索引，从0开始到 NumberOfItems-1
                                                        # 这个参数一般用于在WLAN_INTERFACE_INFO_LIST,被用作参数传递时的一个传递偏移量,这个参数在用之前必须要进行初始化。
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)      # 包含WLAN_INTERFACE_INFO 结构体的阵列，用于记录接口信息。
    ]


WLAN_MAX_PHY_TYPE_NUMBER = 0x8
DOT11_SSID_MAX_LENGTH = 32
WLAN_REASON_CODE = DWORD

DOT11_BSS_TYPE = c_uint                               # 枚举类型，用来标示这个网络类型是 infrastructure 还是 independent
(dot11_BSS_type_infrastructure,
 dot11_BSS_type_independent,
 dot11_BSS_type_any                                    # 是 infrastructure 或者 independent BSS网络
 ) = map(DOT11_BSS_TYPE, range(1, 4))

DOT11_PHY_TYPE = c_uint                               # 枚举类型，PHY类型
dot11_phy_type_unknown = 0                            # Specifies an unknown or uninitialized PHY type
dot11_phy_type_any = 0                                # Specifies any PHY type
dot11_phy_type_fhss = 1                               # Specifies a frequency-hopping spread-spectrum (FHSS) PHY. Bluetooth devices can use FHSS or an adaptation of FHSS
dot11_phy_type_dsss = 2                               # Specifies a direct sequence spread spectrum (DSSS) PHY type
dot11_phy_type_irbaseband = 3                         # Specifies an infrared (IR) baseband PHY type
dot11_phy_type_ofdm = 4                               # Specifies an orthogonal frequency division multiplexing (OFDM) PHY type.  802.11a devices can use OFDM
dot11_phy_type_hrdsss = 5                             # pecifies a high-rate DSSS (HRDSSS) PHY type
dot11_phy_type_erp = 6                                # Specifies an extended rate PHY type (ERP). 802.11g devices can use ERP
dot11_phy_type_ht = 7                                 # Specifies the 802.11n PHY type
dot11_phy_type_IHV_start = 0x80000000                 # Specifies the start of the range that is used to define PHY types that are developed by an independent hardware vendor (IHV)
dot11_phy_type_IHV_end = 0xffffffff                   # Specifies the start of the range that is used to define PHY types that are developed by an independent hardware vendor (IHV)

DOT11_AUTH_ALGORITHM = c_uint
DOT11_AUTH_ALGO_80211_OPEN = 1
DOT11_AUTH_ALGO_80211_SHARED_KEY = 2
DOT11_AUTH_ALGO_WPA = 3
DOT11_AUTH_ALGO_WPA_PSK = 4
DOT11_AUTH_ALGO_WPA_NONE = 5
DOT11_AUTH_ALGO_RSNA = 6
DOT11_AUTH_ALGO_RSNA_PSK = 7
DOT11_AUTH_ALGO_IHV_START = 0x80000000
DOT11_AUTH_ALGO_IHV_END = 0xffffffff

DOT11_CIPHER_ALGORITHM = c_uint
DOT11_CIPHER_ALGO_NONE = 0x00
DOT11_CIPHER_ALGO_WEP40 = 0x01
DOT11_CIPHER_ALGO_TKIP = 0x02
DOT11_CIPHER_ALGO_CCMP = 0x04
DOT11_CIPHER_ALGO_WEP104 = 0x05
DOT11_CIPHER_ALGO_WPA_USE_GROUP = 0x100
DOT11_CIPHER_ALGO_RSN_USE_GROUP = 0x100
DOT11_CIPHER_ALGO_WEP = 0x101
DOT11_CIPHER_ALGO_IHV_START = 0x80000000
DOT11_CIPHER_ALGO_IHV_END = 0xffffffff

WLAN_AVAILABLE_NETWORK_CONNECTED = 1
WLAN_AVAILABLE_NETWORK_HAS_PROFILE = 2

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002


class DOT11_SSID(Structure):
    _fields_ = [
        ("SSIDLength", c_ulong),
        ("SSID", c_char * DOT11_SSID_MAX_LENGTH)
    ]


class WLAN_AVAILABLE_NETWORK(Structure):       # 结构体，包含可用无线网络（network）单元的信息
    _fields_ = [
        ("ProfileName", c_wchar * 256),
        ("dot11Ssid", DOT11_SSID),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("NumberOfBssids", c_ulong),
        ("NetworkConnectable", c_bool),
        ("wlanNotConnectableReason", WLAN_REASON_CODE),
        ("NumberOfPhyTypes", c_ulong),
        ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_TYPE_NUMBER),
        ("MorePhyTypes", c_bool),
        ("wlanSignalQuality", c_ulong),
        ("SecurityEnabled", c_bool),
        ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM),
        ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM),
        ("Flags", DWORD),
        ("Reserved", DWORD)
    ]


class WLAN_AVAILABLE_NETWORK_LIST(Structure):       # 搜索接口上可用的网络
    _fields_ = [
        ("NumberOfItems", DWORD),
        ("Index", DWORD),
        ("Network", WLAN_AVAILABLE_NETWORK * 1)
    ]


DOT11_MAC_ADDRESS = c_ubyte * 6

DOT11_CIPHER_ALGORITHM = c_uint
DOT11_CIPHER_ALGO_NONE = 0x00
DOT11_CIPHER_ALGO_WEP40 = 0x01
DOT11_CIPHER_ALGO_TKIP = 0x02

DOT11_PHY_TYPE = c_uint
DOT11_PHY_TYPE_UNKNOWN = 0
DOT11_PHY_TYPE_ANY = 0
DOT11_PHY_TYPE_FHSS = 1
DOT11_PHY_TYPE_DSSS = 2
DOT11_PHY_TYPE_IRBASEBAND = 3
DOT11_PHY_TYPE_OFDM = 4
DOT11_PHY_TYPE_HRDSSS = 5
DOT11_PHY_TYPE_ERP = 6
DOT11_PHY_TYPE_HT = 7
DOT11_PHY_TYPE_IHV_START = 0X80000000
DOT11_PHY_TYPE_IHV_END = 0XFFFFFFFF


class WLAN_RATE_SET(Structure):
    _fields_ = [
        ("uRateSetLength", c_ulong),
        ("usRateSet", c_ushort * 126)
    ]


class WLAN_BSS_ENTRY(Structure):
    _fields_ = [
        ("dot11Ssid", DOT11_SSID),
        ("uPhyId", c_ulong),
        ("dot11Bssid", DOT11_MAC_ADDRESS),
        ("dot11BssType", DOT11_BSS_TYPE),
        ("dot11BssPhyType", DOT11_PHY_TYPE),
        ("lRssi", c_long),
        ("uLinkQuality", c_ulong),
        ("bInRegDomain", c_bool),
        ("usBeaconPeriod", c_ushort),
        ("ullTimestamp", c_ulonglong),
        ("ullHostTimestamp", c_ulonglong),
        ("usCapabilityInformation", c_ushort),
        ("ulChCenterFrequency", c_ulong),
        ("wlanRateSet", WLAN_RATE_SET),
        ("ulIeOffset", c_ulong),
        ("ulIeSize", c_ulong)]


class WLAN_BSS_LIST(Structure):
    _fields_ = [
        ("TotalSize", DWORD),
        ("NumberOfItems", DWORD),
        ("NetworkBSS", WLAN_BSS_ENTRY * 1)
    ]


class WLAN_AVAILABLE_NETWORK_LIST_BSS(Structure):
    _fields_ = [
        ("TotalSize", DWORD),
        ("NumberOfItems", DWORD),
        ("Network", WLAN_BSS_ENTRY * 1)
    ]


WlanOpenHandle = wlanapi.WlanOpenHandle
WlanOpenHandle.argtypes = (DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE))
WlanOpenHandle.restype = DWORD

WlanCloseHandle = wlanapi.WlanCloseHandle
WlanCloseHandle.argtypes = (HANDLE, c_void_p)
WlanCloseHandle.restype = DWORD

WlanEnumInterfaces = wlanapi.WlanEnumInterfaces
WlanEnumInterfaces.argtypes = (HANDLE, c_void_p,
                               POINTER(POINTER(WLAN_INTERFACE_INFO_LIST)))
WlanEnumInterfaces.restype = DWORD

WlanGetAvailableNetworkList = wlanapi.WlanGetAvailableNetworkList
WlanGetAvailableNetworkList.argtypes = (HANDLE, POINTER(GUID), DWORD, c_void_p,
                                        POINTER(POINTER(WLAN_AVAILABLE_NETWORK_LIST)))
WlanGetAvailableNetworkList.restype = DWORD

WlanGetNetworkBssList = wlanapi.WlanGetNetworkBssList
WlanGetNetworkBssList.argtypes = (HANDLE, POINTER(GUID), POINTER(GUID), POINTER(GUID), c_bool, c_void_p,
                                  POINTER(POINTER(WLAN_BSS_LIST)))
WlanGetNetworkBssList.restype = DWORD

WlanFreeMemory = wlanapi.WlanFreeMemory
WlanFreeMemory.argtypes = [c_void_p]

WlanScan = wlanapi.WlanScan
WlanScan.argtypes = (HANDLE, POINTER(GUID), c_void_p, c_void_p, c_void_p)
WlanScan.restype = DWORD


def get_interface():
    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
        # find all wireless network interfaces
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        # find each available network for each interface
        for iface in ifaces:
            # print "Interface: %s" % (iface.strInterfaceDescription)
            interface = iface.strInterfaceDescription

    finally:
        WlanFreeMemory(pInterfaceList)
    return interface


class MAC_BSSID_POWER:
    """Classe para os valores retirados"""

    def __init__(self, mac, bssid):
        self.mac = str(mac)
        self.bssid = str(bssid)
        self.valores = []

    def addPower(self, power):
        self.valores.append(int(power))

    def getBssid(self):
        return self.bssid

    def getPowers(self):
        return self.valores

    def getMac(self):
        return self.mac


def get_BSSI():
    BSSI_Values = {}

    NegotiatedVersion = DWORD()
    ClientHandle = HANDLE()
    ret = WlanOpenHandle(1, None, byref(NegotiatedVersion), byref(ClientHandle))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
        # find all wireless network interfaces
    pInterfaceList = pointer(WLAN_INTERFACE_INFO_LIST())
    ret = WlanEnumInterfaces(ClientHandle, None, byref(pInterfaceList))
    if ret != ERROR_SUCCESS:
        exit(FormatError(ret))
    try:
        ifaces = customresize(pInterfaceList.contents.InterfaceInfo,
                              pInterfaceList.contents.NumberOfItems)
        # find each available network for each interface
        for iface in ifaces:
            # print "Interface: %s" % (iface.strInterfaceDescription)

            pAvailableNetworkList2 = pointer(WLAN_BSS_LIST())

            ret2 = WlanGetNetworkBssList(ClientHandle,
                                         byref(iface.InterfaceGuid),
                                         None,
                                         None, True, None,
                                         byref(pAvailableNetworkList2))
        if ret2 != ERROR_SUCCESS:
            exit(FormatError(ret2))
        try:
            retScan = WlanScan(ClientHandle, byref(iface.InterfaceGuid), None, None, None)
            if retScan != ERROR_SUCCESS:
                exit(FormatError(retScan))
            avail_net_list2 = pAvailableNetworkList2.contents
            networks2 = customresize(avail_net_list2.NetworkBSS,
                                     avail_net_list2.NumberOfItems)

            for network in networks2:
                SSID = str(network.dot11Ssid.SSID[:network.dot11Ssid.SSIDLength])
                BSSID = ':'.join('%02x' % b for b in network.dot11Bssid).upper()
                signal_strength = str(network.lRssi)

                # print "SSID: " + SSID + " BSSID: "+ BSSID+ " SS: "+signal_strength

                BSSI_Values[BSSID] = [SSID, signal_strength]

                # print "Total "+str(len(networks2))
                # print BSSI_Values

        finally:
            WlanFreeMemory(pAvailableNetworkList2)
            WlanCloseHandle(ClientHandle, None)
    finally:
        WlanFreeMemory(pInterfaceList)
    return BSSI_Values



def get_BSSI_times_and_total_seconds(times, seconds):
    BSSI_to_return = {}

    for i in range(0, seconds * times):
        time_to_sleep = float(1.0 / times)
        time.sleep(time_to_sleep)
        got_bssi_temp = get_BSSI()

        for bssi in got_bssi_temp:
            if not BSSI_to_return.get(bssi):
                BSSI_to_return[bssi] = MAC_BSSID_POWER(bssi, got_bssi_temp[bssi][0])
                BSSI_to_return[bssi].addPower(got_bssi_temp[bssi][1])

                # BSSI_to_return[bssi] = [got_bssi_temp[bssi][1]]

            else:
                BSSI_to_return[bssi].addPower(got_bssi_temp[bssi][1])
                # BSSI_to_return[bssi].append(got_bssi_temp[bssi][1])
        print ("Medicao " + str(i) + " de " + str(seconds * times))
    print (BSSI_to_return)
    return BSSI_to_return


# if __name__ == '__main__':
#
#     # print get_interface()
#     import time
#     database = DataBase()
#     test = get_BSSI()
#     # 获取划分区域
#     place = input("请输入划分的区域:")
#     for i in range(0, 10):
#         time.sleep(1)  # 1秒钟收集一次数据
#         nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
#         oldTest = test
#         test = get_BSSI()
#         print ("Teste: " + str(i))
#         if oldTest == test:
#             print ("IGUAL")
#         else:
#             print ("DIFERENTE")
#         for key, value in test.items():
#             print(key)
#             print(value[0])
#             print(value[1])
#             database.RssInsert(key, value[0], value[1], nowtime, place, i)
#             print("----")
#     database.DbClose()
#     print("End")