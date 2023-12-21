class PantheonConfiguration:
    PANTHEON_ERROR_CODE_STANDARD = -1
    PANTHEON_SUCCESS_CODE_STANDARD = 0
    PANTHEON_OS = ""
    PANTHEON_REQUESTS_SUCCESS_CODE = 200
    PANTHEON_PROXY = False
    PANTHEON_DEFAULT_COUNT = 0
    webcams_found = []
    num_webcams_found = 0
    just_ip_addresses = []

    proxy_api = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite"