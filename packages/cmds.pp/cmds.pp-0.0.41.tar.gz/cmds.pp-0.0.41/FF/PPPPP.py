def is_package_installed(package_name):
    """使用 pip show 檢查是否已安裝指定的套件。"""
    import subprocess
    try:
        result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True)
        if "WARNING: Package(s) not found:" in result.stderr:
            # 如果出現警告，表示該套件未安裝
            return False
        # 若未出現警告，表示套件已安裝
        return True
    except Exception as e:
        # 捕捉任何異常並印出錯誤訊息
        print(f"發生錯誤: {e}")
        return False
    

print(is_package_installed("cmds.pp"))