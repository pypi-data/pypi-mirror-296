from pgpl.utils import *

from pywebio import output, session, pin, SessionClosedException, SessionNotFoundException

import threading

class Page:
    def __init__(self, page_name=""):
        self.loaded = False
        self.main_scope = 'Main'
        self.page_name = page_name

    def load(self):
        if not self.loaded:
            output.put_scope(self.main_scope)  # 创建主scope
            self._on_load()
            self.loaded = True

    def unload(self):
        if self.loaded:
            self.loaded = False
            self._on_unload()
            output.remove(self.main_scope)

    def _on_load(self):
        pin.pin['isSessionExist'] = "1"
        self._load()  # 加载主页
        t = threading.Thread(target=self.__event_thread, daemon=False)  # 创建事件线程
        session.register_thread(t)  # 注册线程
        t.start()  # 启动线程


    def _load(self):pass
    
    def __event_thread(self):
        try:
            self._event_thread()
        except SessionClosedException as e:
            print("SessionClosed, exit.")
        except SessionNotFoundException as e:
            print("SessionNotFound, exit.")

    
    def _event_thread(self):
        while self.loaded:
            time.sleep(0.1)
            pass
    
    def _on_unload(self):
        pass

    def _value_list2buttons_type(self, l1):
        replace_dict = {
            "MainPage": t2t("Main"),
            "SettingPage": t2t("Setting")
        }
        for i in range(len(l1)):
            if l1[i] in replace_dict:
                l1[i] = (replace_dict[l1[i]], l1[i])
        return l1