# -*- coding: utf-8 -*-
import ctypes
import sys
import winreg

args = sys.argv
is_admin = ctypes.windll.shell32.IsUserAnAdmin()
if str(is_admin) == "0":
    is_admin = False
else:
    is_admin = True
configs = {}


class _E(BaseException):
    def __init__(self, arg=""):
        self.arg = arg


class EnvNotFundError(_E):
    def __str__(self):
        return (
            f"{self.arg}"
        )


class EnvError(_E):
    def __str__(self):
        return (
            f"{self.arg}"
        )


def config(**kwargs):
    configs.update(kwargs)


class systems:
    def __init__(self):
        self.mode = "systems"
        self.key = winreg.HKEY_LOCAL_MACHINE
        self.dirs = r"SYSTEM\CurrentControlSet\Control\Session "+(
            r"Manager\Environment")


class user:
    def __init__(self):
        self.mode = "user"
        self.key = winreg.HKEY_CURRENT_USER
        self.dirs = r"Environment"


class volatile:
    def __init__(self):
        self.mode = "volatile"
        self.key = winreg.HKEY_CURRENT_USER
        self.dirs = r"Volatile Environment"


class custom:
    def __init__(self):
        self.mode = "custom"
        self.key = winreg.HKEY_CURRENT_USER
        self.dirs = r"Software\python-lib\3.12\win_env\custom_env"
        self.f1 = winreg.CreateKeyEx(self.key, r"Software\python-lib")
        self.f2 = winreg.CreateKeyEx(self.f1, "3.12")
        self.f3 = winreg.CreateKeyEx(self.f2, "win_env")
        winreg.CreateKeyEx(self.f3, "custom_env")
        self.f1.Close()
        self.f2.Close()
        self.f3.Close()


def all_list():
    """概要

    全てのキー一覧を返します。

    :return: リスト形式で返します
    :rtype: list
    """
    values = {"systems": [], "user": [], "volatile": [], "custom": []}
    for i in ["systems", "user", "volatile", "custom"]:
        if i == "systems":
            values["systems"].append(lists(systems))
        elif i == "user":
            values["user"].append(lists(user))
        elif i == "volatile":
            values["volatile"].append(lists(volatile))
        elif i == "custom":
            values["custom"].append(lists(custom))
    return values


class open():
    def __init__(self, env_type):
        self.env_type = env_type
        self._list = lists
        self._get = get
        self._set = set
        self._del = dels
        self._add = add

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def list(self, types=None):
        return self._list(self.env_type, types)

    def get(self, key):
        return self._get(self.env_type, key)

    def set(self, key, value, type=1):
        return self._set(self.env_type, key, value, type)

    def dels(self, key):
        return self._del(self.env_type, key)

    def add(self, key, value, type=1):
        return self._add(self.env_type, key, value, type)


def lists(env_types, only=None):
    """概要

    キー一覧を返します。

    :env_type: env.userやenv.systemsかenv.volatileなどを指定してください。\n操作する場所を指定する場所です。
    :return: リスト形式で返します
    :rtype: list
    :only: Falseの場合は値のみのリストを返します。Trueの場合はキーのみを返します
    """
    env_type = env_types()
    if not (env_types in [systems, user, volatile, custom]):
        raise TypeError(f"{env_type.mode}は有効なタイプではないか、不正です。")
    with winreg.OpenKey(env_type.key, env_type.dirs) as wr:
        values = []
        valu = winreg.QueryInfoKey(wr)
        valu = valu[1]
        for i in range(valu):
            if not (str(winreg.EnumValue(wr, i)[2]) in ["1", "2"]):
                continue
            if only is None:
                values.append({winreg.EnumValue(wr, i)[0]:
                               winreg.EnumValue(wr, i)[1]})
            elif only is True:
                values.append(winreg.EnumValue(wr, i)[0])
            elif only is False:
                values.append(winreg.EnumValue(wr, i)[1])
            else:
                raise TypeError(f"{only}は有効ではありません。")
    return values


def get(env_types, key):
    """概要

    環境変数の値を取得します。キーが存在しない場合はエラーを返します。

    :env_type: env.userやenv.systemsかenv.volatileなどを指定してください。\n操作する場所を指定する場所です。
    :key: キーを指定してください。
    :return: str形式で返します
    :rtype: str
    :raises EnvNotFundError: BaseException
    """
    env_type = env_types()
    if not (env_types in [systems, user, volatile, custom]):
        raise TypeError(f"{env_type.mode}は有効なタイプではないか、不正です。")
    listss = lists(env_types, True)
    listss2 = lists(env_types, False)
    if not (key in listss):
        raise EnvNotFundError(f"{key}はキーとして存在しません。")
    loop = 0
    for i in listss:
        if str(i) == str(key):
            break
        loop += 1
    return listss2[loop]


def set(env_types, key, value, write_mode=1):
    """概要

    システム環境が存在しない場合は追加します。存在していたら上書きします。

    :env_type: env.userやenv.systemsかenv.volatileなどを指定してください。\n操作する場所を指定する場所です。
    :key: キーを指定してください。
    :value: 値を指定してください。
    :writemode: 1か2で指定してください。1は単純な文字列などに使用し、場所や複数個の場合は2を指定してください。
    :return: None
    :rtype: None
    """
    env_type = env_types()
    if not (env_types in [systems, user, volatile, custom]):
        raise TypeError(f"{env_type}は有効なタイプではないか、不正です。")
    if not (is_admin) and env_types == systems:
        raise PermissionError("管理者権限が必要です。")
    with winreg.OpenKey(
        env_type.key,
            env_type.dirs,
            access=winreg.KEY_WRITE) as wrr:
        if write_mode == 1:
            winreg.SetValueEx(wrr, key, 0, winreg.REG_SZ, value)
        elif write_mode == 2:
            winreg.SetValueEx(wrr, key, 0, winreg.REG_EXPAND_SZ,
                              value)
        else:
            raise TypeError(f"type {write_mode} は存在しません。")


def dels(env_types, key):
    """概要

    環境変数を削除します。存在しない場合は

    :env_type: env.userやenv.systemsかenv.volatileなどを指定してください。\n操作する場所を指定する場所です。
    :key: キーを指定してください。
    :return: None
    :rtype: None
    :raises EnvNotFoundError: BaseException
    """
    env_type = env_types()
    if not (env_types in [systems, user, volatile, custom]):
        raise TypeError(f"{env_type.mode}は有効なタイプではないか、不正です。")
    with winreg.OpenKey(
        env_type.key,
            env_type.dirs,
            access=winreg.KEY_WRITE
            ) as wr:
        listsd = lists(env_types, True)
        if not (key in listsd):
            raise EnvNotFundError(f"{key}はキーとして存在しません。")
        winreg.DeleteValue(wr, key)


def add(env_types, key, value, write_mode=1):
    """概要

    環境変数が存在しない場合は追加します。存在していたらEnvErrorを出します。

    :env_type: env.userやenv.systemsかenv.volatileなどを指定してください。操作する場所を指定する場所です。
    :key: キーを指定してください。
    :value: 値を指定してください。
    :writemode: 1か2で指定してください。1は単純な文字列などに使用し、場所や複数個の場合は2を指定してください。
    :return: None
    :rtype: None
    :raises EnvError: BaseException
    """
    listsd = lists(env_types, True)
    if key in listsd:
        raise EnvError(f"{key}は存在します。")
    set(env_types, key, value, write_mode)
