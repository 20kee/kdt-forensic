import winreg
import json
import os
class RegistryForensicTool:
    def __init__(self):
        pass
    def registry_copy(self, key_url, folder):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_url)
            
            registry_info = {}
            for i in range(winreg.QueryInfoKey(key)[1]):
                name, value, _ = winreg.EnumValue(key, i)
                registry_info[name] = value

            if len(registry_info.keys()) == 0:
                os.mkdir(folder)
                try:
                    i=0
                    while True:
                        key2 = winreg.EnumKey(key, i)
                        self.registry_copy(key_url + '\\' + key2, folder + '\\' + key2)
                        i += 1
                except Exception as e2:
                    pass
            else:
                with open(folder, 'w') as file:
                    json.dump(registry_info, file, indent=4)

        except Exception as e:
            pass
        finally:
            winreg.CloseKey(key)

    def get_subkeys(self, hive, subkey):
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


    def read_registry_value(self, hive, subkey, value_name):
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


    def registry_all(self, hive, root_key):
        starting_point = winreg.HKEY_LOCAL_MACHINE
        subkeys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for subkey in subkeys:
            subkey_path = self.subkey
            subkeys_list = self.get_subkeys(starting_point, subkey_path)

            if subkeys_list:
                print(f"Subkeys under {subkey_path}: {subkeys_list}")

                for subkey_name in subkeys_list:
                    full_subkey = f"{subkey_path}\\{subkey_name}"
                    value, value_type = self.read_registry_value(starting_point, full_subkey, "DisplayName")
                    print(f"Value under {full_subkey}: {value} (Type: {value_type})")

            else:
                print(f"No subkeys found under {subkey_path}.")

    def registry_keyword(self, hive, root_key, keyword):
        # 특정 루트 키에서 시작하여 모든 하위 키 검색
        subkeys_list = self.get_subkeys(hive, root_key)

        for subkey_name in subkeys_list:
            full_subkey = f"{root_key}\\{subkey_name}"
            # 하위 키에서 DisplayName 값 읽기
            value, value_type = self.read_registry_value(hive, full_subkey, "DisplayName")

            # DisplayName에 키워드가 포함되어 있다면 출력
            if value and keyword.lower() in value.lower():
                print(f"Match found under {full_subkey}: {value} (Type: {value_type})")

def main():
    # user_keyword = input("Enter keyword : ")
    registry_forensic_tool = RegistryForensicTool()
    registry_forensic_tool.registry_copy("SOFTWARE\\Microsoft", 'Forensic Result\\registry')
    # 검색 기능 : all 검색하면 다 나오고, keyword 따로 넣으면 검색됨
    # if not user_keyword:
    #     registry_forensic_tool.registry_all()
    # else:
    #     registry_forensic_tool.registry_keyword(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", user_keyword)

if __name__ == "__main__":
    main()