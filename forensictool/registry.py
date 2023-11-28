import winreg

def get_subkeys(hive, subkey):
    try:
        with winreg.OpenKey(hive, subkey) as key:
            subkeys = [winreg.EnumKey(key, i) for i in range(winreg.QueryInfoKey(key)[0])]
        return subkeys
    except FileNotFoundError:
        print(f"Registry key not found: {subkey}")
        return []
    except Exception as e:
        print(f"Error getting registry subkeys: {e}")
        return []


def read_registry_value(hive, subkey, value_name):
    try:
        with winreg.OpenKey(hive, subkey) as key:
            value, value_type = winreg.QueryValueEx(key, value_name)
        return value, value_type
    except FileNotFoundError:
        print(f"Registry key not found: {subkey}")
        return None, None
    except Exception as e:
        print(f"Error reading registry value: {e}")
        return None, None


def registry_all(hive, root_key):
    subkeys_list = get_subkeys(hive, root_key)

    for subkey_name in subkeys_list:
        full_subkey = f"{root_key}\\{subkey_name}"
        value, value_type = read_registry_value(hive, full_subkey, "DisplayName")

        if value:
            print(f"Found under {full_subkey}: {value} (Type: {value_type})")

def registry_keyword(hive, root_key, keyword):
    # 특정 루트 키에서 시작하여 모든 하위 키 검색
    subkeys_list = get_subkeys(hive, root_key)

    for subkey_name in subkeys_list:
        full_subkey = f"{root_key}\\{subkey_name}"
        # 하위 키에서 DisplayName 값 읽기
        value, value_type = read_registry_value(hive, full_subkey, "DisplayName")

        # DisplayName에 키워드가 포함되어 있다면 출력
        if value and keyword.lower() in value.lower():
            print(f"Match found under {full_subkey}: {value} (Type: {value_type})")

def main():
    user_keyword = input("Enter keyword to search in registry (Enter 'all' to search the entire registry): ")

    # 검색 기능 : all 검색하면 다 나오고, keyword 따로 넣으면 검색됨
    if user_keyword.lower() == 'all':
        registry_all(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE")
    else:
        registry_keyword(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", user_keyword)

if __name__ == "__main__":
    main()