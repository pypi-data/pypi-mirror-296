import sys
# if sys.version_info < (3, 8):
print( sys.version_info < (3, 8) )



def get_package_url(package_name):
    import sys
    if sys.version_info < (3, 8):
        import importlib_metadata as metadata  # import importlib_metadata
    else:
        import importlib.metadata as metadata  # import importlib
    ##########################################
    try:
        # 獲取包的元數據
        pkg_metadata = metadata.metadata(package_name)
        # 返回首頁 URL
        return pkg_metadata.get('Home-page', 'No URL found')
    except metadata.PackageNotFoundError:
        return 'Package not found'

package_name = 'cmds.pp'  # 替換為你要查詢的包名
print(get_package_url(package_name))



