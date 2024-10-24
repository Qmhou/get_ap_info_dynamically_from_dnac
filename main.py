from dnac_api import get_auth_token, get_device_detail, get_device_enrichment_details, load_dnac_config

def get_ap_info_dynamically(ap_name):
    # 加载 DNAC 配置
    dnac_config = load_dnac_config()

    # 获取 x-auth-token
    token = get_auth_token(dnac_config)

    # 使用 AP 名称获取 nwDeviceId
    nwDeviceId = get_device_detail(ap_name, token, dnac_config)

    # 使用 nwDeviceId 获取 AP 的相关信息
    ap_info = get_device_enrichment_details(nwDeviceId, token, dnac_config)

    return ap_info

if __name__ == "__main__":
    ap_name = "test_ap"  # 触发的日志中 AP 名称
    ap_info = get_ap_info_dynamically(ap_name)

    print(f"AP 信息: {ap_info}")
