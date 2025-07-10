
import requests
from getpass import getpass
import tkinter as tk
from tkinter import messagebox, simpledialog

class RouterController:
    def __init__(self, ip, username, password, router_type):
        self.ip = ip
        self.username = username
        self.password = password
        self.router_type = router_type.lower()
        self.session = requests.Session()

    def login(self):
        if self.router_type == "tenda":
            return self._login_tenda()
        elif self.router_type == "tplink":
            return self._login_tplink()
        else:
            print("نوع الراوتر غير مدعوم حالياً.")
            return False

    def _login_tenda(self):
        url = f"http://{self.ip}/login/Auth"
        data = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(url, data=data)
            return response.ok
        except Exception as e:
            print(f"خطأ في الاتصال براوتر تيندا: {e}")
            return False

    def _login_tplink(self):
        url = f"http://{self.ip}/userRpm/LoginRpm.htm?username={self.username}&password={self.password}"
        try:
            response = self.session.get(url)
            return response.ok
        except Exception as e:
            print(f"خطأ في الاتصال براوتر تي بي لينك: {e}")
            return False

    def change_wifi_settings(self, ssid, password):
        if self.router_type == "tenda":
            return self._change_tenda_wifi(ssid, password)
        elif self.router_type == "tplink":
            return self._change_tplink_wifi(ssid, password)
        else:
            return False

    def _change_tenda_wifi(self, ssid, password):
        try:
            url = f"http://{self.ip}/goform/setWifi"
            payload = {
                "ssid": ssid,
                "encryption": "psk2",
                "password": password,
                "channel": "auto"
            }
            res = self.session.post(url, data=payload)
            return res.ok
        except Exception as e:
            print(f"خطأ في تغيير إعدادات واي فاي تيندا: {e}")
            return False

    def _change_tplink_wifi(self, ssid, password):
        try:
            url = f"http://{self.ip}/userRpm/WlanNetworkRpm.htm"
            payload = {
                "ssid1": ssid,
                "pskSecret": password,
                "authType": "WPA2-PSK"
            }
            res = self.session.post(url, data=payload)
            return res.ok
        except Exception as e:
            print(f"خطأ في تغيير إعدادات واي فاي تي بي لينك: {e}")
            return False

    def set_dns(self, dns1, dns2):
        print("إعداد DNS مخصص غير مدعوم حالياً عبر API، يجب استخدام واجهة الويب.")

    def update_firmware(self):
        print("ميزة التحديث التلقائي للبرامج الثابتة غير مدعومة حالياً عبر API.")

    def enable_vpn(self):
        print("تفعيل VPN غير متاح تلقائياً، يتطلب إعداد يدوي عبر واجهة الويب.")

# ================= GUI =====================

class RouterGUI:
    def __init__(self, master):
        self.master = master
        master.title("إعدادات الراوتر المتقدمة")
        self.label = tk.Label(master, text="مدير إعدادات الراوتر (Tenda & TP-Link)", font=("Arial", 14))
        self.label.pack(pady=10)

        self.ip_entry = self._make_entry("IP الراوتر:")
        self.type_entry = self._make_entry("نوع الراوتر (tenda / tplink):")
        self.user_entry = self._make_entry("اسم المستخدم:")
        self.pass_entry = self._make_entry("كلمة المرور:", show="*")

        self.login_button = tk.Button(master, text="تسجيل الدخول", command=self.login)
        self.login_button.pack(pady=10)

    def _make_entry(self, label_text, show=None):
        frame = tk.Frame(self.master)
        label = tk.Label(frame, text=label_text)
        label.pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="right")
        frame.pack(pady=5)
        return entry

    def login(self):
        ip = self.ip_entry.get()
        r_type = self.type_entry.get()
        user = self.user_entry.get()
        passwd = self.pass_entry.get()
        self.controller = RouterController(ip, user, passwd, r_type)
        if self.controller.login():
            messagebox.showinfo("نجاح", "تم تسجيل الدخول بنجاح!")
            self.show_wifi_options()
        else:
            messagebox.showerror("فشل", "فشل في تسجيل الدخول. تحقق من المعلومات.")

    def show_wifi_options(self):
        ssid = simpledialog.askstring("اسم الشبكة", "أدخل اسم الشبكة الجديد:")
        wifi_pass = simpledialog.askstring("كلمة المرور", "أدخل كلمة مرور جديدة:", show="*")
        if self.controller.change_wifi_settings(ssid, wifi_pass):
            messagebox.showinfo("تم", "✅ تم تغيير إعدادات الواي فاي.")
        else:
            messagebox.showerror("خطأ", "❌ فشل في تغيير الإعدادات.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = RouterGUI(root)
    root.mainloop()
