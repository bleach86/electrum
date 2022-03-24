from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_string('''
<CSDialog@Popup>
    id: popup
    title: 'Coldstaking'
    size_hint: 1.0, 1.0
    BoxLayout:
        orientation: 'vertical'

        Widget:
            size_hint: 1, 0.1

        Label:
            size_hint: 1, 0.1
            text: _('Coldstaking change address:')
            height: '48dp'
            halign: 'left'
            text_size: self.size

        TextInput:
            size_hint: 1, None
            height: '40dp'
            id: textinput_coldstaking_changeaddress
            valign: 'center'
            multiline: False
            unfocus_on_touch: False
            focus: True

        Label:
            size_hint: 1, 0.1
            text: _('Coldstaking spend changeaddresses:')
            height: '48dp'
            halign: 'left'
            text_size: self.size

        TextInput:
            size_hint: 1, None
            height: '40dp'
            id: textinput_coldstaking_spend_changeaddress
            valign: 'center'
            multiline: False
            unfocus_on_touch: False
            focus: True

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Button:
                text: 'Add'
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.on_add_cs_spend_addr()
            Button:
                text: 'Remove'
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.on_remove_cs_spend_addr()

        TextInput:
            size_hint: 1, 1
            height: '40dp'
            id: textinput_coldstaking_spend_changeaddresses
            valign: 'center'
            multiline: True
            unfocus_on_touch: False
            focus: True

        Widget:
            size_hint: 1, 0.1

        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Button:
                text: 'Cancel'
                size_hint: 0.5, None
                height: '48dp'
                on_release: popup.dismiss()
            Button:
                text: 'OK'
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.apply_cs_stake_address(popup)
''')


from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.clock import Clock

from electrum.gui.kivy.i18n import _
from functools import partial

class CSDialog(Factory.Popup):

    def __init__(self, app, plugins, config, callback):
        self.app = app
        self.config = config
        self.callback = callback

        Factory.Popup.__init__(self)

    def set_data(self):
        ti_stake = self.ids.textinput_coldstaking_changeaddress
        cs_changeaddress = self.app.wallet.get_cs_changeaddress()
        ti_stake.text = '' if not cs_changeaddress else cs_changeaddress

        ti_spend = self.ids.textinput_coldstaking_spend_changeaddresses
        ti_spend.text = '\n'.join(self.app.wallet.list_cs_spendchangeaddresses())

    def on_add_cs_spend_addr(self):
        addr = self.ids.textinput_coldstaking_spend_changeaddress.text
        try:
            self.app.wallet.add_cs_spendchangeaddress(addr)
        except Exception as e:
            self.app.show_info(_('Could not add coldstaking spend address: ') + repr(e)) # repr because str(Exception()) == ''
            return
        ti_spend = self.ids.textinput_coldstaking_spend_changeaddresses
        ti_spend.text = '\n'.join(self.app.wallet.list_cs_spendchangeaddresses())
        self.ids.textinput_coldstaking_spend_changeaddress.text = ''

    def on_remove_cs_spend_addr(self):
        addr = self.ids.textinput_coldstaking_spend_changeaddress.text
        try:
            self.app.wallet.remove_cs_spendchangeaddress(addr)
        except Exception as e:
            self.app.show_info(_('Could not remove coldstaking spend address: ') + repr(e)) # repr because str(Exception()) == ''
            return
        ti_spend = self.ids.textinput_coldstaking_spend_changeaddresses
        ti_spend.text = '\n'.join(self.app.wallet.list_cs_spendchangeaddresses())
        self.ids.textinput_coldstaking_spend_changeaddress.text = ''

    def apply_cs_stake_address(self, popup):
        new_addr = self.ids.textinput_coldstaking_changeaddress.text
        try:
            self.app.wallet.set_cs_changeaddress(new_addr)
        except Exception as e:
            self.app.show_info(_('Could not set coldstaking address: ') + repr(e)) # repr because str(Exception()) == ''
            return
        self.callback()
        popup.dismiss()
