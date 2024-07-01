import socket
import threading

from collections import deque
from typing import Iterable

import pyxel as px

import action
import config
import utils

from fonts import fonts
from popup_messages import PopupMessage


class FillAddr:
    def __init__(self):
        self.classes = ['0', '0', '0', '0']
        self.cursor_pos = 0

        self.letter_w = 3
        self.letter_h = 5
        self.letter_pd = 1
        self.x, self.y = self.get_addr_pos()

    def draw(self):
        self.draw_addr_classes()
        if utils.flicker(0.7):
            self.draw_cursor()

    def update(self):
        if (action.move_player_left() or
            (px.btn(px.KEY_LSHIFT) or px.btn(px.KEY_RSHIFT)) and
            px.btnp(px.KEY_TAB)):
            self.cursor_pos -=1
            if self.cursor_pos < 0:
                self.cursor_pos = len(self.classes) - 1
        elif action.move_player_right() or px.btnp(px.KEY_TAB):
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.classes):
                self.cursor_pos = 0
        if px.btnp(px.KEY_BACKSPACE):
            self.del_elem_in_addr_class()
        for digit in range(10):
            key = px.KEY_0 + digit
            if px.btnp(key):
                self.edit_addr_class(chr(key))
                self.switch_addr_class()

    def draw_addr_classes(self):
        x = self.x
        y = self.y
        for i, c in enumerate(self.classes):
            empty_digits = 3 - len(c)
            x += empty_digits * (self.letter_w + self.letter_pd)
            if len(c):
                col = config.TEXT2_COL if i == self.cursor_pos else config.TEXT1_COL
                px.text(x, y, c, col)
            x += len(c) * (self.letter_w + self.letter_pd)
            px.text(x, y, '.', config.TEXT2_COL)
            x += self.letter_pd + 2

    def draw_cursor(self):
        px.rect(
            self.x + self.cursor_pos * ((self.letter_w + 1) * 3 - 1 + 4),
            self.y + self.letter_h + 2,
            (self.letter_w + self.letter_pd) * 3 - self.letter_pd,
            1,
            config.TEXT2_COL)

    def get_addr_pos(self) -> (int, int):
        w = (self.letter_w + 1) * len('192.168.101.101') - 1
        return utils.centerize_rect_in_rect(
            w, self.letter_h,
            0, 0,
            config.WINDOW_WDT, config.WINDOW_HGT)

    def edit_addr_class(self, key: str):
        # current class
        cc = self.classes[self.cursor_pos]
        if cc == '0' or len(cc) == 3:
            cc = key
        else:
            cc += key
        if int(cc) > 255:
            cc = '255'
        self.classes[self.cursor_pos] = cc

    def switch_addr_class(self):
        cc = self.classes[self.cursor_pos]
        last_class_elem = self.cursor_pos == len(self.classes) - 1
        if (len(cc) == 3 or cc == '0') and not last_class_elem:
            self.cursor_pos += 1

    def del_elem_in_addr_class(self):
        cc = self.classes[self.cursor_pos]
        if cc == '0':
            return
        if len(cc) == 1:
            cc = '0'
        else:
            cc = cc[:-1]
        self.classes[self.cursor_pos] = cc


class ChooseAddr:
    def __init__(self):
        self.cursor_pos = 0
        self.letter_w = 3
        self.letter_h = 5
        self.x, self.y = self.get_addr_pos()
        self.pd = 12

        self.addrs: Iterable[(str, int)] = []

    def draw(self):
        if self.addrs:
            self.draw_addrs()
        else:
            col = config.TEXT2_COL if utils.flicker(0.7) else config.TEXT1_COL
            px.text(self.x, self.y, 'waiting', col)

    def update(self):
        if action.move_player_up():
            self.cursor_pos -= 1
            if self.cursor_pos < 0:
                self.cursor_pos = 0
        if action.move_player_down():
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.addrs):
                self.cursor_pos = len(self.addrs) - 1
    @property
    def current(self):
        return self.addrs[self.cursor_pos]

    def get_addr_pos(self) -> (int, int):
        w = (self.letter_w + 1) * len('192.168.101.101') - 1
        return utils.centerize_rect_in_rect(
            w, self.letter_h,
            0, 0,
            config.WINDOW_WDT, config.WINDOW_HGT)

    def draw_addrs(self):
        px.text(self.x, self.y, self.addrs[self.cursor_pos][0], config.TEXT2_COL)
        if self.cursor_pos > 0:
            px.text(
                self.x + self.pd // 2,
                self.y - self.pd, self.addrs[self.cursor_pos-1][0], config.TEXT1_COL)
        if self.cursor_pos < len(self.addrs) - 1:
            px.text(
                self.x + self.pd // 2,
                self.y + self.pd, self.addrs[self.cursor_pos+1][0], config.TEXT1_COL)
        if utils.flicker(0.7):
            utils.draw_selection_cursor(
                self.x - 8,
                self.y - (self.letter_h - len(config.SELECTION_CURSOR_DATA)) // 2,
                1)

class Server(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Waiting user')
        self.y = 12

        self.host: str | None = None
        self.fill_addr = FillAddr()
        self.addr_filled = False

        self.choose_addr = ChooseAddr()

        self.try_to_send_addr_acceptance = False
        self.should_close_addrs_listening = False

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        if self.addr_filled:
            self.choose_addr.draw()
        else:
            self.fill_addr.draw()
                    
    def update(self):
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.pop()

        if self.addr_filled:
            self.choose_addr.update()

            if action.resume() and self.choose_addr.addrs:
                self.try_to_send_addr_acceptance = True

            if self.try_to_send_addr_acceptance:
                self.try_to_send_addr_acceptance = False
                t = threading.Thread(target=self.send_addr_acceptance)
                t.start()
        else:
            self.fill_addr.update()
            if action.resume():
                self.addr_filled = True
                self.host = '.'.join(self.fill_addr.classes)
                t = threading.Thread(target=self.get_new_addrs)
                t.start()

    def get_new_addrs(self):
        while True:
            if self.should_close_addrs_listening:
                return
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, config.PORT))
                s.listen(1)
                s.settimeout(config.SOCKET_TIMEOUT)
                try:
                    conn, addr = s.accept()
                    to_add = True
                    for i in self.choose_addr.addrs:
                        if addr[0] in i[0]:
                            to_add = False
                            break
                    if to_add:
                        self.choose_addr.addrs.append(addr)
                except OSError:
                    pass
                except TimeoutError:
                    pass

    def send_addr_acceptance(self):
        self.should_close_addrs_listening = True
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, config.PORT))
                    s.listen(1)
                    s.settimeout(config.SOCKET_TIMEOUT)
                    conn, addr = s.accept()
                    if addr[0] == self.choose_addr.current[0]:
                        conn.sendall(b'accept')
                        self.run_game()
            except OSError:
                pass
            except TimeoutError:
                pass

    def run_game(self):
        print('game is running')


class Client(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Connect2server')
        self.y = 12
        self.addr = FillAddr()

        self.should_send_requests_for_connection = False
        self.was_accept = False
        t = threading.Thread(target=self.send_request_for_connection)
        t.start()

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        self.addr.draw()

    def update(self):
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.pop()
        self.addr.update()
        if action.resume():
            self.should_send_requests_for_connection = True

        if self.was_accept:
            self.run_game()

    def send_request_for_connection(self):
        while True:
            if not self.should_send_requests_for_connection:
                continue
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(config.SOCKET_TIMEOUT)
                    s.connect(('.'.join(self.addr.classes), config.PORT))
                    s.sendall(b'')
                    data = s.recv(1024).decode()
                    if data == 'accept':
                        self.was_accept = True
                        return
            except OSError:
                pass
            except TimeoutError:
                pass
            except ConnectionResetError:
                pass
            except ConnectionRefusedError:
                pass

    def run_game(self):
        print('game is running')


class OnlineCoopMenu(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Online coop')
        self.y = 12

        self.choosed = False
        self.options = (
            ('Wait user', lambda: Server(self._scenes)),
            ('Connect', lambda: Client(self._scenes)),
        )
        self.option_names = tuple(i[0] for i in self.options)
        self.options_pd = 6
        self.cursor_pos = 0
        self.options_x, self.options_y = self.get_options_pos()

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        self.draw_options()
        if utils.flicker(0.7):
            utils.draw_selection_cursor(
                self.options_x - max(map(len, config.SELECTION_CURSOR_DATA)) - 4,
                self.options_y + (self.letter_sz - len(config.SELECTION_CURSOR_DATA)) // 2 + (self.letter_sz + self.options_pd) * self.cursor_pos,
                1)

    def update(self):
        if action.move_player_up():
            self.cursor_pos -= 1
            if self.cursor_pos < 0:
                self.cursor_pos = 0
        if action.move_player_down():
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.options):
                self.cursor_pos = len(self.options) - 1
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.pop()
        if action.resume():
            actn = self.options[self.cursor_pos][1]
            self._scenes.append(actn())

    def get_options_pos(self) -> (int, int):
        self.letter_sz = fonts['inkscript'].letter_sz
        w = (self.letter_sz + 1) * max(map(len, self.option_names)) - 1
        h = (self.letter_sz + self.options_pd) * len(self.option_names) - self.options_pd
        return utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)

    def draw_options(self):
        y = self.options_y
        for i, option_name in enumerate(self.option_names):
            col = config.TEXT2_COL if i == self.cursor_pos else config.TEXT1_COL
            fonts['inkscript'].draw(self.options_x, y, option_name, col)
            y += self.letter_sz + self.options_pd
